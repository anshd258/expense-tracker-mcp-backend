from typing import Any, Dict, Optional, List
from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Standard API response format"""
    success: bool = True
    message: str
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {}
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated response format"""
    success: bool = True
    data: List[Any]
    total: int
    skip: int
    limit: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [],
                "total": 100,
                "skip": 0,
                "limit": 10
            }
        }


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    message: str
    status_code: int
    errors: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation error",
                "status_code": 422,
                "errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "type": "value_error"
                    }
                ]
            }
        }