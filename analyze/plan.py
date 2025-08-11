from typing import Dict, List, Optional
from urllib.parse import urlparse
import re

class AnalysisPlan:
    def __init__(self, url: str):
        self.url = url
        self.strategies = self._select_strategies(url)
        self.needs_js = self._detect_js_need(url)
        self.has_pagination = False  # TODO: Implement pagination detection
        self.hints = self._extract_hints(url)

    def _select_strategies(self, url: str) -> List[str]:
        """Select extraction strategies based on URL patterns"""
        strategies = []

        # Check URL patterns for hints
        url_lower = url.lower()

        # Faculty/directory patterns suggest structured data might be available
        if any(keyword in url_lower for keyword in ['faculty', 'directory', 'staff', 'people']):
            strategies.extend(['json_ld', 'directory_table', 'profile_cards'])

        # Music department patterns
        if any(keyword in url_lower for keyword in ['music', 'conservatory', 'arts']):
            strategies.extend(['json_ld', 'directory_table'])

        # Default fallback order if no patterns match
        if not strategies:
            strategies = ['json_ld', 'directory_table', 'profile_cards']

        # Remove duplicates while preserving order
        return list(dict.fromkeys(strategies))

    def _detect_js_need(self, url: str) -> bool:
        """Basic heuristic to detect if JS rendering might be needed"""
        # For now, assume most university sites are server-rendered
        # TODO: Implement more sophisticated detection
        return False

    def _extract_hints(self, url: str) -> Dict:
        """Extract hints from URL structure"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        hints = {
            'domain': domain,
            'path': path,
            'is_university': any(tld in domain for tld in ['.edu', '.ac.', 'university', 'college']),
            'faculty_keywords': []
        }

        # Extract potential faculty-related keywords
        faculty_terms = ['faculty', 'staff', 'people', 'directory', 'music', 'piano', 'voice', 'composition']
        hints['faculty_keywords'] = [term for term in faculty_terms if term in (domain + path)]

        return hints

def create_analysis_plan(url: str) -> Dict:
    """Create analysis plan for given URL"""
    plan = AnalysisPlan(url)

    return {
        'url': plan.url,
        'strategies': plan.strategies,
        'needs_js': plan.needs_js,
        'has_pagination': plan.has_pagination,
        'hints': plan.hints
    }