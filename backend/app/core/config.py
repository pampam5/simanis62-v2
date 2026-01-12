"""Konfigurasi aplikasi backend SIMANIS62 V2.

Menggunakan Pydantic Settings + file JSON di folder ``configs/``
seperti dijelaskan pada .kiro/specs/simanis62-v2/requirements.md dan design.md
serta steering/tech.md.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Path dasar proyek
_CURRENT_FILE = Path(__file__).resolve()
BACKEND_DIR = _CURRENT_FILE.parents[2]  # backend
PROJECT_ROOT = _CURRENT_FILE.parents[3]  # simanis62-v2
CONFIG_DIR = PROJECT_ROOT / "configs"
ENV_FILE = BACKEND_DIR / ".env"


class ApiSettings(BaseModel):
    """Konfigurasi API FastAPI."""

    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True


class DatabaseSettings(BaseModel):
    """Konfigurasi database SQLite."""

    # Path absolut atau relatif ke file database SQLite.
    path: str = "simanis62.db"


class LoggingSettings(BaseModel):
    """Konfigurasi logging backend."""

    level: str = "INFO"
    # Direktori untuk file log (boleh relatif terhadap root proyek).
    log_dir: str = "logs"


class Settings(BaseSettings):
    """Konfigurasi utama aplikasi.

    Sumber konfigurasi (prioritas tinggi ke rendah):
    1. Environment variables (mis. ``ENVIRONMENT``, ``SECRET_KEY``, ``GLITCHTIP_DSN``)
    2. File JSON di ``configs/<environment>.json``
    3. Default value di class ini
    """

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment name: development / production / testing
    environment: str = Field("development", alias="ENVIRONMENT")

    # Secret & monitoring
    secret_key: str = Field("change_me", alias="SECRET_KEY")
    glitchtip_dsn: str | None = Field(None, alias="GLITCHTIP_DSN")

    # Application settings
    nama_sekolah: str = Field("SDN 01 Jakarta Timur", alias="NAMA_SEKOLAH")
    session_timeout_hours: int = Field(2, alias="SESSION_TIMEOUT_HOURS")
    export_dir: str = Field("exports", alias="EXPORT_DIR")

    # Nested config sections
    api: ApiSettings = ApiSettings()
    database: DatabaseSettings = DatabaseSettings()
    logging: LoggingSettings = LoggingSettings()

    # Convenience properties yang dipakai di design.md
    @property
    def DEBUG(self) -> bool:
        return self.api.debug

    @property
    def DATABASE_PATH(self) -> str:
        return self.database.path

    @property
    def LOG_DIR(self) -> str:
        # Jika path relatif, anggap relatif ke root proyek.
        log_dir = Path(self.logging.log_dir)
        if not log_dir.is_absolute():
            log_dir = PROJECT_ROOT / log_dir
        return str(log_dir)

    @property
    def LOG_LEVEL(self) -> str:
        return self.logging.level.upper()

    @property
    def LOG_FILE(self) -> str:
        """Path ke file log utama."""
        log_dir = Path(self.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        return str(log_dir / "simanis62.log")

    @property
    def APP_VERSION(self) -> str:
        """Versi aplikasi."""
        return "2.0.0"

    @property
    def ENVIRONMENT(self) -> str:
        """Environment name."""
        return self.environment


def _load_json_config(environment: str) -> dict[str, Any]:
    """Membaca file configs/<environment>.json jika ada.

    Jika file tidak ada atau invalid, mengembalikan dict kosong.
    """

    filename = f"{environment.lower()}.json"
    path = CONFIG_DIR / filename

    if not path.exists():
        return {}

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception:
        # Jangan gagal hanya karena file config bermasalah; log akan
        # ditangani oleh layer logging saat sudah aktif.
        return {}

    # Normalisasi struktur lama (env, debug, port) ke struktur baru jika perlu.
    if "api" not in data:
        api_data: dict[str, Any] = {}
        if "host" in data:
            api_data["host"] = data["host"]
        if "port" in data:
            api_data["port"] = data["port"]
        if "debug" in data:
            api_data["debug"] = data["debug"]
        if api_data:
            data["api"] = api_data

    if "logging" not in data and "logging_level" in data:
        data["logging"] = {"level": data["logging_level"]}

    if "database" not in data and "database" in data:
        # Sudah dalam bentuk nested, biarkan saja.
        pass

    return data


@lru_cache
def get_settings() -> Settings:
    """Mengembalikan instance `Settings` yang dicache.

    Fungsi ini dipakai oleh modul lain: ``from app.core.config import settings``.
    """

    # Baca ENVIRONMENT dari OS terlebih dulu agar bisa menentukan file JSON.
    env = os.getenv("ENVIRONMENT", "development")
    file_data = _load_json_config(env)

    return Settings(**file_data)


# Instance global yang lazim digunakan di seluruh backend.
settings = get_settings()
