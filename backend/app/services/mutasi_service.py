"""Mutasi service untuk SIMANIS62 V2.

Module ini menyediakan MutasiService untuk:
- Initiate mutation (mulai proses mutasi)
- Complete mutation (selesaikan mutasi)
- Cancel mutation (batalkan mutasi)
- Get mutation history
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AssetInMutationError,
    AssetNotFoundError,
    BusinessRuleError,
    MutationNotFoundError,
    MutationReasonTooShortError,
    RuanganNotFoundError,
    SameRoomMutationError,
)
from app.models.aset import Aset, StatusAset
from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.repositories.aset_repository import AsetRepository
from app.repositories.mutasi_repository import MutasiRepository
from app.repositories.ruangan_repository import RuanganRepository
from app.schemas.mutasi import (
    MutasiCancelRequest,
    MutasiCompleteRequest,
    MutasiCreate,
    MutasiResponse,
    MutasiSearchParams,
)
from app.schemas.response import PaginatedResponse
from app.services.base import BaseService

# Constants
MIN_ALASAN_LENGTH = 10
MUTATION_EXPIRY_DAYS = 7


class MutasiService(BaseService[RiwayatMutasi, MutasiRepository]):
    """Service untuk mutasi aset antar ruangan.

    Menyediakan:
    - initiate_mutation: Mulai proses mutasi
    - complete_mutation: Selesaikan mutasi
    - cancel_mutation: Batalkan mutasi
    - get_mutation_by_id: Get mutasi by ID
    - get_mutation_history: Get history mutasi
    - cancel_expired_mutations: Auto-cancel mutasi expired

    Example:
        ```python
        service = MutasiService(session)
        mutasi = await service.initiate_mutation(data, user_id)
        await service.complete_mutation(mutasi_id, user_id)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize MutasiService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, MutasiRepository(session), "MutasiService")
        self._aset_repo = AsetRepository(session)
        self._ruangan_repo = RuanganRepository(session)

    # =========================================================================
    # Validation Methods
    # =========================================================================

    def _validate_alasan(self, alasan: str) -> None:
        """Validate alasan minimal 10 karakter.

        Args:
            alasan: Alasan mutasi/pembatalan.

        Raises:
            MutationReasonTooShortError: Jika alasan terlalu pendek.
        """
        if len(alasan.strip()) < MIN_ALASAN_LENGTH:
            raise MutationReasonTooShortError(len(alasan.strip()))

    async def _validate_aset_exists(self, aset_id: str) -> Aset:
        """Validate aset exists dan return aset.

        Args:
            aset_id: UUID aset.

        Returns:
            Aset jika ditemukan.

        Raises:
            AssetNotFoundError: Jika aset tidak ditemukan.
        """
        aset = await self._aset_repo.get_by_id(aset_id)
        if not aset:
            raise AssetNotFoundError(aset_id)
        return aset

    async def _validate_ruangan_exists(self, ruangan_id: str) -> None:
        """Validate ruangan exists.

        Args:
            ruangan_id: UUID ruangan.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        exists = await self._ruangan_repo.exists(ruangan_id)
        if not exists:
            raise RuanganNotFoundError(ruangan_id)

    async def _validate_no_pending_mutation(self, aset_id: str) -> None:
        """Validate aset tidak memiliki pending mutation.

        Args:
            aset_id: UUID aset.

        Raises:
            AssetInMutationError: Jika aset sedang dalam mutasi.
        """
        has_pending = await self.repository.has_pending_mutation(aset_id)
        if has_pending:
            raise AssetInMutationError(aset_id)

    # =========================================================================
    # Mutation Operations
    # =========================================================================

    async def initiate_mutation(
        self, data: MutasiCreate, user_id: str
    ) -> RiwayatMutasi:
        """Mulai proses mutasi aset.

        Args:
            data: MutasiCreate schema dengan data mutasi.
            user_id: UUID user yang memproses.

        Returns:
            RiwayatMutasi yang baru dibuat.

        Raises:
            AssetNotFoundError: Jika aset tidak ditemukan.
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
            AssetInMutationError: Jika aset sedang dalam mutasi.
            SameRoomMutationError: Jika ruangan tujuan sama dengan asal.
        """
        self.log_info(f"Initiating mutation for asset: {data.aset_id}")

        # Validate aset
        aset = await self._validate_aset_exists(data.aset_id)

        # Check aset status
        if aset.status == StatusAset.DIHAPUS:
            raise BusinessRuleError("Aset yang sudah dihapus tidak dapat dimutasi")
        if aset.status == StatusAset.MUTASI:
            raise AssetInMutationError(data.aset_id)

        # Validate no pending mutation
        await self._validate_no_pending_mutation(data.aset_id)

        # Validate ruangan tujuan
        await self._validate_ruangan_exists(data.ruangan_tujuan_id)

        # Validate ruangan berbeda
        if aset.ruangan_id == data.ruangan_tujuan_id:
            raise SameRoomMutationError(data.ruangan_tujuan_id)

        # Validate alasan
        self._validate_alasan(data.alasan)

        # Create mutation record
        mutasi = RiwayatMutasi(
            aset_id=data.aset_id,
            ruangan_asal_id=aset.ruangan_id,
            ruangan_tujuan_id=data.ruangan_tujuan_id,
            user_id=user_id,
            tanggal_mutasi=data.tanggal_mutasi,
            alasan=data.alasan,
            kondisi_saat_mutasi=data.kondisi_saat_mutasi,
            status_mutasi=StatusMutasi.DALAM_PROSES,
            mulai_mutasi=datetime.now(UTC),
        )

        created = await self.repository.create(mutasi)

        # Update aset status to MUTASI
        await self._aset_repo.update(
            data.aset_id,
            {"status": StatusAset.MUTASI, "updated_by": user_id},
        )

        await self.commit()

        self.log_info(f"Mutation initiated: id={created.id}, aset={data.aset_id}")
        return created

    async def complete_mutation(
        self, mutasi_id: str, request: MutasiCompleteRequest | None, user_id: str
    ) -> RiwayatMutasi:
        """Selesaikan mutasi.

        Args:
            mutasi_id: UUID mutasi.
            request: MutasiCompleteRequest dengan catatan (optional).
            user_id: UUID user yang menyelesaikan.

        Returns:
            RiwayatMutasi yang diupdate.

        Raises:
            MutationNotFoundError: Jika mutasi tidak ditemukan.
            BusinessRuleError: Jika mutasi tidak dalam status DALAM_PROSES.
        """
        self.log_info(f"Completing mutation: {mutasi_id}")

        # Get mutation
        mutasi = await self.repository.get_by_id(mutasi_id)
        if not mutasi:
            raise MutationNotFoundError(mutasi_id)

        # Check status
        if mutasi.status_mutasi != StatusMutasi.DALAM_PROSES:
            raise BusinessRuleError(
                f"Mutasi dengan status '{mutasi.status_mutasi.value}' tidak dapat diselesaikan"
            )

        # Complete mutation
        completed = await self.repository.complete_mutation(mutasi_id)
        if not completed:
            raise MutationNotFoundError(mutasi_id)

        # Update aset: move to new room and set status to AKTIF
        await self._aset_repo.update(
            mutasi.aset_id,
            {
                "ruangan_id": mutasi.ruangan_tujuan_id,
                "status": StatusAset.AKTIF,
                "updated_by": user_id,
            },
        )

        await self.commit()

        self.log_info(f"Mutation completed: id={mutasi_id}")
        return completed

    async def cancel_mutation(
        self, mutasi_id: str, request: MutasiCancelRequest, user_id: str
    ) -> RiwayatMutasi:
        """Batalkan mutasi.

        Args:
            mutasi_id: UUID mutasi.
            request: MutasiCancelRequest dengan alasan pembatalan.
            user_id: UUID user yang membatalkan.

        Returns:
            RiwayatMutasi yang diupdate.

        Raises:
            MutationNotFoundError: Jika mutasi tidak ditemukan.
            BusinessRuleError: Jika mutasi tidak dalam status DALAM_PROSES.
            MutationReasonTooShortError: Jika alasan terlalu pendek.
        """
        self.log_info(f"Cancelling mutation: {mutasi_id}")

        # Get mutation
        mutasi = await self.repository.get_by_id(mutasi_id)
        if not mutasi:
            raise MutationNotFoundError(mutasi_id)

        # Check status
        if mutasi.status_mutasi != StatusMutasi.DALAM_PROSES:
            raise BusinessRuleError(
                f"Mutasi dengan status '{mutasi.status_mutasi.value}' tidak dapat dibatalkan"
            )

        # Validate alasan
        self._validate_alasan(request.alasan_pembatalan)

        # Cancel mutation
        cancelled = await self.repository.cancel_mutation(
            mutasi_id, request.alasan_pembatalan
        )
        if not cancelled:
            raise MutationNotFoundError(mutasi_id)

        # Revert aset status to AKTIF (stay in original room)
        await self._aset_repo.update(
            mutasi.aset_id,
            {"status": StatusAset.AKTIF, "updated_by": user_id},
        )

        await self.commit()

        self.log_info(f"Mutation cancelled: id={mutasi_id}")
        return cancelled

    async def get_mutation_by_id(self, mutasi_id: str) -> RiwayatMutasi:
        """Get mutasi by ID.

        Args:
            mutasi_id: UUID mutasi.

        Returns:
            RiwayatMutasi jika ditemukan.

        Raises:
            MutationNotFoundError: Jika mutasi tidak ditemukan.
        """
        mutasi = await self.repository.get_by_id(mutasi_id)
        if not mutasi:
            raise MutationNotFoundError(mutasi_id)
        return mutasi

    # =========================================================================
    # Search Operations
    # =========================================================================

    async def get_mutation_history(
        self, params: MutasiSearchParams
    ) -> PaginatedResponse[MutasiResponse]:
        """Get history mutasi dengan filters.

        Args:
            params: MutasiSearchParams dengan filter criteria.

        Returns:
            PaginatedResponse dengan list MutasiResponse.
        """
        self.log_debug(f"Getting mutation history: status={params.status_mutasi}")

        # Calculate pagination
        skip = (params.page - 1) * params.page_size
        limit = params.page_size

        # Convert datetime if needed
        tanggal_dari = (
            datetime.combine(params.tanggal_dari, datetime.min.time())
            if params.tanggal_dari
            else None
        )
        tanggal_sampai = (
            datetime.combine(params.tanggal_sampai, datetime.max.time())
            if params.tanggal_sampai
            else None
        )

        # Get mutations
        mutations = await self.repository.get_mutation_history(
            aset_id=params.aset_id,
            ruangan_asal_id=params.ruangan_id,
            ruangan_tujuan_id=params.ruangan_id,
            status=params.status_mutasi,
            tanggal_dari=tanggal_dari,
            tanggal_sampai=tanggal_sampai,
            skip=skip,
            limit=limit,
        )

        # Count total (simplified - would need separate count method)
        total = len(mutations)
        if len(mutations) == limit:
            # Might have more, estimate
            total = skip + limit + 1

        # Convert to response
        items = [self._to_response(m) for m in mutations]

        return PaginatedResponse(
            data=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size,
        )

    async def get_pending_mutations(self) -> list[RiwayatMutasi]:
        """Get semua pending mutations.

        Returns:
            List of pending mutations.
        """
        return await self.repository.get_pending_mutations()

    # =========================================================================
    # Background Tasks
    # =========================================================================

    async def cancel_expired_mutations(self) -> int:
        """Auto-cancel mutasi yang expired (> 7 hari).

        Returns:
            Jumlah mutasi yang di-cancel.
        """
        self.log_info("Checking for expired mutations...")

        expired = await self.repository.get_expired_mutations(MUTATION_EXPIRY_DAYS)

        cancelled_count = 0
        for mutasi in expired:
            try:
                await self.repository.cancel_mutation(
                    str(mutasi.id),
                    f"Auto-cancelled: mutasi tidak diselesaikan dalam {MUTATION_EXPIRY_DAYS} hari",
                )

                # Revert aset status
                await self._aset_repo.update(
                    mutasi.aset_id,
                    {"status": StatusAset.AKTIF, "updated_by": "SYSTEM"},
                )

                cancelled_count += 1
                self.log_info(f"Auto-cancelled expired mutation: {mutasi.id}")

            except Exception as e:
                self.log_error(f"Failed to cancel mutation {mutasi.id}: {e}")

        if cancelled_count > 0:
            await self.commit()

        self.log_info(f"Expired mutations cancelled: {cancelled_count}")
        return cancelled_count

    def _to_response(self, mutasi: RiwayatMutasi) -> MutasiResponse:
        """Convert RiwayatMutasi model to MutasiResponse schema.

        Args:
            mutasi: RiwayatMutasi model instance.

        Returns:
            MutasiResponse schema.
        """
        return MutasiResponse(
            id=str(mutasi.id),
            aset_id=str(mutasi.aset_id),
            ruangan_asal_id=str(mutasi.ruangan_asal_id)
            if mutasi.ruangan_asal_id
            else "",
            ruangan_tujuan_id=str(mutasi.ruangan_tujuan_id),
            user_id=str(mutasi.user_id),
            tanggal_mutasi=mutasi.tanggal_mutasi,
            alasan=mutasi.alasan,
            kondisi_saat_mutasi=mutasi.kondisi_saat_mutasi,
            status_mutasi=mutasi.status_mutasi,
            mulai_mutasi=mutasi.mulai_mutasi,
            selesai_mutasi=mutasi.selesai_mutasi,
            alasan_pembatalan=mutasi.alasan_pembatalan,
        )
