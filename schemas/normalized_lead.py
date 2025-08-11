
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class EmailStatus(str, Enum):
    PRESENT = "present"
    FOUND_ON_PROFILE = "found_on_profile"
    OBFUSCATED_RESOLVED = "obfuscated_resolved"
    MISSING = "missing"
    NOT_LISTED = "not_listed"
    OBFUSCATED_UNRESOLVED = "obfuscated_unresolved"

class NormalizedLead(BaseModel):
    name: str = Field(..., description="Full name of faculty member")
    title: Optional[str] = Field(None, description="Job title or position")
    email: Optional[str] = Field(None, description="Clean email address or empty if not found")
    email_status: EmailStatus = Field(..., description="Status of email extraction")
    profile_url: Optional[str] = Field(None, description="Link to individual profile page")
    directory_url: str = Field(..., description="Source directory URL")
    socials: List[str] = Field(default_factory=list, description="Social media links")
    bio_snippet: Optional[str] = Field(None, description="Brief bio or description")

class ScrapeResponse(BaseModel):
    success: bool = Field(..., description="Whether extraction was successful")
    items: List[NormalizedLead] = Field(default_factory=list, description="Extracted faculty members")
    total_found: int = Field(..., description="Number of faculty members found")
    source_url: str = Field(..., description="URL that was scraped")
    strategy_used: Optional[str] = Field(None, description="Extraction strategy that succeeded")
    message: Optional[str] = Field(None, description="Human-readable status message")
