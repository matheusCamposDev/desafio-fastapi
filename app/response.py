from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


register_responses = {
    200: {"description": "This response is not used"},
    201: {
        "description": "Created",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"Created": "User created!"},
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "detail": "The user with this email already exists in the system"
                },
            },
        },
    },
    404: {"description": "Not Found", "model": ErrorResponse},
    422: {"description": "Validation Error", "model": ErrorResponse},
}

login_responses = {
    200: {
        "description": "OK",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "access_token": "str_access_token",
                    "refresh_token": "str_refresh_token",
                },
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Invalid credentials in the system"},
            },
        },
    },
    422: {"description": "Validation Error", "model": ErrorResponse},
}

refresh_token_reponses = {
    200: {
        "description": "OK",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "access_token": "str_access_token",
                },
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Invalid Token"},
            },
        },
    },
    422: {"description": "Validation Error", "model": ErrorResponse},
}
