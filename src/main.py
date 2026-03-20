from fastapi import FastAPI

from src.errors.handlers import register_exception_handlers
from src.models.base import Base
from src.routes.auth import router as auth_router
from src.routes.evening import router as evening_router
from src.database.connect import engine

app = FastAPI()


@app.on_event("startup")
def startup():
	Base.metadata.create_all(bind=engine)


register_exception_handlers(app)


app.include_router(auth_router, prefix="/api/v1")
app.include_router(evening_router, prefix="/api/v1")

