from typing import Optional

from fastapi import HTTPException

__all__ = (
    'ValidationResult',
)


class ValidationResult:

    def __init__(self, is_valid: bool, detail: Optional[str] = None, data: Optional[dict] = None) -> None:
        self.is_valid = is_valid
        self.detail = detail
        self.data = data

    def raise_for_is_valid(self) -> None:
        if self.is_valid:
            return
        raise HTTPException(status_code=400, detail={
            'message': self.detail,
            'data': self.data,
            'error': None
        })

    def __bool__(self) -> bool:
        return self.is_valid
