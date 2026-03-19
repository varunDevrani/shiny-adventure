from __future__ import annotations

from fastapi import FastAPI

from src.errors.handlers import register_exception_handlers


app = FastAPI()


register_exception_handlers(app)
