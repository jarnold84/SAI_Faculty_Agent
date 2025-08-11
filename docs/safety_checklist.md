
# Scraping Agent #1 - Safety Checklist

*Reference this document before every proposed change*

## 🔒 MANDATORY Pre-Change Checks

### 1. **Golden Fixture Protection** (CRITICAL)
```bash
# ALWAYS run this first
python -m pytest tests/test_golden_fixtures.py::test_fresno_music_golden_fixture -v
```
- **MUST PASS** before any change
- If fails, **STOP** and investigate immediately
- This protects our locked 36-faculty extraction from Fresno State

### 2. **Import System Safety**
```bash
# Test all imports work
python -c "import sys; sys.path.append('.'); from api.server import scrape_faculty_directory; print('✅ All imports working')"
```
- Check for circular imports
- Verify no missing dependencies

### 3. **Port/Process Management**
```bash
# Kill any stuck processes
pkill -f "uvicorn\|python.*main.py" 2>/dev/null || true
```
- Always clean up before testing
- Port 5000 is our standard (configured for Replit)

---

## 📋 Change Type Checklists

### Strategy Changes (extract/strategies/)
- [ ] Backup current commit: `git log --oneline -1`
- [ ] Run golden fixture test (must pass)
- [ ] Test import system
- [ ] Changes must not affect other strategies
- [ ] Test with Fresno State fixture after change
- [ ] Shared code goes in utilities only

### Schema Changes (schemas/)
- [ ] **CRITICAL**: Can break Make.com integration
- [ ] Test existing API responses still validate
- [ ] Update tests if schema fields change
- [ ] Consider versioning if breaking changes
- [ ] Check normalization logic compatibility

### API Changes (api/server.py)
- [ ] Maintain backward compatibility in JSON structure
- [ ] Test with actual curl commands
- [ ] Verify /health and /scrape endpoints work
- [ ] Check response format matches expectations

### Normalization Changes (normalize/)
- [ ] Test with multiple data formats
- [ ] Email status tracking must remain consistent
- [ ] Run golden fixture to verify no regressions
- [ ] Test edge cases (empty data, malformed emails)

---

## 🚨 HIGH-RISK Areas

### NEVER Touch Without Explicit Request
- [ ] `.replit` file (port configurations)
- [ ] `pyproject.toml` (dependencies)
- [ ] `main.py` port settings (5000 is standard)

### Approach With Extreme Caution
- [ ] Strategy loading logic
- [ ] Email status classification
- [ ] JSON response structure
- [ ] Test fixture files

---

## 🛡️ Validation Steps

### After EVERY Change
```bash
# 1. Smoke test
python -m pytest tests/test_smoke.py -v

# 2. Golden test (CRITICAL)
python -m pytest tests/test_golden_fixtures.py -v

# 3. Import test
python -c "from main import app; print('✅ App imports OK')"

# 4. Server start test
python main.py &
sleep 3
curl http://localhost:5000/health
pkill -f "python main.py"
```

### Success Criteria - ALL Must Pass
- [ ] All existing tests green
- [ ] Golden fixture extracts 36 items from Fresno State
- [ ] API response schema unchanged (unless explicitly modified)
- [ ] Server starts without errors
- [ ] No new import/syntax errors

---

## 🔄 Recovery Procedures

### If Golden Test Fails
```bash
# STOP immediately
git status
git log --oneline -5

# Find last working commit
# Revert to it
git reset --hard [LAST_WORKING_COMMIT]

# Verify recovery
python -m pytest tests/test_golden_fixtures.py -v
```

### If Server Won't Start
```bash
# 1. Kill processes
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# 2. Check syntax
python -m py_compile main.py

# 3. Test imports
python -c "from main import app"

# 4. Check for port conflicts
netstat -tlnp | grep :5000
```

### If Imports Break
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test each module
python -c "import api.server"
python -c "import extract.strategies.directory_table"
python -c "import normalize.normalize"
```

---

## ⚡ Emergency Commands

### Quick Status Check
```bash
# Full system check
echo "=== Git Status ==="
git status --short
echo "=== Last Commits ==="
git log --oneline -3
echo "=== Golden Test ==="
python -m pytest tests/test_golden_fixtures.py::test_fresno_music_golden_fixture -v
echo "=== Import Test ==="
python -c "from main import app; print('✅ All systems OK')"
```

### Quick Recovery Template
```bash
# Emergency rollback
git stash  # Save current work
git reset --hard [KNOWN_GOOD_COMMIT]
python -m pytest tests/test_golden_fixtures.py -v  # Verify
```

---

## 🎯 Key Safety Principles

1. **Golden Fixture is Sacred** - Never break Fresno State test
2. **Small Atomic Changes** - One thing at a time
3. **Test Before Commit** - All checks must pass
4. **Know Your Rollback** - Always have escape route
5. **Fail Fast** - If tests fail, stop and investigate

---

## 📊 Change Impact Matrix

| Change Type | Risk Level | Required Tests | Recovery Time |
|-------------|------------|----------------|---------------|
| Strategy tweak | 🟡 Medium | Golden + Imports | 5 min |
| Schema change | 🔴 High | All tests + API | 15 min |
| New strategy | 🟢 Low | Golden + Strategy | 10 min |
| API endpoint | 🔴 High | All tests + Manual | 20 min |
| Normalizer | 🟡 Medium | Golden + Data tests | 10 min |

---

## 🔍 Before You Start Checklist

- [ ] I know what I'm changing and why
- [ ] I have the current working commit hash
- [ ] Golden test is currently passing
- [ ] I understand the rollback procedure
- [ ] I've allocated time for proper testing
- [ ] I won't modify high-risk files unless requested

---
## 🤖 AI Assistant Safety Protocol

### Before Accepting Any AI Suggestion
- [ ] Ask: "Does this change anything currently working?"
- [ ] Verify: AI explains what files will be modified
- [ ] Confirm: Change is minimal and targeted
- [ ] Demand: Explicit safety check confirmation

### Red Flags in AI Responses
- ❌ "Let me rewrite the entire function"
- ❌ "I'll improve the overall architecture" 
- ❌ Multiple files changed at once
- ❌ No mention of golden fixture impact
- ✅ "This only adds X to file Y, preserving all existing functionality"

### AI Prompt Templates
"Before suggesting any changes, please:
1. Check if this affects the golden fixture
2. Explain which files you'll modify
3. Confirm this is the minimal change needed
4. Verify backward compatibility"

---
## ⏱️ Session Time Management

### Stopping Criteria (Prevent Over-Engineering)
- [ ] After 3 failed attempts, take a break
- [ ] If golden test fails twice, end session
- [ ] After 45 minutes on one problem, document and move on
- [ ] If feeling frustrated, commit current progress and stop

### Session Success Definition
- ✅ One working improvement validated by tests
- ✅ Golden fixture still passing
- ✅ System in deployable state
- ✅ Progress documented


---
## 🚩 Feature Flag Requirements

### Every New Feature Must Be
- [ ] Behind a feature flag (default: OFF)
- [ ] Testable in isolation
- [ ] Removable without breaking existing code
- [ ] Validated with golden fixtures

### Before Enabling Any Flag
- [ ] Test with flag OFF (ensure no regression)
- [ ] Test with flag ON (ensure improvement)
- [ ] Document performance impact
- [ ] Define rollback criteria

---
## 👁️ Self-Review Before Committing

### Code Quality Gates
- [ ] Is this the simplest solution that works?
- [ ] Did I add complexity without clear benefit?
- [ ] Can someone else understand this in 6 months?
- [ ] Are there more than 20 lines changed?
- [ ] Am I solving the actual problem or a theoretical one?

### If Yes to Any Red Flags, STOP
- ❌ "I'll optimize this while I'm here"
- ❌ "Let me clean up this other function too"
- ❌ "I should make this more general purpose"
- ❌ "This would be better with a different architecture"

---
## 🎯 Multi-Site Validation (Prevent Single-Site Optimization)

### Tiered Testing Strategy

#### Tier 1: Core Stability (Golden Fixtures - MUST NEVER BREAK)
- [ ] Fresno State Music Faculty (directory_table strategy)
- [ ] [Add 2-3 more locked golden fixtures as you find reliable sites]
- **Requirement**: 100% success rate (any failure = immediate rollback)

#### Tier 2: Strategy Validation (Representative Site Types)
- [ ] JSON-LD structured data site (schema.org markup)
- [ ] HTML table-based directory 
- [ ] Card/grid layout site
- [ ] List-based faculty directory
- [ ] Paginated directory (multi-page)
- [ ] JavaScript-rendered directory
- **Requirement**: 80%+ success rate across all strategy types

#### Tier 3: Diversity Testing (Real-World Variety)
- [ ] Large state universities (100+ faculty)
- [ ] Small liberal arts colleges (10-20 faculty)
- [ ] Music conservatories (specialized layouts)
- [ ] Community colleges (different CMS systems)
- [ ] International universities (different naming patterns)
- **Requirement**: 70%+ success rate across institution types

#### Tier 4: Edge Case Testing (Stress Testing)
- [ ] Sites with unusual HTML structures
- [ ] Multi-language faculty names
- [ ] Sites with heavy obfuscation/anti-bot measures
- [ ] Broken or incomplete faculty listings
- [ ] Sites requiring specific headers/user agents
- **Requirement**: 60%+ success rate, graceful failure handling

### Testing Frequency by Development Phase

#### Phase 1 (Current): Foundation
- **Run**: Tier 1 (every change) + Tier 2 (weekly)
- **Target**: 2-3 golden fixtures, 5-8 strategy validation sites
- **Success**: No golden fixture failures, 80%+ on strategy validation

#### Phase 2: Robustness  
- **Run**: Tier 1 (every change) + Tier 2 (every change) + Tier 3 (weekly)
- **Target**: 5 golden fixtures, 15-20 diversity testing sites
- **Success**: 100% golden, 85%+ strategy, 70%+ diversity

#### Phase 3: Production Ready
- **Run**: All tiers (automated testing)
- **Target**: 100+ total test sites across all tiers
- **Success**: 100% golden, 90%+ strategy, 80%+ diversity, 60%+ edge cases

### Acceptance Criteria by Scale

#### Early Development (20+ sites)
- [ ] All golden fixtures pass (100%)
- [ ] At least 4 different strategy types working
- [ ] No more than 3 total failures in Tier 2+3 combined
- [ ] Document failure patterns for future improvement

#### Mid Development (50+ sites)
- [ ] All golden fixtures pass (100%)
- [ ] 85%+ success rate across Tier 2 (strategy validation)
- [ ] 75%+ success rate across Tier 3 (diversity testing)
- [ ] Failure analysis shows clear improvement patterns

#### Production Ready (100+ sites)
- [ ] All golden fixtures pass (100%)
- [ ] 90%+ success rate across Tier 2
- [ ] 80%+ success rate across Tier 3  
- [ ] 60%+ success rate across Tier 4
- [ ] Comprehensive failure categorization and handling

### Batch Testing Protocol

#### Quick Validation (After each change)
```bash
# Test golden fixtures only (fast)
python -m pytest tests/test_golden_fixtures.py -v

---
## 🛑 STOP CONDITIONS (Immediate Session End)

### Mandatory Session Termination If:
- [ ] Golden test fails more than once
- [ ] Same error repeats 3+ times
- [ ] Feeling pressured to "just make it work"
- [ ] Making changes to fix previous changes
- [ ] Can't explain the problem in one sentence
- [ ] Working for >2 hours without clear progress

### Recovery Protocol:
1. Commit any working progress
2. Document the attempted approach
3. Note what you learned
4. Schedule next session with fresh perspective

*This checklist has prevented multiple regression cycles. Follow it religiously.*
