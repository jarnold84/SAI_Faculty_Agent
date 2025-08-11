# Changelog

All notable changes to Scraping Agent #1 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planning for Phase 1 completion: more golden fixtures, email enrichment, success rate evaluation

## [0.1.0] - 2024-01-15 - Working Foundation

### Added
- Complete FastAPI server with `/scrape` endpoint working locally and deployed
- Stable JSON response schema (`NormalizedLead`/`ScrapeResponse`) with Pydantic validation
- Core analyzer for basic strategy selection (`analyze/plan.py`)
- HTTP fetcher with retries and timeout (`fetch/http.py`)
- JSON-LD Person extraction strategy (`extract/strategies/json_ld.py`)
- Directory table parsing strategy (`extract/strategies/directory_table.py`)
- First golden fixture: Fresno State Music Faculty directory (36 faculty members)
- Pytest test framework with smoke tests and golden fixture tests
- Basic email normalization and status tracking
- Deployment configuration fixed for Replit

### Fixed
- Deployment configuration: switched from `python3 main.py` to `uvicorn main:app --host 0.0.0.0 --port 5000`
- Port binding for external accessibility on deployed endpoint

### Testing
- Golden fixture test passing: `test_fresno_music_golden_fixture()`
- Smoke tests passing for all core endpoints
- Local and deployed health checks working
- Success rate: 100% on our test fixture (36/36 faculty extracted)

### Architecture Decisions
- Strategy pattern implementation working with fallback chain
- Feature flags structure in place for future expensive operations
- Golden fixtures approach preventing regressions
- Timeboxed development approach successful

## [0.0.1] - 2024-01-15 - Initial Setup

### Added
- Project structure planning
- Visual architecture maps with Mermaid diagrams
- Component specifications and contracts
- Build checklist and phase planning
- Testing strategy with fixtures approach
- Replit project structure with all required folders
- Basic Flask app placeholder

### Documentation
- `docs/overview.md` - Complete system architecture
- `docs/progress.md` - Daily progress tracking
- `CHANGELOG.md` - This file

### Architecture Decisions
- Strategy pattern for extraction methods
- Feature flags for expensive operations
- Golden fixtures for regression prevention
- Timeboxed development to avoid loops

### Next Steps
- Install project dependencies (FastAPI, BeautifulSoup, Pydantic, Playwright)
- Create Pydantic schemas for data validation
- Build `/scrape` endpoint in `api/server.py`
- Set up pytest test framework
- Begin URL analyzer implementation

---

## Release Templates

### When we complete Phase 0
```markdown
## [0.1.0] - [Date] - Working Foundation

### Added
- Basic FastAPI server with /scrape endpoint
- Stable JSON response schema (NormalizedLead/ErrorEnvelope)
- Core analyzer for strategy selection
- HTTP fetcher with retries and timeout
- Schema validation with Pydantic
- Basic test framework setup

### Fixed
- N/A (initial release)

### Changed
- N/A (initial release)

### Testing
- Smoke test passes
- Basic endpoint responds correctly
- Error handling returns proper envelopes
```

### When we complete Phase 1
```markdown
## [0.2.0] - [Date] - Core Parsing

### Added
- JSON-LD Person extraction strategy
- Directory table parsing strategy
- Basic email normalization
- First golden fixtures captured
- Strategy registry system

### Fixed
- [Any bugs found and fixed]

### Changed
- [Any breaking changes to schemas/APIs]

### Testing
- X golden fixtures locked in
- Success rate: X% on test URLs
- Strategy isolation tests passing
```

---

## Green Path Tracking

*This section tracks what's working and must not be broken by future changes.*

### ✅ Locked Green Paths

### ✅ Directory Table Strategy (Locked)
- **Site**: Fresno State Music Faculty Directory
- **Fixture**: `fixtures/fresno_music_success.html` + `fresno_music_success.expected.json`
- **Items**: 36 faculty members extracted
- **Test**: `test_golden_fixtures.py::test_fresno_music_golden_fixture`
- **Must Not Break**: Names, titles, profile URLs all present; email status tracking working
- **API Status**: ✅ Working locally and deployed on Replit

### 🚨 Regression Watch
*Features that have broken before and need extra attention*

---

## Known Issues

### Current
*None yet*

### Resolved
*Will track bug fixes here*

---

## Future Releases (Planned)

### v0.3.0 - Robustness
- Profile card extraction
- Better email obfuscation handling
- Expanded fixture library
- Target: 70-80% success rate

### v0.4.0 - Pagination
- Multi-page directory support
- Profile enrichment (behind flag)
- Rate limiting and politeness
- Target: 80-85% success rate

### v0.5.0 - JavaScript Support
- Playwright integration
- SPA/React directory support
- JS rendering behind feature flag
- Target: 85-90% success rate

### v1.0.0 - Production Ready
- Comprehensive evaluation harness
- 90%+ success rate on canary set
- Full error categorization
- Production deployment ready