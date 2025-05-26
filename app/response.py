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

clients_get_responses = {
    200: {
        "description": "OK",
        "model": dict,
        "content": {
            "application/json": {
                "example": [
                    {"id": 1, "name": "João Silva", "email": "joao@example.com"},
                    {"id": 2, "name": "Maria Souza", "email": "maria@example.com"},
                ]
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "No clients found with the given criteria."},
            },
        },
    },
    422: {
        "description": "Not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": ""},
            },
        },
    },
}


clients_create_responses = {
    201: {
        "description": "Created",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"Created": "Client created successfully!"},
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Email ou CPF já cadastrado."},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    422: {
        "description": "Not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": ""},
            },
        },
    },
}


get_client_responses = {
    200: {
        "description": "Ok",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "name": "João Silva",
                    "email": "joao@example.com",
                    "cpf": "12345678901",
                    "id": 1,
                }
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Cliente ID 1 não encontrado"},
            },
        },
    },
    422: {
        "description": "Not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": ""},
            },
        },
    },
}

update_client_responses = {
    200: {
        "description": "Ok",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "name": "João Silva",
                    "email": "joao@example.com",
                    "cpf": "12345678901",
                    "id": 1,
                }
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Insira um email válido."},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Cliente ID 1 não encontrado"},
            },
        },
    },
    422: {
        "description": "Not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": ""},
            },
        },
    },
}

delete_client_responses = {
    204: {
        "description": "No Content",
        "content": {
            "application/json": {
                "example": {},
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Erro ao deletar cliente. Verifique os dados."},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Cliente ID 1 não encontrado"},
            },
        },
    },
    422: {
        "description": "Not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": ""},
            },
        },
    },
}

products_list_responses = {
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "No products found with the given criteria."},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    422: {
        "description": "This response is not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "This response is not used"},
            },
        },
    },
}

product_create_responses = {
    201: {
        "description": "Created",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": "string",
                    "price": 0,
                    "barcode": "string",
                    "section": "string",
                    "stock": 0,
                    "expiry_date": "2025-05-26",
                    "available": True,
                    "image_url": "string",
                },
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "Error product": {
                        "summary": "Error product",
                        "value": {"detail": "Error creating product"},
                    },
                    "Error codebar": {
                        "summary": "Error codebar",
                        "value": {
                            "detail": "A product with this barcode already exists."
                        },
                    },
                },
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    422: {
        "description": "This response is not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "This response is not used"},
            },
        },
    },
}


product_by_id_responses = {
    200: {
        "description": "OK",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": "string",
                    "price": 0,
                    "barcode": "string",
                    "section": "string",
                    "stock": 0,
                    "expiry_date": "2025-05-26",
                    "available": True,
                    "image_url": "string",
                },
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Product ID not found."},
            },
        },
    },
    422: {
        "description": "This response is not used",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "This response is not used"},
            },
        },
    },
}


product_put_responses = {
    200: {
        "description": "OK",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": "string",
                    "price": 0,
                    "barcode": "string",
                    "section": "string",
                    "stock": 0,
                    "expiry_date": "2025-05-26",
                    "available": True,
                    "image_url": "string",
                },
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Error updating product"},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Product ID not found."},
            },
        },
    },
}

product_delete_responses = {
    204: {
        "description": "No Content",
        "content": {
            "application/json": {
                "example": {},
            },
        },
    },
    400: {
        "description": "Bad Request",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Error deleting product"},
            },
        },
    },
    403: {
        "description": "Forbidden",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    404: {
        "description": "Not Found",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": "Product ID not found."},
            },
        },
    },
}
