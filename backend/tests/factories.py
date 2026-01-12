"""Test data factories untuk SIMANIS62 V2.

Module ini menyediakan factory functions untuk membuat test data.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models.aset import AsalUsul, Aset, KategoriKIB, Kondisi, StatusAset
from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.models.ruangan import Ruangan
from app.models.user import User, UserRole, UserStatus


def create_test_user(
    username: str = "testuser",
    password_hash: str = "$2b$12$test_hash",
    nama_lengkap: str = "Test User",
    role: UserRole = UserRole.ADMIN,
    status: UserStatus = UserStatus.AKTIF,
    dapat_ekspor: bool = False,
) -> User:
    """Create test user instance."""
    return User(
        id=uuid4(),
        username=username,
        password_hash=password_hash,
        nama_lengkap=nama_lengkap,
        role=role,
        status=status,
        dapat_ekspor=dapat_ekspor,
        created_at=datetime.now(UTC),
    )


def create_test_ruangan(
    kode_ruangan: str = "R001",
    nama_ruangan: str = "Ruang Test",
    keterangan: str | None = None,
) -> Ruangan:
    """Create test ruangan instance."""
    return Ruangan(
        id=uuid4(),
        kode_ruangan=kode_ruangan,
        nama_ruangan=nama_ruangan,
        keterangan=keterangan,
        created_at=datetime.now(UTC),
    )


def create_test_aset(
    nama_barang: str = "Laptop Test",
    kode_barang: str = "02.06.01.0001",
    nomor_register: int = 1,  # int, not string
    kategori_kib: KategoriKIB = KategoriKIB.B,
    tahun_perolehan: int = 2024,
    harga: int = 15_000_000,
    kondisi: Kondisi = Kondisi.BAIK,
    status: StatusAset = StatusAset.AKTIF,
    ruangan_id: UUID | None = None,
    created_by: UUID | None = None,
) -> Aset:
    """Create test aset instance."""
    return Aset(
        id=uuid4(),
        nama_barang=nama_barang,
        kode_barang=kode_barang,
        nomor_register=nomor_register,
        kategori_kib=kategori_kib,
        tahun_perolehan=tahun_perolehan,
        asal_usul=AsalUsul.PEMBELIAN,
        harga=harga,
        kondisi=kondisi,
        status=status,
        ruangan_id=ruangan_id,
        created_by=created_by,
        created_at=datetime.now(UTC),
    )


def create_test_mutasi(
    aset_id: UUID,
    ruangan_asal_id: UUID | None,
    ruangan_tujuan_id: UUID,
    user_id: UUID,
    status_mutasi: StatusMutasi = StatusMutasi.DALAM_PROSES,
    alasan: str = "Pemindahan untuk keperluan test",
) -> RiwayatMutasi:
    """Create test mutasi instance."""
    return RiwayatMutasi(
        id=uuid4(),
        aset_id=aset_id,
        ruangan_asal_id=ruangan_asal_id,
        ruangan_tujuan_id=ruangan_tujuan_id,
        user_id=user_id,
        tanggal_mutasi=datetime.now(UTC).date(),
        alasan=alasan,
        kondisi_saat_mutasi=Kondisi.BAIK,
        status_mutasi=status_mutasi,
        mulai_mutasi=datetime.now(UTC),
    )
