"""Performance tests untuk search functionality.

Tests untuk:
- Search performance < 5 detik untuk 1000 aset
- Login performance < 2 detik
"""

import time
from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.models.aset import AsalUsul, Aset, KategoriKIB, Kondisi, StatusAset
from app.repositories.aset_repository import AsetRepository


@pytest_asyncio.fixture
async def bulk_asets(db_session):
    """Create 1000 asets untuk performance testing."""
    asets = []
    user_id = uuid4()  # UUID object
    ruangan_id = uuid4()  # UUID object

    for i in range(1000):
        aset = Aset(
            id=uuid4(),
            nama_barang=f"Aset Performance Test {i:04d}",
            kode_barang=f"02.06.{(i // 100):02d}.{(i % 10000):04d}",
            nomor_register=i + 1,  # int, not string
            kategori_kib=KategoriKIB.B,
            tahun_perolehan=2024,
            asal_usul=AsalUsul.PEMBELIAN,  # Use enum
            harga=1_000_000 + (i * 1000),
            kondisi=Kondisi.BAIK,
            status=StatusAset.AKTIF,
            ruangan_id=ruangan_id,  # UUID object
            created_by=user_id,  # UUID object
            created_at=datetime.now(UTC),
        )
        asets.append(aset)

    # Batch insert
    db_session.add_all(asets)
    await db_session.commit()

    return asets


@pytest.mark.asyncio
@pytest.mark.slow
async def test_search_performance_under_5_seconds(db_session, bulk_asets):
    """Test search performance < 5 detik untuk 1000 aset.

    REQ-22: Search aset < 5 detik
    """
    repo = AsetRepository(db_session)

    # Measure search time
    start_time = time.perf_counter()

    results = await repo.search(
        keyword="Performance",
        limit=100,
    )

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed < 5.0, f"Search took {elapsed:.2f}s, should be < 5s"
    assert len(results) > 0, "Should return results"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_search_with_filters_performance(db_session, bulk_asets):
    """Test search dengan multiple filters < 5 detik."""
    repo = AsetRepository(db_session)

    start_time = time.perf_counter()

    results = await repo.search(
        keyword="Test",
        kategori_kib=KategoriKIB.B,
        status=StatusAset.AKTIF,
        tahun_perolehan=2024,
        limit=100,
    )

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed < 5.0, f"Filtered search took {elapsed:.2f}s, should be < 5s"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_pagination_performance(db_session, bulk_asets):
    """Test pagination performance."""
    repo = AsetRepository(db_session)

    # Test multiple pages
    total_time = 0
    for page in range(10):
        start_time = time.perf_counter()

        results = await repo.search(
            skip=page * 100,
            limit=100,
        )

        end_time = time.perf_counter()
        total_time += end_time - start_time

    avg_time = total_time / 10
    assert avg_time < 1.0, f"Average page load took {avg_time:.2f}s, should be < 1s"


@pytest.mark.asyncio
async def test_count_performance(db_session, bulk_asets):
    """Test count query performance."""
    repo = AsetRepository(db_session)

    start_time = time.perf_counter()

    count = await repo.count_search(
        keyword="Performance",
        kategori_kib=KategoriKIB.B,
    )

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed < 2.0, f"Count took {elapsed:.2f}s, should be < 2s"
    assert count > 0, "Should return count > 0"
