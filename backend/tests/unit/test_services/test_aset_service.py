"""Unit tests untuk AsetService.

Tests untuk:
- Validation methods
- CRUD operations
- Search functionality
"""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    AssetInMutationError,
    AssetNotFoundError,
    DeleteReasonTooShortError,
    DuplicateKodeBarangError,
    InvalidHargaError,
    InvalidKodeBarangFormatError,
    InvalidTahunPerolehanError,
)
from app.models.aset import Aset, KategoriKIB, Kondisi, StatusAset
from app.schemas.aset import AsetCreate, AsetDeleteRequest, AsetUpdate
from app.services.aset_service import AsetService


class TestAsetServiceValidation:
    """Tests untuk validation methods."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = AsetService(self.mock_session)

    def test_validate_kode_barang_format_valid(self):
        """Test valid kode_barang format."""
        # Should not raise
        self.service._validate_kode_barang_format("02.06.01.0001")
        self.service._validate_kode_barang_format("01.01.01.0001")
        self.service._validate_kode_barang_format("99.99.99.9999")

    def test_validate_kode_barang_format_invalid(self):
        """Test invalid kode_barang format."""
        invalid_codes = [
            "02060100001",  # No dots
            "02.06.01.001",  # Wrong last segment length
            "2.06.01.0001",  # Wrong first segment length
            "02.6.01.0001",  # Wrong second segment length
            "02.06.1.0001",  # Wrong third segment length
            "AB.CD.EF.GHIJ",  # Letters instead of numbers
            "",  # Empty
            "02.06.01",  # Missing segment
        ]
        for code in invalid_codes:
            with pytest.raises(InvalidKodeBarangFormatError):
                self.service._validate_kode_barang_format(code)

    def test_validate_tahun_perolehan_valid(self):
        """Test valid tahun_perolehan."""
        self.service._validate_tahun_perolehan(1900)
        self.service._validate_tahun_perolehan(2000)
        self.service._validate_tahun_perolehan(2024)

    def test_validate_tahun_perolehan_invalid(self):
        """Test invalid tahun_perolehan."""
        with pytest.raises(InvalidTahunPerolehanError):
            self.service._validate_tahun_perolehan(1899)
        with pytest.raises(InvalidTahunPerolehanError):
            self.service._validate_tahun_perolehan(2100)

    def test_validate_harga_valid(self):
        """Test valid harga."""
        self.service._validate_harga(0)
        self.service._validate_harga(1)
        self.service._validate_harga(999_999_999_999)

    def test_validate_harga_invalid(self):
        """Test invalid harga."""
        with pytest.raises(InvalidHargaError):
            self.service._validate_harga(-1)
        with pytest.raises(InvalidHargaError):
            self.service._validate_harga(1_000_000_000_000)

    def test_validate_delete_reason_valid(self):
        """Test valid delete reason (>= 20 chars)."""
        self.service._validate_delete_reason(
            "Alasan penghapusan yang cukup panjang untuk validasi"
        )

    def test_validate_delete_reason_invalid(self):
        """Test invalid delete reason (< 20 chars)."""
        with pytest.raises(DeleteReasonTooShortError):
            self.service._validate_delete_reason("Terlalu pendek")


class TestAsetServiceCRUD:
    """Tests untuk CRUD operations."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = AsetService(self.mock_session)

    @pytest.mark.asyncio
    async def test_create_asset_success(self):
        """Test create asset dengan data valid."""
        user_id = str(uuid4())
        ruangan_id = str(uuid4())

        data = AsetCreate(
            nama_barang="Laptop Dell",
            kode_barang="02.06.01.0001",
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul="Pembelian",
            harga=15_000_000,
            kondisi=Kondisi.BAIK,
            ruangan_id=ruangan_id,
        )

        # Mock repository methods
        self.service.repository.get_by_kode_barang = AsyncMock(return_value=None)
        self.service.repository.get_next_nomor_register = AsyncMock(
            return_value="B/2024/0001"
        )
        self.service.repository.create = AsyncMock(
            return_value=Aset(
                id=uuid4(),
                nama_barang=data.nama_barang,
                kode_barang=data.kode_barang,
                nomor_register="B/2024/0001",
                kategori_kib=data.kategori_kib,
                tahun_perolehan=data.tahun_perolehan,
                asal_usul=data.asal_usul,
                harga=data.harga,
                kondisi=data.kondisi,
                status=StatusAset.AKTIF,
                ruangan_id=ruangan_id,
                created_by=user_id,
            )
        )
        self.service._ruangan_repo.exists = AsyncMock(return_value=True)
        self.service.commit = AsyncMock()

        result = await self.service.create_asset(data, user_id)

        assert result.nama_barang == data.nama_barang
        assert result.kode_barang == data.kode_barang
        assert result.status == StatusAset.AKTIF

    @pytest.mark.asyncio
    async def test_create_asset_duplicate_kode(self):
        """Test create asset dengan kode_barang duplikat."""
        user_id = str(uuid4())

        data = AsetCreate(
            nama_barang="Laptop Dell",
            kode_barang="02.06.01.0001",
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul="Pembelian",
            harga=15_000_000,
            kondisi=Kondisi.BAIK,
        )

        # Mock existing asset
        existing = Aset(id=uuid4(), kode_barang=data.kode_barang)
        self.service.repository.get_by_kode_barang = AsyncMock(return_value=existing)

        with pytest.raises(DuplicateKodeBarangError):
            await self.service.create_asset(data, user_id)

    @pytest.mark.asyncio
    async def test_get_asset_by_id_found(self):
        """Test get asset by ID - found."""
        aset_id = str(uuid4())
        expected = Aset(id=aset_id, nama_barang="Test")

        self.service.repository.get_by_id = AsyncMock(return_value=expected)

        result = await self.service.get_asset_by_id(aset_id)
        assert result.id == aset_id

    @pytest.mark.asyncio
    async def test_get_asset_by_id_not_found(self):
        """Test get asset by ID - not found."""
        aset_id = str(uuid4())
        self.service.repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(AssetNotFoundError):
            await self.service.get_asset_by_id(aset_id)

    @pytest.mark.asyncio
    async def test_update_asset_in_mutation(self):
        """Test update asset yang sedang dalam mutasi."""
        aset_id = str(uuid4())
        user_id = str(uuid4())

        existing = Aset(
            id=aset_id,
            nama_barang="Test",
            status=StatusAset.MUTASI,
        )
        self.service.repository.get_by_id = AsyncMock(return_value=existing)

        data = AsetUpdate(nama_barang="Updated")

        with pytest.raises(AssetInMutationError):
            await self.service.update_asset(aset_id, data, user_id)

    @pytest.mark.asyncio
    async def test_delete_asset_success(self):
        """Test soft delete asset."""
        aset_id = str(uuid4())
        user_id = str(uuid4())

        existing = Aset(
            id=aset_id,
            nama_barang="Test",
            status=StatusAset.AKTIF,
        )
        self.service.repository.get_by_id = AsyncMock(return_value=existing)
        self.service.repository.soft_delete = AsyncMock(return_value=existing)
        self.service.commit = AsyncMock()

        request = AsetDeleteRequest(
            alasan_penghapusan="Aset rusak berat dan tidak dapat diperbaiki lagi"
        )

        result = await self.service.delete_asset(aset_id, request, user_id)
        assert result is not None

    @pytest.mark.asyncio
    async def test_delete_asset_in_mutation(self):
        """Test delete asset yang sedang dalam mutasi."""
        aset_id = str(uuid4())
        user_id = str(uuid4())

        existing = Aset(
            id=aset_id,
            nama_barang="Test",
            status=StatusAset.MUTASI,
        )
        self.service.repository.get_by_id = AsyncMock(return_value=existing)

        request = AsetDeleteRequest(
            alasan_penghapusan="Aset rusak berat dan tidak dapat diperbaiki lagi"
        )

        with pytest.raises(AssetInMutationError):
            await self.service.delete_asset(aset_id, request, user_id)
