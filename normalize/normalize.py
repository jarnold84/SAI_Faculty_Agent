
from schemas import NormalizedLead, EmailStatus
from typing import List, Dict, Any
import re

from typing import List, Dict, Any, Optional
from schemas.normalized_lead import NormalizedLead, EmailStatus

def normalize_faculty_data(raw_leads: List[Dict[Any, Any]], source_url: str) -> List[NormalizedLead]:
    """
    Normalize raw extracted faculty data into consistent schema
    """
    normalized_leads = []
    
    for raw_lead in raw_leads:
        # Clean and normalize name
        name = str(raw_lead.get('name', '')).strip()
        if not name:
            continue  # Skip entries without names
            
        # Normalize title
        title = raw_lead.get('title') or raw_lead.get('jobTitle')
        if title:
            title = str(title).strip()
        
        # Handle email extraction and status
        email_raw = raw_lead.get('email') or raw_lead.get('email_raw')
        email_status = EmailStatus.MISSING
        clean_email = None
        
        if email_raw:
            clean_email = clean_email_address(email_raw)
            if clean_email:
                email_status = EmailStatus.PRESENT
            else:
                email_status = EmailStatus.OBFUSCATED_UNRESOLVED
        
        # Handle profile URL
        profile_url = raw_lead.get('profile_url') or raw_lead.get('url')
        if profile_url and not profile_url.startswith('http'):
            profile_url = None
            
        # Handle social links
        socials = raw_lead.get('socials', [])
        if not isinstance(socials, list):
            socials = []
        
        # Create normalized lead
        normalized_lead = NormalizedLead(
            name=name,
            title=title,
            email=clean_email,
            email_status=email_status,
            profile_url=profile_url,
            directory_url=source_url,
            socials=socials,
            bio_snippet=raw_lead.get('bio_snippet')
        )
        
        normalized_leads.append(normalized_lead)
    
    return normalized_leads

def clean_email_address(email_raw: str) -> Optional[str]:
    """Clean and validate email address"""
    if not email_raw:
        return None
        
    # Remove mailto: prefix
    email = email_raw.replace('mailto:', '').strip()
    
    # Basic email validation
    if '@' in email and '.' in email.split('@')[1]:
        return email
    
    return None
            email_status=email_status,
            profile_url=profile_url,
            directory_url=source_url,
            socials=socials,
            bio_snippet=raw_lead.get('bio_snippet')
        )
        
        normalized_leads.append(normalized_lead)
    
    return normalized_leads

def clean_email_address(email_raw: str) -> str:
    """Clean and validate email address"""
    if not email_raw:
        return None
        
    email = str(email_raw).strip().lower()
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    
    return None
