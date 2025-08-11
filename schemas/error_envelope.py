
from pydantic import BaseModel, Field
from typing import Optional

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Always false for error responses")
    error_code: str = Field(..., description="Machine-readable error identifier")
    error_message: str = Field(..., description="Human-readable error description")
    source_url: Optional[str] = Field(None, description="URL that caused the error")
    details: Optional[dict] = Field(None, description="Additional error context")
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Always false for error responses")
    error_type: str = Field(..., description="Category of error (validation, network, extraction, etc.)")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context")
    source_url: Optional[str] = Field(None, description="URL that caused the error")
