# Improvements Needed - Priority List

**Date:** October 9, 2025  
**Current Quality:** 67% average  
**Target Quality:** 85-90%

---

## 🔴 CRITICAL PRIORITY 1: Fix Pronoun Generation (1-2 hours)

### Issue:
Personal pronouns generate with # marker:
```
me → #mi (I)
ni → #ni (we)  
il → #li (he)
```

### Root Cause:
Esperanto monolingual generator (`apertium-epo.epo.dix`) missing proper pronoun generation forms.

### Impact:
- 25+ occurrences across tests
- Affects 37% of sentences
- Pronouns are in EVERY sentence

### Solution:
**File to modify:** `apertium-epo/apertium-epo.epo.dix`

Add generation paradigms for personal pronouns or fix existing ones.

**Alternative (if can't modify apertium-epo):**
- Note: We may not have write access to apertium-epo official repo
- Could fork and maintain local copy
- Or document as known issue

### Expected Impact:
67% → 78% quality (+11%)

---

## 🔴 CRITICAL PRIORITY 2: Add Missing Common Verbs (30 min)

### Missing Verbs:

| Ido | Esperanto | Occurrences | Priority |
|-----|-----------|-------------|----------|
| amar | ami | 4 | 🔴 High |
| konar | koni | 2 | 🔴 High |
| studar | studi | 2 | 🟡 Medium |
| kurar | kuri | 2 | 🟡 Medium |
| instruar | instrui | 1 | 🟡 Medium |

### Solution:
Add to `apertium-ido-epo.ido-epo.dix`:
```xml
<e><p><l>ami<s n="vblex" /></l><r>amar<s n="vblex" /></r></p></e>
<e><p><l>koni<s n="vblex" /></l><r>konar<s n="vblex" /></r></p></e>
<e><p><l>studi<s n="vblex" /></l><r>studar<s n="vblex" /></r></p></e>
<e><p><l>kuri<s n="vblex" /></l><r>kurar<s n="vblex" /></r></p></e>
<e><p><l>instrui<s n="vblex" /></l><r>instruar<s n="vblex" /></r></p></e>
```

### Expected Impact:
Current → +2-3% quality

---

## 🟡 HIGH PRIORITY 3: Fix Common Verb Generation (1 hour)

### Issue:
Common verbs like "havas" generate with #:
```
me havas → #mi #havas
```

### Root Cause:
Similar to pronouns - generation issue in apertium-epo

### Solution:
Fix in `apertium-epo.epo.dix` or document limitation

### Expected Impact:
+1-2% quality

---

## 🟡 MEDIUM PRIORITY 4: Add Wikipedia Vocabulary (2-3 hours)

### Top 20 Missing Words:

**Scientific/Academic (10 words):**
1. naturala → natura (natural)
2. celestala → ĉiela (celestial)
3. sunala → suna (solar)
4. planedo → planedo (planet)
5. linguajo → lingvaĵo (language)
6. plusa → pli (more)
7. materio → materio (matter)
8. relateso → rilato (relationship)
9. fenomeni → fenomenoj (phenomena)
10. objekti → objektoj (objects)

**Geographic/Common (10 words):**
11. chefurbo → ĉefurbo (capital city)
12. akvo → akvo (water)
13. buliar → boli (to boil)
14. domestikigita → hejmigita (domesticated)
15. apartenas → aparteni (belongs)
16. mamifero → mamulo (mammal)
17. konektita → konektita (connected)
18. kreita → kreita (created)
19. parlata → parolata (spoken)
20. familio → familio (family)

### Solution:
Add to bilingual dictionary via extractor scripts

### Expected Impact:
+8-10% quality on Wikipedia content

---

## ⚠️ LOW PRIORITY 5: Fix Relative Pronoun "kiu" (30 min)

### Issue:
```
la hundo kiu apartenas → la hundo #kiu apartenas
```

### Impact:
4 occurrences, affects relative clauses

### Solution:
Fix generation in apertium-epo or add mapping

### Expected Impact:
+1% quality

---

## ⚠️ LOW PRIORITY 6: Add Pronoun "elu" (15 min)

### Issue:
```
elu → *elu (she - not in dictionary)
```

### Impact:
4 occurrences

### Solution:
Add to dictionaries:
```xml
<e><p><l>ŝi<s n="prn" /></l><r>elu<s n="prn" /></r></p></e>
```

### Expected Impact:
+1% quality

---

## 🚀 IMPROVEMENT: Add Test Expected Outputs (1-2 hours)

### Current State:
Tests only have input files, no expected output for automated comparison

### Improvement:
Create expected output files:
```
test/ido-epo-basic-input.txt
test/ido-epo-basic-expected.txt ← NEW
```

### Benefits:
- ✅ Automated pass/fail testing
- ✅ Regression detection
- ✅ Quality tracking over time
- ✅ CI/CD integration ready

### Implementation:
1. Generate current "best" outputs
2. Manually review and correct
3. Save as expected.txt files
4. Update tests.json with expected outputs

---

## 📈 Quality Improvement Roadmap

### Current: 67%

| After... | Quality | Improvement | Time | Effort |
|----------|---------|-------------|------|--------|
| Add verbs (P2) | 70% | +3% | 30m | Easy |
| Fix pronouns (P1) | 78% | +8% | 2h | Medium |
| Fix verb gen (P3) | 80% | +2% | 1h | Medium |
| Add Wikipedia vocab (P4) | 88% | +8% | 3h | Easy |
| Fix kiu (P5) | 89% | +1% | 30m | Easy |

**Total to 88%:** 7 hours of work

---

## 💡 Quick Wins (Can do NOW - 30 min)

### Quick Win 1: Add 5 Missing Verbs
**Time:** 20 minutes  
**Impact:** +2-3%  
**Difficulty:** Easy

**Action:**
```bash
cd /home/mark/apertium-dev/ido-esperanto-extractor
# Edit dictionary_merged.json
# Add: amar→ami, konar→koni, studar→studi, kurar→kuri, instruar→instrui
# Regenerate
python3 json_to_dix_converter.py
cp *.dix ../apertium-ido-epo/
cd ../apertium-ido-epo && make
```

---

### Quick Win 2: Add Pronoun "elu"
**Time:** 10 minutes  
**Impact:** +1%  
**Difficulty:** Very easy

**Action:**
```bash
# Add to bilingual dictionary
<e><p><l>ŝi<s n="prn" /></l><r>elu<s n="prn" /></r></p></e>
```

---

## 🎯 Recommended Approach

### Option A: Quick Improvement (1 hour today)
1. Add 5 missing verbs (20 min)
2. Add pronoun "elu" (10 min)
3. Add top 10 Wikipedia words (30 min)

**Result:** 67% → 72-75%  
**Effort:** Low  
**Timeline:** Today

---

### Option B: Major Fix (2-3 hours tomorrow)
1. Fix pronoun generation in apertium-epo (2 hours)
2. Add missing verbs (20 min)
3. Test comprehensively (30 min)

**Result:** 67% → 80-82%  
**Effort:** Medium  
**Timeline:** Tomorrow  
**Challenge:** Need to modify apertium-epo (may not have permissions)

---

### Option C: Vocabulary Focus (3-4 hours this week)
1. Add 50 Wikipedia terms (2 hours)
2. Add missing verbs (30 min)
3. Add function words (30 min)
4. Test and document (1 hour)

**Result:** 67% → 78-80%  
**Effort:** Medium  
**Timeline:** This week  
**Benefit:** Better domain coverage

---

## 🔍 Test Insights

### What Tests Revealed:

**Good News:**
- ✅ Accusative case works (73% in dedicated tests)
- ✅ Basic grammar works (70%)
- ✅ No critical @unknown in basic tests
- ✅ Transfer rules functioning correctly

**Bad News:**
- ❌ Pronoun generation broken (#mi everywhere)
- ❌ Some verb forms missing
- ❌ Wikipedia vocabulary gaps larger than expected

**Neutral:**
- ⚠️ Quality varies by domain (59-73%)
- ⚠️ Expected outputs needed for automation

---

## 📝 Specific Improvements to Tests

### 1. Add Expected Outputs
Create files like:
```
test/ido-epo-basic-expected.txt:
mi havas katon
mi havas grandan katon
la kato estas bela
...
```

### 2. Add Pass/Fail Criteria
Define acceptable error thresholds:
```json
{
  "ido-epo-basic": {
    "input": "ido-epo-basic-input.txt",
    "expected": "ido-epo-basic-expected.txt",
    "mode": "ido-epo",
    "max_errors": 5,
    "min_quality": 70
  }
}
```

### 3. Add Test Categories
Missing test types:
- Negation tests
- Question tests
- Imperative tests
- Complex sentences (multiple clauses)
- Idioms/phrases

### 4. Create Minimal Smoke Test
**Purpose:** Quick pre-commit check  
**Size:** 10-15 critical sentences  
**Coverage:** Core grammar + accusative + common words

---

## 🎯 My Recommendation

**Do Option A (Quick Wins) TODAY:**

1. ✅ Add 5 missing verbs (20 min) ← Easy, immediate impact
2. ✅ Add pronoun "elu" (10 min) ← Easy
3. ✅ Add top 10 Wikipedia words (30 min) ← Easy

**Result:** 67% → 73-75% in 1 hour of work

**Then document pronoun generation issue as "known limitation" for v0.1.0**

This gives you:
- ✅ Improved quality fast
- ✅ Can submit sooner
- ✅ Defer hard problems (pronoun generation) to v0.2.0

---

**Status:** Tests complete ✅ | Analysis done ✅ | Plan ready ✅

