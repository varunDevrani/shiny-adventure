from http import HTTPStatus

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.errors.codes import ErrorCode
from src.errors.app_exception import AppException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    def domain_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message
            }
        )

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error_code": ErrorCode.UNPROCESSABLE_CONTENT,
                "message": "Request cannot be processed",
                "field_violation": []
            }
        )

    @app.exception_handler(Exception)
    def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error_code": ErrorCode.INTERNAL_SERVER_ERROR,
                "message": str(exc)
            }
        )
