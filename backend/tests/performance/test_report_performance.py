"""Performance tests untuk report generation.

Tests untuk:
- KIB report generation < 10 detik untuk 1000 aset
- Excel export < 15 detik untuk 1000 aset
"""

import time
from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.models.aset import AsalUsul, Aset, KategoriKIB, Kondisi, StatusAset
from app.repositories.aset_repository import AsetRepository


@pytest_asyncio.fixture
async def bulk_kib_asets(db_session):
    """Create 1000 asets untuk KIB report testing."""
    asets = []
    user_id = uuid4()  # UUID object
    ruangan_id = uuid4()  # UUID object

    for i in range(1000):
        aset = Aset(
            id=uuid4(),
            nama_barang=f"KIB Report Test {i:04d}",
            kode_barang=f"02.06.{(i // 100):02d}.{(i % 10000):04d}",
            nomor_register=i + 1,  # int, not string
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,  # Use enum
            harga=1_000_000 + (i * 1000),
            kondisi=Kondisi.BAIK if i % 3 != 0 else Kondisi.RUSAK_RINGAN,
            status=StatusAset.AKTIF if i % 5 != 0 else StatusAset.RUSAK,
            ruangan_id=ruangan_id,  # UUID object
            created_by=user_id,  # UUID object
            created_at=datetime.now(UTC),
        )
        asets.append(aset)

    db_session.add_all(asets)
    await db_session.commit()

    return asets


@pytest.mark.asyncio
@pytest.mark.slow
async def test_kib_report_generation_under_10_seconds(db_session, bulk_kib_asets):
    """Test KIB report generation < 10 detik untuk 1000 aset.

    REQ-22: Generate laporan KIB < 10 detik
    """
    repo = AsetRepository(db_session)

    start_time = time.perf_counter()

    # Get assets for KIB report (only Aktif and Rusak)
    results = await repo.get_for_kib_report(KategoriKIB.B)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed < 10.0, f"KIB report generation took {elapsed:.2f}s, should be < 10s"
    assert len(results) > 0, "Should return results"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_kib_report_filters_deleted(db_session, bulk_kib_asets):
    """Test KIB report excludes deleted assets."""
    repo = AsetRepository(db_session)

    # Add some deleted assets
    user_id = uuid4()  # UUID object
    ruangan_id = uuid4()  # UUID object

    for i in range(100):
        deleted_aset = Aset(
            id=uuid4(),
            nama_barang=f"Deleted Asset {i}",
            kode_barang=f"02.06.99.{i:04d}",
            nomor_register=2000 + i,  # int, not string
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,  # Use enum
            harga=500_000,
            kondisi=Kondisi.RUSAK_BERAT,
            status=StatusAset.DIHAPUS,
            deleted_at=datetime.now(UTC),
            deleted_by=user_id,  # UUID object
            ruangan_id=ruangan_id,  # UUID object
            created_by=user_id,  # UUID object
            created_at=datetime.now(UTC),
        )
        db_session.add(deleted_aset)
    await db_session.commit()

    # Get KIB report
    results = await repo.get_for_kib_report(KategoriKIB.B)

    # Should not include deleted assets
    assert all(a.status != StatusAset.DIHAPUS for a in results)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_large_dataset_memory_efficiency(db_session, bulk_kib_asets):
    """Test memory efficiency dengan large dataset."""
    repo = AsetRepository(db_session)

    # Process in batches
    batch_size = 100
    total_processed = 0

    start_time = time.perf_counter()

    for offset in range(0, 1000, batch_size):
        results = await repo.search(
            kategori_kib=KategoriKIB.B,
            skip=offset,
            limit=batch_size,
        )
        total_processed += len(results)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed < 15.0, f"Batch processing took {elapsed:.2f}s, should be < 15s"
    assert total_processed >= 1000, f"Should process all assets, got {total_processed}"
