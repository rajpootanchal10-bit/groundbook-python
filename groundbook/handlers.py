from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .errors import GroundbookException

PROBLEM = "application/problem+json"

def problem(status: int, type_: str, title: str, detail: str, **extra) -> JSONResponse:
    """Helper function to build a compliant RFC 7807 problem details response body."""
    body = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail
    }
    body.update(extra)
    return JSONResponse(status_code=status, content=body, media_type=PROBLEM)

def register_error_handlers(app: FastAPI):
    @app.exception_handler(GroundbookException)
    async def groundbook_exception_handler(request: Request, exc: GroundbookException):
        # Map specific titles based on the error types
        if exc.error_type == "/errors/no-such-venue":
            title = "No such venue"
            detail = "The requested venue could not be found."
        elif exc.error_type == "/errors/no-such-ground":
            title = "No such ground"
            detail = "The requested ground could not be found at this venue."
        else:
            title = "Validation error"
            detail = "The provided request payload or route parameters are invalid."
            
        return problem(
            status=exc.status_code,
            type_=exc.error_type,
            title=title,
            detail=detail
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return problem(
            status=400,
            type_="/errors/validation",
            title="Validation error",
            detail="The request structure or values fail baseline format verification rules."
        )