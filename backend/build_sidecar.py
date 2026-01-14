#!/usr/bin/env python3
"""Build script untuk membuat sidecar executable dengan PyInstaller.

Script ini membuat executable FastAPI yang akan digunakan sebagai sidecar
oleh aplikasi Tauri SIMANIS62.

Usage:
    python build_sidecar.py

Output:
    frontend-tauri/src-tauri/bin/api/simanis62-api-{target_triple}.exe
"""

import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_target_triple() -> str:
    """Dapatkan target triple untuk platform saat ini.

    Tauri menggunakan format: {arch}-{vendor}-{os}[-{env}]

    Returns:
        Target triple string (contoh: x86_64-pc-windows-msvc)
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Map architecture
    arch_map = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "x64": "x86_64",
        "i386": "i686",
        "i686": "i686",
        "x86": "i686",
        "arm64": "aarch64",
        "aarch64": "aarch64",
    }
    arch = arch_map.get(machine, machine)

    # Map OS
    if system == "windows":
        return f"{arch}-pc-windows-msvc"
    if system == "darwin":
        return f"{arch}-apple-darwin"
    if system == "linux":
        return f"{arch}-unknown-linux-gnu"
    raise ValueError(f"Unsupported platform: {system}")


def build_sidecar() -> Path:
    """Build sidecar executable dengan PyInstaller.

    Returns:
        Path ke executable yang dihasilkan.

    Raises:
        subprocess.CalledProcessError: Jika build gagal.
    """
    # Paths
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    tauri_bin_dir = project_root / "frontend-tauri" / "src-tauri" / "bin" / "api"

    # Ensure output directory exists
    tauri_bin_dir.mkdir(parents=True, exist_ok=True)

    # Target triple untuk naming
    target_triple = get_target_triple()
    exe_name = f"simanis62-api-{target_triple}"

    print(f"Building sidecar for target: {target_triple}")
    print(f"Output directory: {tauri_bin_dir}")

    # PyInstaller command - use pyinstaller directly
    # This ensures we use the globally installed PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--onefile",
        "--name",
        exe_name,
        "--distpath",
        str(tauri_bin_dir),
        "--workpath",
        str(backend_dir / "build" / "pyinstaller"),
        "--specpath",
        str(backend_dir / "build"),
        # Hidden imports untuk FastAPI dan dependencies
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=email.mime.multipart",
        "--hidden-import=email.mime.text",
        # SQLModel dan SQLAlchemy
        "--hidden-import=sqlmodel",
        "--hidden-import=sqlalchemy.dialects.sqlite",
        # Pydantic
        "--hidden-import=pydantic",
        "--hidden-import=pydantic_settings",
        "--hidden-import=pydantic_settings.sources",
        # aiosqlite untuk async SQLite
        "--hidden-import=aiosqlite",
        # Collect all data files
        "--collect-all=uvicorn",
        "--collect-all=starlette",
        "--collect-all=fastapi",
        "--collect-all=pydantic_settings",
        "--collect-all=aiosqlite",
        # Clean build
        "--clean",
        "--noconfirm",
        # Entry point
        str(backend_dir / "app" / "main.py"),
    ]

    print("Running PyInstaller...")
    print(f"Command: {' '.join(pyinstaller_args)}")

    # Run PyInstaller
    result = subprocess.run(
        pyinstaller_args,
        cwd=backend_dir,
        check=True,
        capture_output=False,
    )

    # Verify output
    if platform.system() == "Windows":
        output_exe = tauri_bin_dir / f"{exe_name}.exe"
    else:
        output_exe = tauri_bin_dir / exe_name

    if not output_exe.exists():
        raise FileNotFoundError(f"Build failed: {output_exe} not found")

    print("\n[OK] Build successful!")
    print(f"   Executable: {output_exe}")
    print(f"   Size: {output_exe.stat().st_size / 1024 / 1024:.1f} MB")

    return output_exe


def clean_build() -> None:
    """Bersihkan folder build temporary."""
    backend_dir = Path(__file__).parent
    build_dir = backend_dir / "build"

    if build_dir.exists():
        print(f"Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build SIMANIS62 API sidecar")
    parser.add_argument("--clean", action="store_true", help="Clean build directory")
    args = parser.parse_args()

    if args.clean:
        clean_build()
    else:
        try:
            output = build_sidecar()
            print(f"\nSidecar ready at: {output}")
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Build failed with exit code {e.returncode}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[ERROR] Build failed: {e}")
            sys.exit(1)
