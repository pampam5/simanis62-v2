"""KIB Repository untuk SIMANIS62 V2.

Module ini menyediakan KibRepository untuk query KIB dengan join ke extension tables.
Khusus untuk KIB B dengan format 18 kolom BPAD DKI Jakarta.
"""

from datetime import date
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aset import Aset, KategoriKIB, StatusAset
from app.models.aset_kib import AsetKIBB


class KibRepository:
    """Repository untuk query KIB dengan join ke extension tables.

    Menyediakan:
    - get_kib_b_data: Query aset KIB B dengan join ke aset_kib_b
    - get_kib_b_export_data: Query untuk export Excel 18 kolom
    - count_kib_b: Count total aset KIB B

    Example:
        ```python
        repo = KibRepository(session)
        data = await repo.get_kib_b_data(ruangan_id="xxx")
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize KibRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        self.session = session

    async def get_kib_b_data(
        self,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
        kondisi: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Query aset KIB B dengan join ke aset_kib_b.

        Hanya mengembalikan aset dengan status "Aktif".

        Args:
            ruangan_id: Filter berdasarkan ruangan (optional).
            tahun_perolehan: Filter berdasarkan tahun (optional).
            kondisi: Filter berdasarkan kondisi (optional).
            skip: Offset untuk pagination.
            limit: Limit untuk pagination.

        Returns:
            List of dict dengan data KIB B lengkap.
        """
        # Build query dengan join
        query = (
            select(Aset, AsetKIBB)
            .outerjoin(AsetKIBB, Aset.id == AsetKIBB.aset_id)
            .where(Aset.kategori_kib == KategoriKIB.B)
            .where(Aset.status == StatusAset.AKTIF)
        )

        # Apply filters
        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)
        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)
        if kondisi:
            query = query.where(Aset.kondisi == kondisi)

        # Order and paginate
        query = query.order_by(Aset.nomor_register).offset(skip).limit(limit)

        result = await self.session.execute(query)
        rows = result.all()

        # Convert to list of dicts
        data = []
        for aset, kib_b in rows:
            item = self._to_kib_b_dict(aset, kib_b)
            data.append(item)

        return data

    async def get_kib_b_export_data(
        self,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
    ) -> list[dict[str, Any]]:
        """Query data KIB B untuk export Excel 18 kolom BPAD DKI Jakarta.

        Hanya mengembalikan aset dengan status "Aktif".
        Tidak ada pagination - ambil semua data.

        Args:
            ruangan_id: Filter berdasarkan ruangan (optional).
            tahun_perolehan: Filter berdasarkan tahun (optional).

        Returns:
            List of dict dengan format 18 kolom BPAD DKI Jakarta.
        """
        # Build query dengan join
        query = (
            select(Aset, AsetKIBB)
            .outerjoin(AsetKIBB, Aset.id == AsetKIBB.aset_id)
            .where(Aset.kategori_kib == KategoriKIB.B)
            .where(Aset.status == StatusAset.AKTIF)
        )

        # Apply filters
        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)
        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)

        # Order by nomor_register
        query = query.order_by(Aset.nomor_register)

        result = await self.session.execute(query)
        rows = result.all()

        # Convert to export format (18 kolom)
        data = []
        for idx, (aset, kib_b) in enumerate(rows, 1):
            item = self._to_export_row(idx, aset, kib_b)
            data.append(item)

        return data

    async def count_kib_b(
        self,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
        kondisi: str | None = None,
    ) -> int:
        """Count total aset KIB B.

        Args:
            ruangan_id: Filter berdasarkan ruangan (optional).
            tahun_perolehan: Filter berdasarkan tahun (optional).
            kondisi: Filter berdasarkan kondisi (optional).

        Returns:
            Total count.
        """
        query = (
            select(func.count(Aset.id))
            .where(Aset.kategori_kib == KategoriKIB.B)
            .where(Aset.status == StatusAset.AKTIF)
        )

        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)
        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)
        if kondisi:
            query = query.where(Aset.kondisi == kondisi)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_total_nilai_kib_b(
        self,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
    ) -> int:
        """Get total nilai aset KIB B.

        Args:
            ruangan_id: Filter berdasarkan ruangan (optional).
            tahun_perolehan: Filter berdasarkan tahun (optional).

        Returns:
            Total nilai dalam Rupiah.
        """
        query = (
            select(func.sum(Aset.harga))
            .where(Aset.kategori_kib == KategoriKIB.B)
            .where(Aset.status == StatusAset.AKTIF)
        )

        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)
        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)

        result = await self.session.execute(query)
        return result.scalar() or 0

    def _to_kib_b_dict(self, aset: Aset, kib_b: AsetKIBB | None) -> dict[str, Any]:
        """Convert Aset + AsetKIBB to dict.

        Args:
            aset: Aset model.
            kib_b: AsetKIBB model (optional).

        Returns:
            Dict dengan data KIB B lengkap.
        """
        # Map kondisi ke kode BPAD
        kondisi_map = {
            "Baik": "B",
            "Kurang Baik": "KB",
            "Rusak Berat": "RB",
        }

        return {
            "id": str(aset.id),
            "kode_barang": aset.kode_barang,
            "nama_barang": aset.nama_barang,
            "nomor_register": aset.nomor_register,
            "tahun_perolehan": aset.tahun_perolehan,
            "tanggal_perolehan": self._format_date(aset.tanggal_perolehan),
            "asal_usul": aset.asal_usul.value if aset.asal_usul else "",
            "harga": aset.harga,
            "kondisi": kondisi_map.get(aset.kondisi.value, "") if aset.kondisi else "",
            "keterangan": aset.keterangan or "",
            # KIB B specific fields
            "satuan": kib_b.satuan if kib_b else "",
            "ukuran_cc": kib_b.ukuran_cc if kib_b else "",
            "bahan": kib_b.bahan if kib_b else "",
            "merk": kib_b.merk if kib_b else "",
            "tipe": kib_b.tipe if kib_b else "",
            "tanggal_dokumen": self._format_date(kib_b.tanggal_dokumen)
            if kib_b
            else "",
            "nomor_rangka": kib_b.nomor_rangka if kib_b else "",
            "nomor_mesin": kib_b.nomor_mesin if kib_b else "",
            "nomor_polisi": kib_b.nomor_polisi if kib_b else "",
            "kapitalisasi": kib_b.kapitalisasi if kib_b else 0,
            "total_harga": kib_b.total_harga if kib_b else aset.harga,
        }

    def _to_export_row(
        self, no: int, aset: Aset, kib_b: AsetKIBB | None
    ) -> dict[str, Any]:
        """Convert to export row format (18 kolom BPAD DKI Jakarta).

        Format kolom:
        1. NO
        2. KODE BARANG
        3. NAMA BARANG
        4. NO. REGISTER
        5. UKU-RAN
        6. SATU-AN
        7. TAHUN PEROLEHAN
        8. BA-HAN
        9. MEREK
        10. TYPE
        11. TGL. BPKB/TGL. DOK.
        12. NO. CHASIS/NO. RANGKA
        13. NO. MESIN/NO. PABRIK
        14. NOMOR POLISI
        15. KONDISI (B/KB/RB)
        16. HARGA (Rp.) - Rupiah penuh
        17. KAPITALISASI (Rp.)
        18. TOTAL (Rp.)

        Args:
            no: Nomor urut.
            aset: Aset model.
            kib_b: AsetKIBB model (optional).

        Returns:
            Dict dengan format 18 kolom.
        """
        # Map kondisi ke kode BPAD
        kondisi_map = {
            "Baik": "B",
            "Kurang Baik": "KB",
            "Rusak Berat": "RB",
        }

        return {
            "no": no,
            "kode_barang": aset.kode_barang,
            "nama_barang": aset.nama_barang,
            "nomor_register": str(aset.nomor_register).zfill(3),
            "ukuran_cc": kib_b.ukuran_cc if kib_b and kib_b.ukuran_cc else "-",
            "satuan": kib_b.satuan if kib_b else "Unit",
            "tahun_perolehan": aset.tahun_perolehan,
            "bahan": kib_b.bahan if kib_b and kib_b.bahan else "-",
            "merk": kib_b.merk if kib_b and kib_b.merk else "-",
            "tipe": kib_b.tipe if kib_b and kib_b.tipe else "-",
            "tanggal_dokumen": self._format_date(kib_b.tanggal_dokumen)
            if kib_b and kib_b.tanggal_dokumen
            else "-",
            "nomor_rangka": kib_b.nomor_rangka if kib_b and kib_b.nomor_rangka else "-",
            "nomor_mesin": kib_b.nomor_mesin if kib_b and kib_b.nomor_mesin else "-",
            "nomor_polisi": kib_b.nomor_polisi if kib_b and kib_b.nomor_polisi else "-",
            "kondisi": kondisi_map.get(aset.kondisi.value, "B")
            if aset.kondisi
            else "B",
            "harga": aset.harga,  # Rupiah penuh
            "kapitalisasi": kib_b.kapitalisasi
            if kib_b and kib_b.kapitalisasi
            else aset.harga,
            "total_harga": kib_b.total_harga
            if kib_b and kib_b.total_harga
            else aset.harga,
        }

    def _format_date(self, d: date | None) -> str:
        """Format date ke DD/MM/YYYY.

        Args:
            d: Date object.

        Returns:
            Formatted string atau empty string.
        """
        if d is None:
            return ""
        return d.strftime("%d/%m/%Y")
