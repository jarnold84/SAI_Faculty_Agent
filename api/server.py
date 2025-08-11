from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from schemas import ScrapeResponse, ErrorResponse
from typing import Optional

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="University faculty directory URL to scrape")
    enable_js: Optional[bool] = Field(False, description="Enable JavaScript rendering")
    enrich_profiles: Optional[bool] = Field(False, description="Fetch individual profile pages")
    max_pages: Optional[int] = Field(5, description="Maximum pages to crawl if pagination detected")

async def scrape_faculty_directory(request: ScrapeRequest, enrich_emails: bool = False) -> ScrapeResponse:
    """
    Main endpoint for scraping university music faculty directories.
    Implements the core pipeline: Analyze → Fetch → Extract → Normalize
    """
    try:
        from analyze.plan import create_analysis_plan
        from fetch.http import fetch_html
        from extract.strategies.json_ld import extract_json_ld_people
        from schemas import NormalizedLead, EmailStatus
        
        # Phase 1: Analyze URL
        plan = create_analysis_plan(request.url)
        
        # Phase 2: Fetch HTML content
        html_content, fetch_notes = await fetch_html(request.url)
        
        # Phase 3: Try extraction strategies in order
        raw_leads = []
        strategy_used = None
        
        for strategy_name in plan['strategies']:
            if strategy_name == 'json_ld':
                raw_leads = extract_json_ld_people(html_content, request.url)
                if raw_leads:
                    strategy_used = 'json_ld'
                    break
            elif strategy_name == 'directory_table':
                from extract.strategies.directory_table import extract_directory_table
                raw_leads = extract_directory_table(html_content, request.url)
                if raw_leads:
                    strategy_used = 'directory_table'
                    break
            elif strategy_name == 'faculty_generic':
                from extract.strategies.faculty_generic import extract_faculty_generic
                raw_leads = extract_faculty_generic(html_content, request.url)
                if raw_leads:
                    strategy_used = 'faculty_generic'
                    break
        
        # Phase 4: Enrich with emails from profiles (if enabled)
        if enrich_emails and raw_leads:
            from normalize.profile_enricher import enrich_emails_from_profiles
            raw_leads = await enrich_emails_from_profiles(raw_leads)
        
        # Phase 5: Normalize data
        normalized_leads = []
        for raw_lead in raw_leads:
            # Basic normalization - TODO: move to separate normalizer
            normalized_lead = NormalizedLead(
                name=raw_lead.get('name', ''),
                title=raw_lead.get('title'),
                email=raw_lead.get('email_raw'),
                email_status=EmailStatus.FOUND_ON_PROFILE if raw_lead.get('email_enriched') else (EmailStatus.PRESENT if raw_lead.get('email_raw') else EmailStatus.MISSING),
                profile_url=raw_lead.get('profile_url'),
                directory_url=raw_lead.get('directory_url', request.url),
                socials=raw_lead.get('socials', []),
                bio_snippet=raw_lead.get('bio_snippet')
            )
            normalized_leads.append(normalized_lead)
        
        # Return results
        return ScrapeResponse(
            success=len(normalized_leads) > 0,
            items=normalized_leads,
            total_found=len(normalized_leads),
            source_url=request.url,
            strategy_used=strategy_used,
            message=f"Extracted {len(normalized_leads)} faculty members using {strategy_used or 'no'} strategy"
        )
        
    except Exception as e:
        # Return error in consistent format
        return ScrapeResponse(
            success=False,
            items=[],
            total_found=0,
            source_url=request.url,
            strategy_used=None,
            message=f"Error occurred: {str(e)}"
        )

def register_routes(app: FastAPI):
    """Register all API routes"""
    
    @app.post("/scrape", response_model=ScrapeResponse)
    async def scrape_endpoint(request: ScrapeRequest):
        """Scrape a university music faculty directory"""
        return await scrape_faculty_directory(request)
    
    @app.get("/test/{url:path}")
    async def quick_test(url: str):
        """Quick test endpoint for debugging URLs"""
        request = ScrapeRequest(url=url)
        return await scrape_faculty_directory(request)
    
    @app.post("/debug")
    async def debug_html(request: ScrapeRequest):
        """Debug endpoint to see what HTML we're getting"""
        from fetch.http import fetch_html
        try:
            html_content, fetch_notes = await fetch_html(request.url)
            return {
                "url": request.url,
                "html_length": len(html_content),
                "fetch_notes": fetch_notes,
                "html_preview": html_content[:1000] + "..." if len(html_content) > 1000 else html_content,
                "has_json_ld": "<script type=\"application/ld+json\">" in html_content
            }
        except Exception as e:
            return {"error": str(e)}

app = FastAPI(title="Faculty Scraping Agent API")
register_routes(app)
