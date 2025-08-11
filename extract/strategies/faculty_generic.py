from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_faculty_generic(html_content: str, base_url: str):
    """
    Generic faculty directory parser for card/list layouts.
    Looks for names, titles, emails, and profile links using common HTML patterns.
    Returns a list of RawLead dicts.
    """

    soup = BeautifulSoup(html_content, "lxml")
    raw_leads = []

    # Common containers for faculty listings
    containers = soup.select(
        ".faculty-card, .faculty, .person, .profile-card, .staff-card, li, .card"
    )

    for container in containers:
        name = None
        title = None
        email_raw = None
        profile_url = None
        socials = []
        bio_snippet = None

        # Try to find a name
        name_tag = container.select_one("h1, h2, h3, .faculty-name, .name")
        if name_tag:
            name = name_tag.get_text(strip=True)

        # Try to find a title
        title_tag = container.select_one(".faculty-title, .title, h4, p")
        if title_tag:
            title = title_tag.get_text(strip=True)

        # Try to find an email
        email_tag = container.select_one('a[href^="mailto:"]')
        if email_tag:
            email_raw = email_tag.get("href").replace("mailto:", "").strip()

        # Try to find a profile link
        link_tag = container.select_one("a[href]")
        if link_tag:
            href = link_tag.get("href")
            if href and not href.startswith("mailto:"):
                profile_url = urljoin(base_url, href)

        # Grab any obvious social links
        for a in container.select("a[href]"):
            href = a.get("href")
            if any(s in href.lower() for s in ["facebook", "twitter", "linkedin", "instagram"]):
                socials.append(href)

        # Grab a short bio snippet if present
        bio_tag = container.select_one(".bio, .description, p")
        if bio_tag:
            bio_snippet = bio_tag.get_text(strip=True)[:200]

        # Build raw lead dict if we have at least a name
        if name:
            raw_leads.append({
                "name": name,
                "title": title,
                "email_raw": email_raw,
                "profile_url": profile_url,
                "directory_url": base_url,
                "socials": socials,
                "bio_snippet": bio_snippet,
                "diagnostics": {
                    "source_strategy": "faculty_generic",
                    "confidence": 0.6  # base confidence, adjust if needed
                }
            })

    return raw_leads
