from fastapi import FastAPI, Request
import time

from src.errors.handlers import register_exception_handlers
from src.models.base import Base
from src.routes.auth import router as auth_router
from src.routes.evening import router as evening_router
from src.database.connect import engine
from fastapi.openapi.utils import get_openapi


app = FastAPI()



def custom_openapi(app: FastAPI):
    def openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
        )

        schemas = schema.get("components", {}).get("schemas", {})

        # Rewrite the auto-generated HTTPValidationError to match
        # what your validation_exception_handler actually returns
        schemas["HTTPValidationError"] = {
            "type": "object",
            "title": "HTTPValidationError",
            "properties": {
                "success": {"type": "boolean", "default": False},
                "error_code": {"type": "string"},
                "message": {"type": "string"},
                "field_violation": {"type": "array", "items": {}},
            },
            "required": ["success", "error_code", "message", "field_violation"],
        }

        # Remove the unused ValidationError schema that Pydantic's
        # error details reference (the loc/msg/type/input/ctx one)
        schemas.pop("ValidationError", None)

        app.openapi_schema = schema
        return schema

    app.openapi = openapi


@app.on_event("startup")
def startup():
	Base.metadata.create_all(bind=engine)
	


register_exception_handlers(app)



@app.get("/")
def root():
	return {
		"message": "FUCK YOU"
	}
	
custom_openapi(app)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(evening_router, prefix="/api/v1")

