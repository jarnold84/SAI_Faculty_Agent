
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import re

def extract_directory_table(html_content: str, source_url: str) -> List[Dict[str, Any]]:
    """
    Extract faculty information from HTML tables or lists
    """
    if not html_content:
        return []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        faculty_data = []
        
        # Strategy 1: Look for tables with faculty data
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                person_data = extract_person_from_table_row(row, source_url)
                if person_data:
                    faculty_data.append(person_data)
        
        # Strategy 2: Look for div-based directory listings
        if not faculty_data:
            faculty_data.extend(extract_from_div_listings(soup, source_url))
        
        # Strategy 3: Look for ul/li based listings  
        if not faculty_data:
            faculty_data.extend(extract_from_list_items(soup, source_url))
            
        return faculty_data
        
    except Exception:
        return []

def extract_person_from_table_row(row, source_url: str) -> Dict[str, Any]:
    """Extract person data from a table row"""
    try:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            return None
            
        # Look for name in first cell
        name_cell = cells[0]
        name = name_cell.get_text(strip=True)
        
        if not name or len(name) < 3:
            return None
            
        # Look for email in any cell
        email = None
        title = None
        profile_url = None
        
        for cell in cells:
            cell_text = cell.get_text(strip=True)
            
            # Extract email
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cell_text)
            if email_match and not email:
                email = email_match.group()
            
            # Extract title (if it contains common title words)
            if any(title_word in cell_text.lower() for title_word in ['professor', 'instructor', 'lecturer', 'chair', 'director']):
                title = cell_text
                
            # Extract profile URL
            link = cell.find('a')
            if link and link.get('href') and not profile_url:
                href = link.get('href')
                if href.startswith('http'):
                    profile_url = href
                elif href.startswith('/'):
                    # Convert relative URL to absolute
                    from urllib.parse import urljoin
                    profile_url = urljoin(source_url, href)
                else:
                    profile_url = href
        
        return {
            'name': name,
            'title': title,
            'email': email,
            'profile_url': profile_url,
            'directory_url': source_url,
            'socials': [],
            'bio_snippet': None
        }
        
    except Exception:
        return None

def extract_from_div_listings(soup, source_url: str) -> List[Dict[str, Any]]:
    """Extract from div-based faculty listings"""
    faculty_data = []
    
    # Look for divs that might contain faculty info
    potential_divs = soup.find_all('div', class_=re.compile(r'(faculty|person|staff|member|profile)', re.I))
    
    for div in potential_divs:
        person_data = extract_person_from_div(div, source_url)
        if person_data:
            faculty_data.append(person_data)
    
    return faculty_data

def extract_from_list_items(soup, source_url: str) -> List[Dict[str, Any]]:
    """Extract from ul/li based faculty listings"""
    faculty_data = []
    
    # Look for lists that might contain faculty
    lists = soup.find_all(['ul', 'ol'])
    
    for list_elem in lists:
        items = list_elem.find_all('li')
        for item in items:
            person_data = extract_person_from_list_item(item, source_url)
            if person_data:
                faculty_data.append(person_data)
    
    return faculty_data

def extract_person_from_div(div, source_url: str) -> Dict[str, Any]:
    """Extract person data from a div element"""
    try:
        text = div.get_text(strip=True)
        
        # Look for name (assume it's in a header or strong tag)
        name_elem = div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'])
        name = name_elem.get_text(strip=True) if name_elem else None
        
        if not name:
            # Fallback: try first line of text
            first_line = text.split('\n')[0].strip()
            if len(first_line) > 3 and len(first_line) < 50:
                name = first_line
        
        if not name:
            return None
            
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        email = email_match.group() if email_match else None
        
        # Extract profile URL
        link = div.find('a')
        if link and link.get('href'):
            href = link.get('href')
            if href.startswith('http'):
                profile_url = href
            elif href.startswith('/'):
                from urllib.parse import urljoin
                profile_url = urljoin(source_url, href)
            else:
                profile_url = href
        else:
            profile_url = None
        
        # Extract title
        title = None
        if any(title_word in text.lower() for title_word in ['professor', 'instructor', 'lecturer', 'chair', 'director']):
            # Try to extract the line containing the title
            lines = text.split('\n')
            for line in lines:
                if any(title_word in line.lower() for title_word in ['professor', 'instructor', 'lecturer', 'chair', 'director']):
                    title = line.strip()
                    break
        
        return {
            'name': name,
            'title': title,
            'email': email,
            'profile_url': profile_url,
            'directory_url': source_url,
            'socials': [],
            'bio_snippet': None
        }
        
    except Exception:
        return None

def extract_person_from_list_item(item, source_url: str) -> Dict[str, Any]:
    """Extract person data from a list item"""
    try:
        text = item.get_text(strip=True)
        
        if len(text) < 3:
            return None
            
        # Assume first part is name
        parts = text.split('\n')
        name = parts[0].strip()
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        email = email_match.group() if email_match else None
        
        # Extract profile URL
        link = item.find('a')
        if link and link.get('href'):
            href = link.get('href')
            if href.startswith('http'):
                profile_url = href
            elif href.startswith('/'):
                from urllib.parse import urljoin
                profile_url = urljoin(source_url, href)
            else:
                profile_url = href
        else:
            profile_url = None
        
        return {
            'name': name,
            'title': None,
            'email': email,
            'profile_url': profile_url,
            'directory_url': source_url,
            'socials': [],
            'bio_snippet': None
        }
        
    except Exception:
        return None
