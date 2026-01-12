"""Unit tests untuk AsetRepository.

Tests untuk:
- CRUD operations
- Search dengan filters
- Pagination
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.models.aset import AsalUsul, Aset, KategoriKIB, Kondisi, StatusAset
from app.repositories.aset_repository import AsetRepository


@pytest.mark.asyncio
async def test_create_aset(db_session):
    """Test create aset."""
    repo = AsetRepository(db_session)

    aset = Aset(
        id=uuid4(),
        nama_barang="Laptop Dell",
        kode_barang="02.06.01.0001",
        nomor_register=1,  # int, not string
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,  # Use enum
        harga=15_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),  # UUID object
        created_by=uuid4(),  # UUID object
        created_at=datetime.now(UTC),
    )

    created = await repo.create(aset)
    await db_session.commit()

    assert created.id is not None
    assert created.nama_barang == "Laptop Dell"
    assert created.kode_barang == "02.06.01.0001"


@pytest.mark.asyncio
async def test_get_by_id(db_session):
    """Test get aset by ID."""
    repo = AsetRepository(db_session)

    # Create aset first
    aset_id = uuid4()
    aset = Aset(
        id=aset_id,
        nama_barang="Laptop HP",
        kode_barang="02.06.01.0002",
        nomor_register=2,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=12_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )
    db_session.add(aset)
    await db_session.commit()

    # Get by ID
    result = await repo.get_by_id(aset_id)

    assert result is not None
    assert result.id == aset_id
    assert result.nama_barang == "Laptop HP"


@pytest.mark.asyncio
async def test_get_by_id_not_found(db_session):
    """Test get aset by ID - not found."""
    repo = AsetRepository(db_session)

    result = await repo.get_by_id(uuid4())  # UUID object

    assert result is None


@pytest.mark.asyncio
async def test_get_by_kode_barang(db_session):
    """Test get aset by kode_barang."""
    repo = AsetRepository(db_session)

    # Create aset first
    aset = Aset(
        id=uuid4(),
        nama_barang="Printer Canon",
        kode_barang="02.06.02.0001",
        nomor_register=3,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=5_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )
    db_session.add(aset)
    await db_session.commit()

    # Get by kode_barang
    result = await repo.get_by_kode_barang("02.06.02.0001")

    assert result is not None
    assert result.kode_barang == "02.06.02.0001"
    assert result.nama_barang == "Printer Canon"


@pytest.mark.asyncio
async def test_search_by_keyword(db_session):
    """Test search aset by keyword."""
    repo = AsetRepository(db_session)

    # Create multiple asets
    asets = [
        Aset(
            id=uuid4(),
            nama_barang="Laptop Lenovo ThinkPad",
            kode_barang="02.06.01.0010",
            nomor_register=10,
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,
            harga=18_000_000,
            kondisi=Kondisi.BAIK,
            status=StatusAset.AKTIF,
            ruangan_id=uuid4(),
            created_by=uuid4(),
            created_at=datetime.now(UTC),
        ),
        Aset(
            id=uuid4(),
            nama_barang="Meja Kerja",
            kode_barang="02.06.03.0001",
            nomor_register=11,
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,
            harga=2_000_000,
            kondisi=Kondisi.BAIK,
            status=StatusAset.AKTIF,
            ruangan_id=uuid4(),
            created_by=uuid4(),
            created_at=datetime.now(UTC),
        ),
    ]

    for aset in asets:
        db_session.add(aset)
    await db_session.commit()

    # Search by keyword
    results = await repo.search(keyword="Laptop")

    assert len(results) >= 1
    assert any("Laptop" in a.nama_barang for a in results)


@pytest.mark.asyncio
async def test_search_by_kategori_kib(db_session):
    """Test search aset by kategori_kib."""
    repo = AsetRepository(db_session)

    # Create asets with different kategori
    aset_b = Aset(
        id=uuid4(),
        nama_barang="Monitor Samsung",
        kode_barang="02.06.01.0020",
        nomor_register=20,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=3_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )
    db_session.add(aset_b)
    await db_session.commit()

    # Search by kategori
    results = await repo.search(kategori_kib=KategoriKIB.B)

    assert len(results) >= 1
    assert all(a.kategori_kib == KategoriKIB.B for a in results)


@pytest.mark.asyncio
async def test_search_pagination(db_session):
    """Test search dengan pagination."""
    repo = AsetRepository(db_session)

    # Create multiple asets
    for i in range(5):
        aset = Aset(
            id=uuid4(),
            nama_barang=f"Aset Pagination Test {i}",
            kode_barang=f"02.06.01.{100+i:04d}",
            nomor_register=100 + i,
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,
            harga=1_000_000,
            kondisi=Kondisi.BAIK,
            status=StatusAset.AKTIF,
            ruangan_id=uuid4(),
            created_by=uuid4(),
            created_at=datetime.now(UTC),
        )
        db_session.add(aset)
    await db_session.commit()

    # Test pagination
    page1 = await repo.search(skip=0, limit=2)
    page2 = await repo.search(skip=2, limit=2)

    assert len(page1) <= 2
    assert len(page2) <= 2


@pytest.mark.asyncio
async def test_soft_delete(db_session):
    """Test soft delete aset."""
    repo = AsetRepository(db_session)

    # Create aset
    aset_id = uuid4()
    aset = Aset(
        id=aset_id,
        nama_barang="Aset To Delete",
        kode_barang="02.06.01.9999",
        nomor_register=9999,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=1_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )
    db_session.add(aset)
    await db_session.commit()

    # Soft delete
    user_id = uuid4()  # UUID object
    deleted = await repo.soft_delete(
        aset_id, "Aset rusak dan tidak dapat diperbaiki", user_id
    )
    await db_session.commit()

    assert deleted is not None
    assert deleted.status == StatusAset.DIHAPUS
    assert deleted.deleted_at is not None
    assert deleted.deleted_by == user_id


@pytest.mark.asyncio
async def test_search_exclude_deleted(db_session):
    """Test search exclude deleted asets."""
    repo = AsetRepository(db_session)

    # Create active and deleted asets
    active_aset = Aset(
        id=uuid4(),
        nama_barang="Active Aset",
        kode_barang="02.06.01.8001",
        nomor_register=8001,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=1_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )

    deleted_aset = Aset(
        id=uuid4(),
        nama_barang="Deleted Aset",
        kode_barang="02.06.01.8002",
        nomor_register=8002,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=1_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.DIHAPUS,
        deleted_at=datetime.now(UTC),
        deleted_by=uuid4(),  # UUID object
        ruangan_id=uuid4(),
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )

    db_session.add(active_aset)
    db_session.add(deleted_aset)
    await db_session.commit()

    # Search without deleted
    results = await repo.search(include_deleted=False)

    assert all(a.status != StatusAset.DIHAPUS for a in results)
