"""Unit tests untuk MutasiRepository.

Tests untuk:
- CRUD operations
- Query mutations
- Pagination
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.models.aset import AsalUsul, Aset, KategoriKIB, Kondisi, StatusAset
from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.models.ruangan import Ruangan
from app.models.user import User, UserRole, UserStatus
from app.repositories.mutasi_repository import MutasiRepository


@pytest_asyncio.fixture
async def setup_mutation_data(db_session):
    """Setup test data untuk mutation tests."""
    # Create user first (for foreign key)
    user = User(
        id=uuid4(),
        username="mutasi_test_user",
        password_hash="$2b$12$mock_hash_test",
        nama_lengkap="Mutasi Test User",
        role=UserRole.ADMIN,
        status=UserStatus.AKTIF,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)

    # Create ruangan
    ruangan_asal = Ruangan(
        id=uuid4(),
        kode_ruangan="R001",
        nama_ruangan="Ruang Asal",
        created_at=datetime.now(UTC),
    )
    ruangan_tujuan = Ruangan(
        id=uuid4(),
        kode_ruangan="R002",
        nama_ruangan="Ruang Tujuan",
        created_at=datetime.now(UTC),
    )
    db_session.add(ruangan_asal)
    db_session.add(ruangan_tujuan)

    # Create aset
    aset = Aset(
        id=uuid4(),
        nama_barang="Laptop Test",
        kode_barang="02.06.01.5001",
        nomor_register=5001,  # int, not string
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=15_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=ruangan_asal.id,  # UUID object
        created_by=user.id,  # UUID object
        created_at=datetime.now(UTC),
    )
    db_session.add(aset)

    await db_session.commit()

    return {
        "ruangan_asal": ruangan_asal,
        "ruangan_tujuan": ruangan_tujuan,
        "aset": aset,
        "user": user,
    }


@pytest.mark.asyncio
async def test_create_mutation(db_session, setup_mutation_data):
    """Test create mutation."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    mutasi = RiwayatMutasi(
        id=uuid4(),
        aset_id=data["aset"].id,  # UUID object
        ruangan_asal_id=data["ruangan_asal"].id,  # UUID object
        ruangan_tujuan_id=data["ruangan_tujuan"].id,  # UUID object
        user_id=data["user"].id,  # UUID object
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="Pemindahan untuk keperluan operasional",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )

    created = await repo.create(mutasi)
    await db_session.commit()

    assert created.id is not None
    assert created.status_mutasi == StatusMutasi.DALAM_PROSES


@pytest.mark.asyncio
async def test_get_by_id(db_session, setup_mutation_data):
    """Test get mutation by ID."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create mutation first
    mutasi_id = uuid4()
    mutasi = RiwayatMutasi(
        id=mutasi_id,
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="Test get by ID mutation",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )
    db_session.add(mutasi)
    await db_session.commit()

    # Get by ID
    result = await repo.get_by_id(mutasi_id)  # UUID object

    assert result is not None
    assert result.id == mutasi_id


@pytest.mark.asyncio
async def test_has_pending_mutation_true(db_session, setup_mutation_data):
    """Test has_pending_mutation - ada pending."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create pending mutation
    mutasi = RiwayatMutasi(
        id=uuid4(),
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="Pending mutation test case",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )
    db_session.add(mutasi)
    await db_session.commit()

    # Check has pending
    result = await repo.has_pending_mutation(data["aset"].id)  # UUID object

    assert result is True


@pytest.mark.asyncio
async def test_has_pending_mutation_false(db_session, setup_mutation_data):
    """Test has_pending_mutation - tidak ada pending."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create completed mutation
    mutasi = RiwayatMutasi(
        id=uuid4(),
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="Completed mutation test case",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.SELESAI,
        mulai_mutasi=datetime.now(UTC),
        selesai_mutasi=datetime.now(UTC),
    )
    db_session.add(mutasi)
    await db_session.commit()

    # Check has pending - should be false since mutation is completed
    result = await repo.has_pending_mutation(data["aset"].id)

    assert result is False


@pytest.mark.asyncio
async def test_complete_mutation(db_session, setup_mutation_data):
    """Test complete mutation."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create pending mutation
    mutasi_id = uuid4()
    mutasi = RiwayatMutasi(
        id=mutasi_id,
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="To be completed mutation",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )
    db_session.add(mutasi)
    await db_session.commit()

    # Complete mutation
    completed = await repo.complete_mutation(mutasi_id)  # UUID object
    await db_session.commit()

    assert completed is not None
    assert completed.status_mutasi == StatusMutasi.SELESAI
    assert completed.selesai_mutasi is not None


@pytest.mark.asyncio
async def test_cancel_mutation(db_session, setup_mutation_data):
    """Test cancel mutation."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create pending mutation
    mutasi_id = uuid4()
    mutasi = RiwayatMutasi(
        id=mutasi_id,
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="To be cancelled mutation",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )
    db_session.add(mutasi)
    await db_session.commit()

    # Cancel mutation
    alasan_batal = "Pembatalan karena perubahan keputusan"
    cancelled = await repo.cancel_mutation(mutasi_id, alasan_batal)  # UUID object
    await db_session.commit()

    assert cancelled is not None
    assert cancelled.status_mutasi == StatusMutasi.DIBATALKAN
    assert cancelled.alasan_pembatalan == alasan_batal


@pytest.mark.asyncio
async def test_get_pending_mutations(db_session, setup_mutation_data):
    """Test get all pending mutations."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create multiple mutations with different statuses
    pending = RiwayatMutasi(
        id=uuid4(),
        aset_id=data["aset"].id,
        ruangan_asal_id=data["ruangan_asal"].id,
        ruangan_tujuan_id=data["ruangan_tujuan"].id,
        user_id=data["user"].id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan="Pending mutation for test",
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=StatusMutasi.DALAM_PROSES,
        mulai_mutasi=datetime.now(UTC),
    )
    db_session.add(pending)
    await db_session.commit()

    # Get pending mutations
    results = await repo.get_pending_mutations()

    assert len(results) >= 1
    assert all(m.status_mutasi == StatusMutasi.DALAM_PROSES for m in results)


@pytest.mark.asyncio
async def test_get_mutation_history(db_session, setup_mutation_data):
    """Test get mutation history."""
    repo = MutasiRepository(db_session)
    data = setup_mutation_data

    # Create mutations
    for i in range(3):
        mutasi = RiwayatMutasi(
            id=uuid4(),
            aset_id=data["aset"].id,
            ruangan_asal_id=data["ruangan_asal"].id,
            ruangan_tujuan_id=data["ruangan_tujuan"].id,
            user_id=data["user"].id,
            tanggal_mutasi=datetime.now(UTC).date(),
            alasan=f"History mutation test {i}",
            kondisi_saat_mutasi=Kondisi.BAIK,
            status_mutasi=StatusMutasi.SELESAI,
            mulai_mutasi=datetime.now(UTC),
            selesai_mutasi=datetime.now(UTC),
        )
        db_session.add(mutasi)
    await db_session.commit()

    # Get history
    results = await repo.get_mutation_history(aset_id=data["aset"].id)  # UUID object

    assert len(results) >= 3
