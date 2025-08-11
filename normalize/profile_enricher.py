
import asyncio
import re
from typing import List, Dict, Any
from fetch.http import fetch_html

async def enrich_emails_from_profiles(raw_leads: List[Dict[str, Any]], max_concurrent: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch emails from individual profile URLs.
    Simple, fast, graceful fallback if anything fails.
    """
    enriched_leads = []
    
    # Process in batches to be polite to servers
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def enrich_single_profile(lead):
        async with semaphore:
            if not lead.get('profile_url'):
                return lead
            
            try:
                # Fetch profile page
                html_content, _ = await fetch_html(lead['profile_url'], timeout=10)
                
                # Extract email with regex
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_content)
                
                if email_match:
                    lead['email_raw'] = email_match.group()
                    lead['email_enriched'] = True
                else:
                    lead['email_enriched'] = False
                    
            except Exception:
                # Graceful fallback - don't break the whole pipeline
                lead['email_enriched'] = False
                
            return lead
    
    # Process all profiles concurrently
    tasks = [enrich_single_profile(lead.copy()) for lead in raw_leads]
    enriched_leads = await asyncio.gather(*tasks)
    
    return enriched_leads
