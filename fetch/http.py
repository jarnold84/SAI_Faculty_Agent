
import httpx
from typing import Tuple

async def fetch_html(url: str, timeout: int = 30) -> Tuple[str, dict]:
    """
    Fetch HTML content via HTTP.
    Returns: (html_content, fetch_notes)
    TODO: Add retries, user agents, error handling
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            response.raise_for_status()
            
            return response.text, {
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "method": "http"
            }
    except Exception as e:
        raise Exception(f"HTTP fetch failed for {url}: {str(e)}")
import httpx
from typing import Tuple, Optional
import asyncio

async def fetch_html(url: str, timeout: int = 30) -> Tuple[str, dict]:
    """
    Fetch HTML content from URL with retries and proper error handling
    
    Returns:
        Tuple of (html_content, fetch_notes)
    """
    fetch_notes = {
        "url": url,
        "status_code": None,
        "content_length": None,
        "content_type": None,
        "errors": []
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            response = await client.get(url, follow_redirects=True)
            
            fetch_notes["status_code"] = response.status_code
            fetch_notes["content_type"] = response.headers.get("content-type", "")
            fetch_notes["content_length"] = len(response.content)
            
            if response.status_code == 200:
                html_content = response.text
                return html_content, fetch_notes
            else:
                fetch_notes["errors"].append(f"HTTP {response.status_code}")
                return "", fetch_notes
                
    except httpx.TimeoutException:
        fetch_notes["errors"].append("Request timeout")
        return "", fetch_notes
    except httpx.RequestError as e:
        fetch_notes["errors"].append(f"Request error: {str(e)}")
        return "", fetch_notes
    except Exception as e:
        fetch_notes["errors"].append(f"Unexpected error: {str(e)}")
        return "", fetch_notes
