from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exceção para recurso não encontrado"""
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException(HTTPException):
    """Exceção para conflito de dados"""
    def __init__(self, detail: str = "Conflito de dados"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedException(HTTPException):
    """Exceção para não autorizado"""
    def __init__(self, detail: str = "Não autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    """Exceção para acesso proibido"""
    def __init__(self, detail: str = "Acesso proibido"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(HTTPException):
    """Exceção para requisição inválida"""
    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
