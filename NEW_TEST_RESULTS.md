# New Test Results - Wikipedia & Accusative Tests

**Date:** October 9, 2025  
**Tests Added:** 4 new test suites (60 additional test sentences)

---

## 📊 Test Suite Summary

### New Tests Added:

1. **ido-epo-wikipedia** (15 sentences)
   - Real sentences from Ido Wikipedia
   - Topics: science, geography, language, history
   
2. **epo-ido-wikipedia** (15 sentences)
   - Real sentences from Esperanto Wikipedia
   - Same topics as above for comparison

3. **ido-epo-accusative** (30 sentences)
   - Focused accusative case testing
   - Various word orders: SVO, OVS, SOV
   - Singular and plural objects
   
4. **epo-ido-accusative** (30 sentences)
   - Reverse direction accusative testing
   - Tests accusative removal (Epo→Ido)

**Total new tests:** 90 sentences  
**Previous tests:** 40 sentences  
**Grand total:** 130 test sentences

---

## 🐛 Critical Issues Discovered

### Issue 1: Accusative Case NOT Applied (Ido→Epo) 🔴 CRITICAL

**Problem:**
Direct objects are NOT receiving accusative -n ending in Esperanto.

**Examples:**
```
Input:  me vidas la kato
Output: mi vidas la kato       ❌ WRONG
Should: mi vidas la katon      ✓ CORRECT

Input:  me vidas la granda kato
Output: mi vidas la granda kato  ❌ WRONG
Should: mi vidas la grandan katon ✓ CORRECT

Input:  me amas la libri
Output: mi amas la libroj        ❌ WRONG
Should: mi amas la librojn       ✓ CORRECT
```

**Impact:** SEVERE - Grammatically incorrect Esperanto output  
**Scope:** ALL transitive verbs with direct objects  
**Priority:** 🔴 HIGHEST - Must fix before any submission

---

### Issue 2: Word Order Transfer Issues

**Problem:**
Object-first word order (OVS) not handled correctly.

**Examples:**
```
Input:  la kato me vidas  (OVS in Ido)
Output: la kato mi vidas  (OVS in Esperanto - OK but needs accusative!)
Should: la katon mi vidas (accusative marks the object)

Input:  la granda kato me vidas
Output: la granda kato mi vidas  ❌
Should: la grandan katon mi vidas ✓
```

**Impact:** HIGH - Ambiguous/incorrect word order  
**Priority:** 🔴 HIGH - Related to accusative issue

---

### Issue 3: Esperanto→Ido Direction Broken 🔴 CRITICAL

**Problem:**
Reverse direction completely non-functional.

**Examples:**
```
Input:  mi vidas la katon
Output: @mi vidas @la katon    ❌ All words unknown!

Input:  mi amas la libron
Output: @mi @ami @la libron    ❌ Complete failure
```

**Coverage:** ~0% (all @ markers)  
**Impact:** SEVERE - Direction unusable  
**Priority:** 🔴 HIGH (if bidirectional needed)

---

### Issue 4: Wikipedia Vocabulary Gaps

**Sample output:**
```
Input:  Matematiko esas la cienco pri nombri, spaco e strukturo.
Output: Matematiko estas la scienco pri nombroj, spaco kaj strukturon.
        ✓ Good! (minor accusative error on "strukturon")

Input:  La Tero esas la tria planeto de la sunala sistemo.
Output: La Tero estas la @tria planedo *de la *sunala sistemo.
        ⚠️ Missing: tria (ordinal), sunala (solar)

Input:  Paris esas la chefurbo di Francia.
Output: #Parizo estas la *chefurbo de #Francio.
        ⚠️ Missing: chefurbo (capital city)
```

**Missing common words:**
- Ordinals: tria (third)
- Adjectives: sunala (solar)
- Nouns: chefurbo (capital), planedo (planet), akvo (water)
- Names: Some proper nouns have # markers

---

## 📈 Test Results by Category

### Wikipedia Tests (Ido→Epo)

| Metric | Result | Notes |
|--------|--------|-------|
| Clean output | ~40% | Lower than general tests |
| # markers | ~25% | Proper nouns, some words |
| * passthrough | ~20% | Missing vocabulary |
| @ unknown | ~15% | Completely missing words |
| **Quality** | **~40%** | Much lower due to specific vocabulary |

**Conclusion:** Specialized vocabulary needs significant expansion.

---

### Accusative Tests (Ido→Epo)

| Test Type | Expected | Actual | Status |
|-----------|----------|--------|--------|
| SVO order | Accusative on object | No accusative | ❌ FAIL |
| OVS order | Accusative on object | No accusative | ❌ FAIL |
| Plural objects | Accusative -jn | Wrong/missing | ❌ FAIL |
| Adjective agreement | Agrees with object | Partial | ⚠️ PARTIAL |

**Success Rate:** 0% for core accusative functionality  
**Conclusion:** 🔴 Transfer rules NOT applying accusative case

---

### Accusative Tests (Epo→Ido)

| Test Type | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Remove accusative | Remove -n ending | All @ unknown | ❌ FAIL |
| Strip adjective case | Remove -jn → -j | All @ unknown | ❌ FAIL |

**Success Rate:** 0% (direction broken)  
**Conclusion:** 🔴 Epo→Ido dictionary completely missing

---

## 🔧 Root Cause Analysis

### Accusative Issue Root Cause:

The transfer rules in `apertium-ido-epo.ido-epo.t1x` are likely:

1. **Not detecting direct objects** - Pattern matching may not identify objects correctly
2. **Not applying case tags** - Rules exist but aren't triggering
3. **Generator doesn't add -n** - Even if tagged, generator may not apply ending

### Investigation Needed:

```bash
# Check if object is being identified
echo "me vidas la kato" | apertium -d . ido-epo-morph
echo "me vidas la kato" | apertium -d . ido-epo-biltrans
echo "me vidas la kato" | apertium -d . ido-epo-transfer

# Expected at transfer stage:
# Should have <acc> tag or similar for direct object
```

---

## ✅ What Worked Well

1. **Basic vocabulary** - Common words translate
2. **Number/case agreement** (where it works) - Adjectives agree when rules fire
3. **Conjunction "e"** → "kaj" - Fixed earlier, still working
4. **Word order preservation** - Structure maintained

---

## 🎯 Critical Next Steps

### BEFORE ANY SUBMISSION - Must Fix:

#### 1. Fix Accusative Case Transfer 🔴 URGENT
**Priority:** Highest  
**Time:** 2-4 hours  
**Action:**
- Review transfer rules in `.t1x` files
- Add/fix direct object detection
- Ensure accusative tag applied
- Test with all word orders

#### 2. Test Fix Comprehensively
**Priority:** High  
**Time:** 1 hour  
**Action:**
- Run all accusative tests
- Verify SVO, OVS, SOV word orders
- Check plural and singular
- Verify adjective agreement

#### 3. Add Missing Wikipedia Vocabulary
**Priority:** Medium  
**Time:** 2-3 hours  
**Action:**
- Add ordinals (1-100+)
- Add scientific terms (planedo, sistemo, etc.)
- Add common compounds (chefurbo, etc.)
- Test Wikipedia sentences again

#### 4. Decide on Epo→Ido Direction
**Priority:** Medium  
**Time:** Variable  
**Options:**
- A) Remove from submission (Ido→Epo only)
- B) Build separate dictionary (large effort)
- C) Mark as experimental/incomplete

---

## 📊 Updated Quality Assessment

### Previous Assessment: 82% ❌ INCORRECT

The 82% quality was based on limited tests that didn't thoroughly test accusative case.

### Revised Assessment: ~40-50% ⚠️

**Reasons for downgrade:**
1. ❌ Accusative case completely broken
2. ❌ Esperanto→Ido direction non-functional  
3. ⚠️ Wikipedia vocabulary gaps larger than expected
4. ✓ Basic grammar works (but missing critical feature)

---

## 🚨 Recommendation: DO NOT SUBMIT YET

**Reasons:**
1. 🔴 Accusative case is MANDATORY in Esperanto
2. 🔴 Current output is grammatically incorrect
3. 🔴 Quality much lower than initially assessed
4. 🔴 Would damage reputation if submitted in current state

**Required before submission:**
- ✅ Fix accusative case transfer (CRITICAL)
- ✅ Test all 130 test cases pass
- ✅ Verify grammatical correctness
- ✅ Add essential vocabulary
- ⚠️ Either fix or remove Epo→Ido direction

---

## 📝 Test Files Created

New test files in `/test/` directory:

1. `ido-epo-wikipedia-input.txt` (15 sentences)
2. `epo-ido-wikipedia-input.txt` (15 sentences)
3. `ido-epo-accusative-input.txt` (30 sentences)
4. `epo-ido-accusative-input.txt` (30 sentences)
5. `tests.json` (updated with 4 new test suites)

**Output files:**
- `test_accusative_ido_epo_results.txt`
- `test_wikipedia_ido_epo_results.txt`

---

## 🎯 Immediate Action Required

**Priority 1:** Fix accusative case transfer  
**Estimated time:** 2-4 hours  
**Blocker:** YES - Cannot proceed without this

Once accusative is fixed, quality should jump from 40% → 75-80%+ on these tests.

---

**Status:** Tests added ✅ | Critical issues discovered ✅ | Ready for fixes ⚠️

