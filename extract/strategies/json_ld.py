
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import json
import re

def extract_json_ld_people(html: str, base_url: str) -> List[Dict]:
    """
    Extract Person schema from JSON-LD structured data.
    Returns list of raw lead dictionaries.
    """
    soup = BeautifulSoup(html, 'html.parser')
    leads = []
    
    # Find all JSON-LD script tags
    json_scripts = soup.find_all('script', type='application/ld+json')
    
    for script in json_scripts:
        try:
            data = json.loads(script.string)
            
            # Handle both single objects and arrays
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                continue
                
            for item in data:
                if isinstance(item, dict):
                    # Check if this is a Person or contains Person data
                    persons = _extract_persons_from_item(item)
                    for person in persons:
                        lead = _convert_person_to_lead(person, base_url)
                        if lead:
                            leads.append(lead)
                            
        except (json.JSONDecodeError, KeyError, TypeError):
            # Skip malformed JSON-LD
            continue
    
    return leads

def _extract_persons_from_item(item: Dict) -> List[Dict]:
    """Extract Person objects from a JSON-LD item"""
    persons = []
    
    # Direct Person object
    if item.get('@type') == 'Person':
        persons.append(item)
    
    # Array of Person objects  
    elif item.get('@type') == 'ItemList' and 'itemListElement' in item:
        for element in item['itemListElement']:
            if isinstance(element, dict) and element.get('@type') == 'Person':
                persons.append(element)
    
    # Organization with members
    elif item.get('@type') == 'Organization' and 'member' in item:
        members = item['member']
        if not isinstance(members, list):
            members = [members]
        for member in members:
            if isinstance(member, dict) and member.get('@type') == 'Person':
                persons.append(member)
    
    return persons

def _convert_person_to_lead(person: Dict, base_url: str) -> Optional[Dict]:
    """Convert JSON-LD Person to raw lead format"""
    try:
        # Extract name (required)
        name = person.get('name')
        if not name:
            return None
            
        # Extract other fields with fallbacks
        title = (person.get('jobTitle') or 
                person.get('hasOccupation', {}).get('name') if isinstance(person.get('hasOccupation'), dict) else None)
        
        email = person.get('email')
        # Clean email if it has mailto: prefix
        if email and email.startswith('mailto:'):
            email = email[7:]
            
        profile_url = person.get('url') or person.get('sameAs')
        if isinstance(profile_url, list) and profile_url:
            profile_url = profile_url[0]
            
        # Extract social links
        socials = []
        same_as = person.get('sameAs', [])
        if isinstance(same_as, str):
            same_as = [same_as]
        for link in same_as:
            if any(social in link.lower() for social in ['twitter', 'facebook', 'linkedin', 'instagram']):
                socials.append(link)
        
        return {
            'name': name,
            'title': title,
            'email_raw': email,
            'profile_url': profile_url,
            'directory_url': base_url,
            'socials': socials,
            'bio_snippet': person.get('description'),
            'diagnostics': {
                'source_strategy': 'json_ld',
                'confidence': 0.9  # High confidence for structured data
            }
        }
        
    except (KeyError, TypeError):
        return None
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any

def extract_json_ld_people(html_content: str, source_url: str) -> List[Dict[str, Any]]:
    """
    Extract faculty information from JSON-LD structured data
    """
    if not html_content:
        return []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all JSON-LD script tags
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        
        faculty_data = []
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                
                # Handle both single objects and arrays
                if isinstance(data, list):
                    items = data
                else:
                    items = [data]
                
                for item in items:
                    # Look for Person schema objects
                    if is_person_schema(item):
                        person_data = extract_person_data(item, source_url)
                        if person_data:
                            faculty_data.append(person_data)
                    
                    # Handle nested structures (e.g., Organization with employees)
                    elif isinstance(item, dict):
                        nested_people = find_nested_people(item, source_url)
                        faculty_data.extend(nested_people)
                        
            except json.JSONDecodeError:
                continue
            except Exception:
                continue
        
        return faculty_data
        
    except Exception:
        return []

def is_person_schema(item: Dict[str, Any]) -> bool:
    """Check if item is a Person schema object"""
    if not isinstance(item, dict):
        return False
        
    schema_type = item.get('@type', '')
    if isinstance(schema_type, list):
        return 'Person' in schema_type
    return schema_type == 'Person'

def extract_person_data(person: Dict[str, Any], source_url: str) -> Dict[str, Any]:
    """Extract relevant data from Person schema"""
    try:
        # Extract name (try multiple fields)
        name = (person.get('name') or 
                person.get('givenName', '') + ' ' + person.get('familyName', '')).strip()
        
        if not name:
            return None
        
        # Extract job title
        job_title = person.get('jobTitle') or person.get('title')
        
        # Extract email
        email = person.get('email')
        if isinstance(email, list) and email:
            email = email[0]
        
        # Extract URL/profile
        url = person.get('url') or person.get('sameAs')
        if isinstance(url, list) and url:
            url = url[0]
            
        # Extract description/bio
        description = person.get('description') or person.get('bio')
        
        # Extract social links
        socials = []
        same_as = person.get('sameAs', [])
        if isinstance(same_as, list):
            socials = [link for link in same_as if isinstance(link, str) and link.startswith('http')]
        elif isinstance(same_as, str) and same_as.startswith('http'):
            socials = [same_as]
        
        return {
            'name': name,
            'title': job_title,
            'email': email,
            'profile_url': url,
            'directory_url': source_url,
            'socials': socials,
            'bio_snippet': description
        }
        
    except Exception:
        return None

def find_nested_people(item: Dict[str, Any], source_url: str) -> List[Dict[str, Any]]:
    """Find Person objects nested within other schema objects"""
    people = []
    
    try:
        # Common fields that might contain people
        people_fields = ['employee', 'member', 'person', 'author', 'contributor']
        
        for field in people_fields:
            if field in item:
                field_value = item[field]
                if isinstance(field_value, list):
                    for sub_item in field_value:
                        if is_person_schema(sub_item):
                            person_data = extract_person_data(sub_item, source_url)
                            if person_data:
                                people.append(person_data)
                elif is_person_schema(field_value):
                    person_data = extract_person_data(field_value, source_url)
                    if person_data:
                        people.append(person_data)
        
    except Exception:
        pass
    
    return people
