# Einstein Article Translation Analysis

**Source:** [Ido Wikipedia - Albert Einstein](https://io.wikipedia.org/wiki/Albert_Einstein)  
**Date:** October 9, 2025  
**Test:** Biographical content translation analysis

---

## Test Sentences (8 biographical statements)

### Sentence 1: Birth and nationality
```
IDO: Albert Einstein esis Germaniana fizikisto qua viveskis en 1879-1955.
ESP: #unknown #unknown #default #unknown *fizikisto #kiu #unknown en #unknown-#unknown.
EXP: Albert Einstein estis germana fizikisto kiu vivis en 1879-1955.
```

**Issues:**
- ❌ `Albert Einstein` → `#unknown #unknown` (proper name)
- ❌ `esis` → `#default` (past tense of "esar" - to be)
- ❌ `Germaniana` → `#unknown` (German adjective)
- ⚠️ `fizikisto` → `*fizikisto` (physicist - partially recognized)
- ✅ `qua` → `#kiu` (who - relative pronoun recognized)
- ❌ `viveskis` → `#unknown` (lived - past tense)
- ❌ `1879-1955` → `#unknown-#unknown` (year range not handled)

**Grammar:** ⚠️ Structure preserved but verbs not working

---

### Sentence 2: Fame and century
```
IDO: Il esis la maxim fama fizikisto di la 20ma yarcento.
ESP: #Li #default #la plej @fama #unknown de #la dudeka jarcento.
EXP: Li estis la plej fama fizikisto de la 20-a jarcento.
```

**Issues:**
- ⚠️ `Il` → `#Li` (he - pronoun recognized but marked)
- ❌ `esis` → `#default` (was - verb issue)
- ✅ `maxim` → `plej` (most - WORKS! superlative)
- ❌ `fama` → `@fama` (famous - not in dictionary)
- ❌ `fizikisto` → `#unknown` (physicist)
- ✅ `di` → `de` (of - preposition works)
- ✅ `20ma` → `dudeka` (20th - ordinal works!)
- ✅ `yarcento` → `jarcento` (century - WORKS!)

**Grammar:** ✅ Good! Structure correct

**Positive:** Several words working well

---

### Sentence 3: Theory of relativity
```
IDO: Einstein publikigis la teorio di relativeso en 1905.
ESP: #unknown *publikigis #la #unknown de #unknown en #unknown.
EXP: Einstein publikigis la teorion de relativeco en 1905.
```

**Issues:**
- ❌ `Einstein` → `#unknown`
- ⚠️ `publikigis` → `*publikigis` (published - partially recognized)
- ❌ `teorio` → `#unknown` (theory)
- ❌ `relativeso` → `#unknown` (relativity)
- ❌ `1905` → `#unknown` (year)

---

### Sentence 4: Nobel Prize
```
IDO: Il recevis la Nobel-premio por fiziko en 1921.
ESP: #Li #ricevi #la #Nobel-premio *por fiziko en #unknown.
EXP: Li ricevis la Nobel-premion por fiziko en 1921.
```

**Issues:**
- ⚠️ `Il` → `#Li` (recognized)
- ⚠️ `recevis` → `#ricevi` (received - infinitive form shown)
- ⚠️ `Nobel-premio` → `#Nobel-premio` (Nobel Prize - recognized but marked)
- ⚠️ `por` → `*por` (for - partially working)
- ✅ `fiziko` → `fiziko` (physics - WORKS!)
- ❌ `1921` → `#unknown`

**Grammar:** ✅ Structure good

---

### Sentence 5: Birthplace
```
IDO: Einstein naskis en Ulm, Germania.
ESP: #unknown #naskiĝi en *Ulm, #Germanio.
EXP: Einstein naskiĝis en Ulm, Germanio.
```

**Issues:**
- ❌ `Einstein` → `#unknown`
- ⚠️ `naskis` → `#naskiĝi` (was born - infinitive shown, needs past tense)
- ⚠️ `Ulm` → `*Ulm` (city name)
- ⚠️ `Germania` → `#Germanio` (Germany - recognized)

---

### Sentence 6: Migration
```
IDO: En 1933 il migris a Usa pro la nazii.
ESP: En #unknown #li #migri #al #Usono #default #la #unknown.
EXP: En 1933 li migris al Usono pro la nazioj.
```

**Issues:**
- ❌ `1933` → `#unknown`
- ⚠️ `il` → `#li` (recognized)
- ⚠️ `migris` → `#migri` (migrated - infinitive shown)
- ✅ `a` → `#al` (to - works)
- ⚠️ `Usa` → `#Usono` (USA - recognized)
- ❌ `pro` → `#default` (because of)
- ❌ `nazii` → `#unknown` (Nazis - plural)

---

### Sentence 7: Famous equation
```
IDO: La fama equaciono E=mc² derivis de lua laboro.
ESP: #La @fama ekvacio Kaj=#unknown² #derivi *de sia laboro.
EXP: La fama ekvacio E=mc² derivis de lia laboro.
```

**Issues:**
- ❌ `fama` → `@fama` (famous)
- ✅ `equaciono` → `ekvacio` (equation - WORKS!)
- ❌ `E=mc²` → `Kaj=#unknown²` (formula parsing issue)
- ⚠️ `derivis` → `#derivi` (derived - infinitive)
- ✅ `lua` → `sia` (his/her - possessive works!)
- ✅ `laboro` → `laboro` (work - WORKS!)

**Positive:** Several words working!

---

### Sentence 8: Patent office
```
IDO: Einstein laboris en la patento-oficejo en Bern.
ESP: #unknown #labori en #la patento-#unknown en #unknown.
EXP: Einstein laboris en la patento-oficejo en Berno.
```

**Issues:**
- ❌ `Einstein` → `#unknown`
- ⚠️ `laboris` → `#labori` (worked - infinitive)
- ✅ `patento` → `patento` (patent - WORKS!)
- ❌ `oficejo` → `#unknown` (office)
- ❌ `Bern` → `#unknown` (city name)

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Total words tested** | ~55 | 100% |
| ✅ **Correctly translated** | ~12 | 22% |
| ⚠️ **Recognized but marked** | ~18 | 33% |
| ❌ **Not recognized** | ~25 | 45% |

**Overall Quality:** 22% fully correct, 55% recognized

---

## Critical Pattern: Past Tense Verbs ⚠️⚠️⚠️

### **MAJOR ISSUE: Past tense not working**

All past tense verbs failing:
- `esis` (was) → `#default`
- `viveskis` (lived) → `#unknown`
- `publikigis` (published) → `*publikigis`
- `recevis` (received) → `#ricevi` (shows infinitive)
- `naskis` (was born) → `#naskiĝi` (shows infinitive)
- `migris` (migrated) → `#migri` (shows infinitive)
- `derivis` (derived) → `#derivi` (shows infinitive)
- `laboris` (worked) → `#labori` (shows infinitive)

**Pattern:** Past tense `-is` endings not generating properly. System recognizes root but outputs infinitive instead of past tense.

**Impact:** 🔴 **CRITICAL** - Makes it impossible to translate biographical/historical content

---

## Issues by Category

### 1. 🔴 CRITICAL: Past Tense Generation Failure
**Impact:** Makes historical/biographical content impossible

**Problem:** Ido past tense `-is` not mapping to Esperanto `-is`

**Examples:**
- `laboris` → Should output `laboris`, but outputs `#labori`
- `migris` → Should output `migris`, but outputs `#migri`

**Solution:** Fix verb generation in transfer rules or autogen

---

### 2. ⚠️ HIGH: Missing Common Vocabulary

**Scientists/academics:**
- `fizikisto` → `fizikisto` (physicist)
- `fama` → `fama` (famous)
- `teorio` → `teorio` (theory)
- `relativeso` → `relativeco` (relativity)

**Biographical:**
- `Germaniana` → `germana` (German adjective)
- `nazii` → `nazioj` (Nazis)
- `oficejo` → `oficejo` (office)

---

### 3. ⚠️ MEDIUM: Year/Number Handling

**Years not recognized:**
- `1879`, `1905`, `1921`, `1933`, `1955`

**Year ranges:**
- `1879-1955` → Splits incorrectly

**Solution:** Add number/year handling

---

### 4. ⚠️ LOW: Proper Names

**People:**
- `Albert Einstein`

**Places:**
- `Ulm`, `Bern`

**Note:** These are expected to be #unknown unless we add them

---

## What Works Well ✅

1. **Superlative:** `maxim` → `plej` ✓
2. **Ordinals:** `20ma` → `dudeka` ✓
3. **Century:** `yarcento` → `jarcento` ✓
4. **Possessive:** `lua` → `sia` ✓
5. **Basic nouns:** `laboro`, `patento`, `fiziko` ✓
6. **Equation:** `equaciono` → `ekvacio` ✓
7. **Prepositions:** `di` → `de`, `a` → `al` ✓
8. **Structure:** Sentence structure preserved ✓

---

## Priority Fixes

### 🔴 CRITICAL (Must fix):
1. **Past tense generation** - Biographical content impossible without this
2. **`esis` verb** - Most common past tense verb

### ⚠️ HIGH (Important):
3. Add `fama` (famous)
4. Add `fizikisto` (physicist)
5. Add `teorio` (theory)
6. Add `relativeso` → `relativeco`

### ⚠️ MEDIUM (Nice to have):
7. Year handling (1900s numbers)
8. Add `Germaniana` → `germana`
9. Add `oficejo` (office)
10. Add `nazii` → `nazioj`

---

## Root Cause Analysis

### Past Tense Issue

Looking at the output pattern:
```
laboris → #labori (infinitive shown, not past tense)
```

**Hypothesis:** 
1. Morphological analyzer recognizes `-is` as past tense ✓
2. Bilingual lookup finds the root ✓
3. **Generator fails to add `-is` ending** ❌

**Likely location of bug:**
- Transfer rules (`.t1x`) might not be passing tense information
- Or generator (`.autogen.bin`) not producing past tense forms

**Evidence:**
- Present tense verbs work
- Infinitives work
- Only past tense fails

---

## Comparison with Kazakhstan Article

| Feature | Kazakhstan | Einstein | Change |
|---------|-----------|----------|--------|
| **Past tense** | ✅ Works (`esas`) | ❌ Broken | Regression? |
| **Proper nouns** | ❌ Missing | ❌ Missing | Same |
| **Basic grammar** | ✅ Good | ✅ Good | Same |
| **Coverage** | 50% | 22% | Worse |

**Note:** Kazakhstan article used present tense (`esas` = is), which worked. Einstein article uses past tense (`esis` = was), which doesn't work.

---

## Test Commands

```bash
cd /home/mark/apertium-dev/apertium-ido-epo

# Test single verb
echo "Einstein laboris." | apertium -d . ido-epo

# Full test
apertium -d . ido-epo < test_einstein.txt
```

---

## Recommendations

### Immediate:
1. **Investigate past tense generation** - This is blocking biographical content
2. Check if `esis` (was) is mapped correctly in bilingual dictionary
3. Test other past tense verbs to confirm pattern

### Short-term:
4. Add scientific vocabulary (fama, fizikisto, teorio, relativeso)
5. Add year handling

### Long-term:
6. Systematic proper noun handling
7. Compound word support (patento-oficejo)

---

## Conclusion

**Current State:**
- Grammar structure: ✅ Excellent
- Present tense: ✅ Works
- Past tense: ❌ **BROKEN** (critical bug)
- Vocabulary: ⚠️ Fair (22% coverage)
- Overall: **Blocked by past tense issue**

**The translator cannot handle biographical or historical content** until the past tense generation bug is fixed. This is a higher priority than adding vocabulary.

**Priority:** Fix past tense generation immediately.

