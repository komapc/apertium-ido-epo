# Recommended Next Steps

**Date:** October 9, 2025  
**Current Quality:** 74% (Berlin article baseline)  
**Current State:** Functional translator, ready for testing

---

## Session Accomplishments ✅

Today we fixed **3 critical bugs** and improved coverage from 20% → 74%:

1. ✅ **Copula case agreement** - `guvernala sistemo` now stays nominative
2. ✅ **Number handling** - Years and quantities now pass through
3. ✅ **Past tense generation** - Biographical/historical content now works

---

## Priority 1: Fix Generation Markers 🔴 HIGH IMPACT

### Issue: # markers on known words (30% of output)

**Pattern:**
```
#la, #La, #Berlino, #Germanio, #estis, #havas, #Li, #Ĝi, #Post
```

**What it means:**  
These words ARE in dictionaries and ARE translating correctly, but Esperanto generator marks them with #.

### Root Cause Hypothesis:

The # marker typically means "word recognized but not in generation dictionary". Likely causes:

1. **Tag mismatch** - Input tag doesn't match generator paradigm
2. **Missing generation entries** - Some tags not in `apertium-epo.epo.dix`
3. **Capitalization** - Proper nouns might need special handling

### Investigation Steps:

```bash
cd /home/mark/apertium-dev/apertium-ido-epo

# Test what's happening with "la"
echo "^la<adj>$" | lt-proc -g ido-epo.autogen.bin
echo "^la<det>$" | lt-proc -g ido-epo.autogen.bin

# Test with "estis"
echo "^esti<vblex><pii>$" | lt-proc -g ido-epo.autogen.bin

# Test proper nouns
echo "^Berlino<np>$" | lt-proc -g ido-epo.autogen.bin
```

### Expected Impact:
- **Quality:** 74% → **85-90%**
- **Professional appearance:** Much cleaner output
- **User perception:** Major improvement

### Estimated Time: 2-3 hours

---

## Priority 2: Add High-Frequency Missing Vocabulary 🟡 MEDIUM IMPACT

### Issue: Common words missing (25% passthrough)

From test articles, most frequently needed words:

#### Must-Have Words (10-15 words):
1. **importanta** → grava (important)
2. **Hodie** → Hodiaŭ (today)
3. **fama** → fama (famous)
4. **teorio** → teorio (theory)
5. **lokalizesas** → situas (is located)
6. **loĝanto** → loĝanto (inhabitant) - fix plural
7. **distriko** → distrikto (district)
8. **duesma** → dua (second - ordinal)
9. **Mondala Milito** → Mondmilito (World War)
10. **oficejo** → oficejo (office)

#### Nice-to-Have (10 more):
11. **relativeso** → relativeco (relativity)
12. **nazii** → nazioj (Nazis)
13. **konstruktesar** → konstruiĝi (be constructed)
14. **Germaniana** → germana (German adjective)
15. **nordo-esto** → nordoriento (northeast)

### How to Add:

```bash
cd /home/mark/apertium-dev/ido-esperanto-extractor

# Create supplement
cat > common_words_supplement.json << 'EOF'
{
  "words": [
    {"ido_word": "importanta", "esperanto_words": ["grava"], "morfologio": ["important", ".a"]},
    {"ido_word": "Hodie", "esperanto_words": ["Hodiaŭ"], "morfologio": null},
    {"ido_word": "fama", "esperanto_words": ["fama"], "morfologio": ["fam", ".a"]},
    ...
  ]
}
EOF

# Apply and regenerate
python3 apply_supplement.py common_words_supplement.json
python3 json_to_dix_converter.py
cp *.dix ../apertium-ido-epo/
cd ../apertium-ido-epo && make
```

### Expected Impact:
- **Quality:** 74% → **80-85%**
- **Coverage:** Most common words covered
- **Usability:** Significantly improved

### Estimated Time: 1-2 hours

---

## Priority 3: Fix Conjunction "e" ⚠️ LOW-MEDIUM IMPACT

### Issue: "e" sometimes marked with *

**Pattern:**
```
kulturo, politiko e ekonomio → kulturo, politiko *e ekonomio
```

**Expected:**
```
kulturo, politiko e ekonomio → kulturo, politiko kaj ekonomio
```

### Why it happens:
The conjunction "e" (and) should always map to "kaj", but sometimes gets marked as unknown.

### Investigation:

```bash
# Check if "e" is in dictionary
echo "e" | lt-proc ido-epo.automorf.bin
echo "^e<cnjcoo>$" | lt-proc -b ido-epo.autobil.bin
```

### Expected Impact:
- **Quality:** 74% → **76%**
- **Professional appearance:** Cleaner lists

### Estimated Time: 30 minutes

---

## Priority 4: Add Compound Word Support ⚠️ MEDIUM IMPACT

### Issue: Compounds marked with *

**Examples:**
- `chefurbo` → `*chefurbo` (should be: `ĉefurbo`)
- `patento-oficejo` → `patento-*oficejo`
- `Mondala Milito` → `*Mondala Milito`
- `nordo-esto` → `nordo-eosto`

### Solutions:

**Option A: Add common compounds directly**
```json
{
  "ido_word": "chefurbo",
  "esperanto_words": ["ĉefurbo"],
  "note": "capital city (compound: chief + city)"
}
```

**Option B: Add morphological analyzer rules**
- Recognize `chef-` prefix → `ĉef-`
- Recognize `-urbo`, `-oficejo` as compound parts

**Recommendation:** Option A (simpler, faster) - add ~20 most common compounds

### Expected Impact:
- **Quality:** 74% → **77-78%**
- **Accuracy:** Better for technical/administrative text

### Estimated Time: 1-2 hours

---

## Priority 5: Create Comprehensive Test Suite ✅ IMPORTANT

### What we have:
- ✅ `test_republiko.txt` - Political/abstract (83% quality)
- ✅ `test_kazakstan.txt` - Geographic/present (50% quality)
- ✅ `test_einstein.txt` - Biographical/past (60% quality)
- ✅ `test_berlin.txt` - Mixed content (74% quality)

### What to add:

**Diverse content types:**
1. Scientific article (physics, chemistry, biology)
2. Literature/narrative (stories, descriptions)
3. News article (current events)
4. Technical documentation
5. Conversation/dialogue

### Test automation:

```bash
# Create test runner
cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "Running translation test suite..."
for file in test_*.txt; do
    echo "Testing: $file"
    apertium -d . ido-epo < "$file" > "output_${file}"
    # Analyze coverage
    coverage=$(grep -o '#' "output_${file}" | wc -l)
    echo "  # markers: $coverage"
done
EOF
chmod +x run_tests.sh
```

### Expected Impact:
- **Regression detection:** Catch bugs before they reach users
- **Coverage measurement:** Track improvement over time
- **Quality assurance:** Systematic testing

### Estimated Time: 2-3 hours

---

## Priority 6: Optimize for Real-World Use 🟢 POLISH

### Current Issues for Production:

1. **Remove .md clutter** - We have 5-6 .md files
   - Keep: README.md only
   - Archive: Others to /docs folder

2. **Add usage examples** to README

3. **Create installation script**

4. **Add pre-commit hooks** for testing

### Expected Impact:
- **User experience:** Much better
- **Adoption:** Easier for others to use

### Estimated Time: 1-2 hours

---

## Summary Table

| Priority | Task | Impact | Time | Difficulty |
|----------|------|--------|------|------------|
| 🔴 **P1** | Fix # generation markers | High (74%→85%) | 2-3h | Medium |
| 🟡 **P2** | Add common vocabulary | Medium (74%→80%) | 1-2h | Easy |
| ⚠️ **P3** | Fix conjunction "e" | Low (74%→76%) | 30m | Easy |
| ⚠️ **P4** | Add compound words | Medium (74%→78%) | 1-2h | Easy |
| ✅ **P5** | Test suite | Quality assurance | 2-3h | Easy |
| 🟢 **P6** | Production polish | User experience | 1-2h | Easy |

---

## Recommended Action Plan

### This Week (Quick Wins):

**Day 1:** (2-3 hours)
1. Fix # generation markers (P1) - **Highest impact**
2. Fix conjunction "e" (P3) - **Quick win**

**Day 2:** (2-3 hours)
3. Add 20 high-frequency words (P2)
4. Add 15 common compounds (P4)

**Day 3:** (2-3 hours)
5. Create test suite (P5)
6. Polish for production (P6)

### Next Week:

7. Extract more from Idolinguo (full 7,206 words)
8. Add constraint grammar for disambiguation
9. Test with real users
10. Gather feedback and iterate

---

## Immediate Quick Wins (Can do in <1 hour)

If you only have 30-60 minutes:

### Option A: Add Top 10 Missing Words
```bash
cd /home/mark/apertium-dev/ido-esperanto-extractor
# Add: importanta, Hodie, fama, teorio, oficejo, etc.
# Regenerate and test
```
**Impact:** +5% coverage

### Option B: Fix Conjunction "e"
```bash
# Investigate why "e" marked
# Add proper bilingual entry
# Test
```
**Impact:** Cleaner output

### Option C: Add Test Automation
```bash
# Create test runner script
# Run on all 4 test files
# Document baseline
```
**Impact:** Quality assurance

---

## Expected Final Quality

If all priorities completed:

| After... | Quality | Status |
|----------|---------|--------|
| **Current** | 74% | Functional |
| **P1 (# markers)** | 85% | Very good |
| **P2 (vocab)** | 88% | Excellent |
| **P3+P4 (polish)** | **90%+** | Professional |

---

## My Recommendation

**Start with Priority 1 (Fix # markers)** - This has the highest impact and will make the translator look much more professional.

The # markers are the most visible issue to users. Once fixed, the translator will produce much cleaner output even with the same vocabulary coverage.

**Then Priority 2 (Add top 20 words)** - Low effort, good return.

**Save testing/polish for last** - These are important but lower urgency.

---

## Questions to Consider

1. **What's your target use case?**
   - General purpose? → Focus on vocabulary breadth
   - Specific domain? → Focus on that domain's vocabulary
   - Demo/showcase? → Focus on # marker fix (looks better)

2. **What's your timeline?**
   - Few hours? → P1 + P2 (quick wins)
   - Few days? → All priorities
   - Ongoing? → Systematic vocabulary expansion

3. **What's your quality target?**
   - 80%? → P1 + P2
   - 90%? → All priorities + more vocabulary
   - 95%? → + Constraint grammar + extensive testing

---

## Current Status Report

**What works excellently:**
- ✅ Grammar (copula, case, agreement)
- ✅ Past tense (biographical content)
- ✅ Numbers (years, quantities)
- ✅ Core vocabulary (politics, geography)
- ✅ Complex sentences

**What needs improvement:**
- ⚠️ Generation markers (cosmetic)
- ⚠️ Vocabulary gaps (addressable)
- ⚠️ Compound words (systematic)

**Overall assessment:**
The translator has gone from **barely functional (20%)** to **very good (74%)** in one session. The foundation is solid. Now it's about polish and vocabulary expansion.

---

## What Would You Like to Tackle Next?

1. **Fix # markers** (highest visual impact)
2. **Add more vocabulary** (improve coverage)
3. **Create test suite** (quality assurance)
4. **Polish for production** (user experience)
5. **Something else?**

Let me know which direction you'd like to take!


