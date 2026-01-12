"""Unit tests untuk MutasiService.

Tests untuk:
- Initiate mutation
- Complete mutation
- Cancel mutation
- Business logic validation
"""

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    AssetInMutationError,
    AssetNotFoundError,
    BusinessRuleError,
    MutationNotFoundError,
    MutationReasonTooShortError,
    RuanganNotFoundError,
    SameRoomMutationError,
)
from app.models.aset import Aset, Kondisi, StatusAset
from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.schemas.mutasi import MutasiCancelRequest, MutasiCreate
from app.services.mutasi_service import MutasiService


class TestMutasiServiceValidation:
    """Tests untuk validation methods."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = MutasiService(self.mock_session)

    def test_validate_alasan_valid(self):
        """Test valid alasan (>= 10 chars)."""
        self.service._validate_alasan("Alasan yang cukup panjang")

    def test_validate_alasan_invalid(self):
        """Test invalid alasan (< 10 chars)."""
        with pytest.raises(MutationReasonTooShortError):
            self.service._validate_alasan("Pendek")


class TestMutasiServiceInitiate:
    """Tests untuk initiate mutation."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = MutasiService(self.mock_session)

    @pytest.mark.asyncio
    async def test_initiate_mutation_success(self):
        """Test initiate mutation dengan data valid."""
        user_id = str(uuid4())
        aset_id = str(uuid4())
        ruangan_asal_id = str(uuid4())
        ruangan_tujuan_id = str(uuid4())

        aset = Aset(
            id=aset_id,
            nama_barang="Laptop",
            status=StatusAset.AKTIF,
            ruangan_id=ruangan_asal_id,
        )

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=ruangan_tujuan_id,
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru untuk keperluan operasional",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        # Mock repository methods
        self.service._aset_repo.get_by_id = AsyncMock(return_value=aset)
        self.service._ruangan_repo.exists = AsyncMock(return_value=True)
        self.service.repository.has_pending_mutation = AsyncMock(return_value=False)
        self.service.repository.create = AsyncMock(
            return_value=RiwayatMutasi(
                id=uuid4(),
                aset_id=aset_id,
                ruangan_asal_id=ruangan_asal_id,
                ruangan_tujuan_id=ruangan_tujuan_id,
                user_id=user_id,
                tanggal_mutasi=data.tanggal_mutasi,
                alasan=data.alasan,
                kondisi_saat_mutasi=data.kondisi_saat_mutasi,
                status_mutasi=StatusMutasi.DALAM_PROSES,
                mulai_mutasi=datetime.now(UTC),
            )
        )
        self.service._aset_repo.update = AsyncMock()
        self.service.commit = AsyncMock()

        result = await self.service.initiate_mutation(data, user_id)

        assert result.status_mutasi == StatusMutasi.DALAM_PROSES
        assert result.aset_id == aset_id

    @pytest.mark.asyncio
    async def test_initiate_mutation_asset_not_found(self):
        """Test initiate mutation - aset tidak ditemukan."""
        user_id = str(uuid4())
        aset_id = str(uuid4())

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=str(uuid4()),
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        self.service._aset_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(AssetNotFoundError):
            await self.service.initiate_mutation(data, user_id)

    @pytest.mark.asyncio
    async def test_initiate_mutation_asset_deleted(self):
        """Test initiate mutation - aset sudah dihapus."""
        user_id = str(uuid4())
        aset_id = str(uuid4())

        aset = Aset(
            id=aset_id,
            nama_barang="Laptop",
            status=StatusAset.DIHAPUS,
        )

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=str(uuid4()),
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        self.service._aset_repo.get_by_id = AsyncMock(return_value=aset)

        with pytest.raises(BusinessRuleError):
            await self.service.initiate_mutation(data, user_id)

    @pytest.mark.asyncio
    async def test_initiate_mutation_asset_in_mutation(self):
        """Test initiate mutation - aset sedang dalam mutasi."""
        user_id = str(uuid4())
        aset_id = str(uuid4())

        aset = Aset(
            id=aset_id,
            nama_barang="Laptop",
            status=StatusAset.MUTASI,
        )

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=str(uuid4()),
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        self.service._aset_repo.get_by_id = AsyncMock(return_value=aset)

        with pytest.raises(AssetInMutationError):
            await self.service.initiate_mutation(data, user_id)

    @pytest.mark.asyncio
    async def test_initiate_mutation_same_room(self):
        """Test initiate mutation - ruangan tujuan sama dengan asal."""
        user_id = str(uuid4())
        aset_id = str(uuid4())
        ruangan_id = str(uuid4())

        aset = Aset(
            id=aset_id,
            nama_barang="Laptop",
            status=StatusAset.AKTIF,
            ruangan_id=ruangan_id,
        )

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=ruangan_id,  # Same as current
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        self.service._aset_repo.get_by_id = AsyncMock(return_value=aset)
        self.service._ruangan_repo.exists = AsyncMock(return_value=True)
        self.service.repository.has_pending_mutation = AsyncMock(return_value=False)

        with pytest.raises(SameRoomMutationError):
            await self.service.initiate_mutation(data, user_id)

    @pytest.mark.asyncio
    async def test_initiate_mutation_ruangan_not_found(self):
        """Test initiate mutation - ruangan tujuan tidak ditemukan."""
        user_id = str(uuid4())
        aset_id = str(uuid4())

        aset = Aset(
            id=aset_id,
            nama_barang="Laptop",
            status=StatusAset.AKTIF,
            ruangan_id=str(uuid4()),
        )

        data = MutasiCreate(
            aset_id=aset_id,
            ruangan_tujuan_id=str(uuid4()),
            tanggal_mutasi=date.today(),
            alasan="Pemindahan ke ruang baru",
            kondisi_saat_mutasi=Kondisi.BAIK,
        )

        self.service._aset_repo.get_by_id = AsyncMock(return_value=aset)
        self.service.repository.has_pending_mutation = AsyncMock(return_value=False)
        self.service._ruangan_repo.exists = AsyncMock(return_value=False)

        with pytest.raises(RuanganNotFoundError):
            await self.service.initiate_mutation(data, user_id)


class TestMutasiServiceComplete:
    """Tests untuk complete mutation."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = MutasiService(self.mock_session)

    @pytest.mark.asyncio
    async def test_complete_mutation_success(self):
        """Test complete mutation dengan data valid."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())
        aset_id = str(uuid4())
        ruangan_tujuan_id = str(uuid4())

        mutasi = RiwayatMutasi(
            id=mutasi_id,
            aset_id=aset_id,
            ruangan_asal_id=str(uuid4()),
            ruangan_tujuan_id=ruangan_tujuan_id,
            user_id=user_id,
            status_mutasi=StatusMutasi.DALAM_PROSES,
        )

        self.service.repository.get_by_id = AsyncMock(return_value=mutasi)
        self.service.repository.complete_mutation = AsyncMock(return_value=mutasi)
        self.service._aset_repo.update = AsyncMock()
        self.service.commit = AsyncMock()

        result = await self.service.complete_mutation(mutasi_id, None, user_id)

        assert result is not None
        self.service._aset_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_mutation_not_found(self):
        """Test complete mutation - mutasi tidak ditemukan."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())

        self.service.repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(MutationNotFoundError):
            await self.service.complete_mutation(mutasi_id, None, user_id)

    @pytest.mark.asyncio
    async def test_complete_mutation_wrong_status(self):
        """Test complete mutation - status bukan DALAM_PROSES."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())

        mutasi = RiwayatMutasi(
            id=mutasi_id,
            aset_id=str(uuid4()),
            ruangan_tujuan_id=str(uuid4()),
            user_id=user_id,
            status_mutasi=StatusMutasi.SELESAI,  # Already completed
        )

        self.service.repository.get_by_id = AsyncMock(return_value=mutasi)

        with pytest.raises(BusinessRuleError):
            await self.service.complete_mutation(mutasi_id, None, user_id)


class TestMutasiServiceCancel:
    """Tests untuk cancel mutation."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = MutasiService(self.mock_session)

    @pytest.mark.asyncio
    async def test_cancel_mutation_success(self):
        """Test cancel mutation dengan data valid."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())
        aset_id = str(uuid4())

        mutasi = RiwayatMutasi(
            id=mutasi_id,
            aset_id=aset_id,
            ruangan_asal_id=str(uuid4()),
            ruangan_tujuan_id=str(uuid4()),
            user_id=user_id,
            status_mutasi=StatusMutasi.DALAM_PROSES,
        )

        request = MutasiCancelRequest(
            alasan_pembatalan="Pembatalan karena perubahan keputusan manajemen"
        )

        self.service.repository.get_by_id = AsyncMock(return_value=mutasi)
        self.service.repository.cancel_mutation = AsyncMock(return_value=mutasi)
        self.service._aset_repo.update = AsyncMock()
        self.service.commit = AsyncMock()

        result = await self.service.cancel_mutation(mutasi_id, request, user_id)

        assert result is not None
        self.service._aset_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_mutation_not_found(self):
        """Test cancel mutation - mutasi tidak ditemukan."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())

        request = MutasiCancelRequest(
            alasan_pembatalan="Pembatalan karena perubahan keputusan"
        )

        self.service.repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(MutationNotFoundError):
            await self.service.cancel_mutation(mutasi_id, request, user_id)

    @pytest.mark.asyncio
    async def test_cancel_mutation_wrong_status(self):
        """Test cancel mutation - status bukan DALAM_PROSES."""
        user_id = str(uuid4())
        mutasi_id = str(uuid4())

        mutasi = RiwayatMutasi(
            id=mutasi_id,
            aset_id=str(uuid4()),
            ruangan_tujuan_id=str(uuid4()),
            user_id=user_id,
            status_mutasi=StatusMutasi.DIBATALKAN,  # Already cancelled
        )

        request = MutasiCancelRequest(
            alasan_pembatalan="Pembatalan karena perubahan keputusan"
        )

        self.service.repository.get_by_id = AsyncMock(return_value=mutasi)

        with pytest.raises(BusinessRuleError):
            await self.service.cancel_mutation(mutasi_id, request, user_id)

    @pytest.mark.asyncio
    async def test_cancel_mutation_short_reason(self):
        """Test cancel mutation - alasan terlalu pendek (caught by Pydantic)."""
        # Note: Pydantic validation catches this before service layer
        # This test verifies that Pydantic schema validation works
        with pytest.raises(Exception):  # ValidationError from Pydantic
            MutasiCancelRequest(alasan_pembatalan="Pendek")
