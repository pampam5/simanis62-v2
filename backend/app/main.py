"""Entry point FastAPI untuk SIMANIS62 V2.

Menginisialisasi aplikasi, middleware, logging, dan routing.
"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Factory function untuk membuat instance FastAPI.

    Detail konfigurasi (logging, database, middleware, router) akan
    diimplementasikan sesuai design di .kiro/specs/simanis62-v2/design.md.
    """
    # TODO: setup logging, database, middleware, router v1, dll.

    return FastAPI(title="SIMANIS62 V2 API")


app = create_app()
