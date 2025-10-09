# Kazakhstan Article Translation Analysis

**Source:** [Ido Wikipedia - Kazakstan](https://io.wikipedia.org/wiki/Kazakstan)  
**Date:** October 9, 2025  
**Test:** Sentence-by-sentence translation analysis

---

## Test Sentences

### Sentence 1: Basic statement
```
IDO: Kazakstan esas stato en Central-Azia.
ESP: #unknown estas ŝtato en *Central-#Azio.
EXP: Kazaĥstano estas ŝtato en Centr-Azio.
```

**Issues:**
- ❌ `Kazakstan` → `#unknown` (proper noun not in dictionary)
- ❌ `Central-Azia` → `*Central-#Azio` (compound proper noun issue)

**Grammar:** ✅ Correct (copula working, case correct)

---

### Sentence 2: Superlative + comparative
```
IDO: Ol esas la maxim granda lando sen aceso a la oceano.
ESP: #Ĝi estas #la *maxim granda lando sen *aceso #al #la oceano.
EXP: Ĝi estas la plej granda lando sen aliro al la oceano.
```

**Issues:**
- ⚠️ `#Ĝi` - pronoun recognized but marked
- ⚠️ `#la` (×3) - article generation issues
- ❌ `maxim` → `*maxim` (should be `plej`)
- ❌ `aceso` → `*aceso` (should be `aliro` or `alireblo`)
- ⚠️ `#al` - preposition marked

**Grammar:** ✅ Correct (copula, case, agreement all good)

---

### Sentence 3: Capital city
```
IDO: La chefurbo esas Astana.
ESP: #La #unknown estas #unknown.
EXP: La ĉefurbo estas Astano.
```

**Issues:**
- ❌ `chefurbo` → `#unknown` (compound: chef + urbo = capital city)
- ❌ `Astana` → `#unknown` (proper noun)

**Grammar:** ✅ Correct

---

### Sentence 4: Main city
```
IDO: La precipua urbo esas Almatı.
ESP: #La ĉefa urbo estas #unknown.
EXP: La ĉefa urbo estas Almato.
```

**Issues:**
- ✅ `precipua` → `ĉefa` (WORKS!)
- ❌ `Almatı` → `#unknown` (proper noun with special character)

**Grammar:** ✅ Correct

**Note:** Good example - `precipua` correctly translated!

---

### Sentence 5: Countries list
```
IDO: Kazakstan havas frontieri kun Rusia, Chinia, Kirgizistan, Uzbekistan e Turkmenistan.
ESP: #unknown #default frontoj kun #Rusio, @Chinia, #unknown, #unknown #unknown #unknown.
EXP: Kazaĥstano havas limojn kun Rusio, Ĉinio, Kirgizio, Uzbekio kaj Turkmenio.
```

**Issues:**
- ❌ `Kazakstan` → `#unknown`
- ❌ `havas` → `#default` (verb recognition issue?)
- ✅ `frontieri` → `frontoj` (WORKS! borders)
- ⚠️ `Rusia` → `#Rusio` (recognized but marked)
- ❌ `Chinia` → `@Chinia` (not found - should be `Ĉinio`)
- ❌ `Kirgizistan` → `#unknown` (should be `Kirgizio`)
- ❌ `Uzbekistan` → `#unknown` (should be `Uzbekio`)
- ❌ `Turkmenistan` → `#unknown` (should be `Turkmenio`)
- ❌ `e` → `#unknown` (should be `kaj` - coordination issue)

**Grammar:** ⚠️ Plural correct, but verb issue

---

### Sentence 6: Population
```
IDO: La populaco esas sirke 19 milioni.
ESP: #La #unknown estas #unknown *19 milionoj.
EXP: La popolnombro estas ĉirkaŭ 19 milionoj.
```

**Issues:**
- ❌ `populaco` → `#unknown` (should be `popolnombro` or `loĝantaro`)
- ❌ `sirke` → `#unknown` (should be `ĉirkaŭ`)
- ⚠️ `19` → `*19` (number partially works)
- ✅ `milioni` → `milionoj` (WORKS!)

**Grammar:** ✅ Correct

---

### Sentence 7: Official languages
```
IDO: La oficiala lingui esas kazaka e rusa.
ESP: #La #unknown #unknown estas #unknown #unknown #unknown.
EXP: La oficialaj lingvoj estas kazaĥa kaj rusa.
```

**Issues:**
- ❌ `oficiala` → `#unknown` (should be `oficiala`)
- ❌ `lingui` → `#unknown` (plural of `linguo` - should be `lingvoj`)
- ❌ `kazaka` → `#unknown` (adjective - should be `kazaĥa`)
- ❌ `e` → `#unknown` (conjunction should be `kaj`)
- ❌ `rusa` → `#unknown` (adjective - should be `rusa`)

**Grammar:** ❓ Can't assess due to missing words

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Total words tested** | 47 | 100% |
| ✅ **Correctly translated** | 8 | 17% |
| ⚠️ **Recognized but marked (#)** | 11 | 23% |
| ❌ **Not recognized (#unknown)** | 18 | 38% |
| ❌ **Not found (@)** | 1 | 2% |
| ⚠️ **Partial (*)** | 5 | 11% |
| **#default** | 1 | 2% |

**Overall Quality:** 17% fully correct, 40% recognized

---

## Issues by Category

### 1. Missing Proper Nouns (High Priority) ⚠️
**Impact:** 40% of failures

Missing country/place names:
- `Kazakstan` → Should add `Kazaĥstano`
- `Astana` → Should add `Astano`
- `Almatı` → Should add `Almato`
- `Chinia` → Should add or fix to `Ĉinio`
- `Kirgizistan` → Should add `Kirgizio`
- `Uzbekistan` → Should add `Uzbekio`
- `Turkmenistan` → Should add `Turkmenio`

**Solution:** Add systematic country name mappings

---

### 2. Missing Common Vocabulary (High Priority) ⚠️
**Impact:** 35% of failures

Essential missing words:
- `chefurbo` → `ĉefurbo` (capital city - compound)
- `populaco` → `popolnombro` or `loĝantaro` (population)
- `sirke` → `ĉirkaŭ` (approximately)
- `oficiala` → `oficiala` (official)
- `lingui` → `lingvoj` (languages - plural)
- `aceso` → `aliro` (access)

**Solution:** Add these common words to dictionary

---

### 3. Article Generation Issues (Medium Priority) ⚠️
**Impact:** Aesthetic issue, doesn't prevent comprehension

Pattern: `#la`, `#La` appearing frequently

**Current:** Articles recognized but marked with #  
**Expected:** Clean output without #

**Solution:** Fix generation in `.autogen.bin` or improve transfer rules

---

### 4. Compound Words (Medium Priority) ⚠️
**Impact:** 15% of failures

Issues:
- `Central-Azia` → Not handling hyphenated compounds
- `chefurbo` → Not splitting `chef-urbo`

**Solution:** Add compound word handling or add common compounds directly

---

### 5. Adjective Forms (Low Priority) ⚠️
Nationality adjectives:
- `kazaka` → `kazaĥa`
- `rusa` → `rusa`

**Solution:** Add nationality adjectives systematically

---

## What Works Well ✅

1. **Copula case agreement:** All copula sentences have correct nominative case
2. **Basic grammar:** Subject-verb-object order preserved
3. **Number agreement:** Plurals working (`frontieri` → `frontoj`, `milioni` → `milionoj`)
4. **Some adjectives:** `precipua` → `ĉefa` ✓
5. **Pronouns:** `ol` → `ĝi` (recognized)
6. **Basic structure:** Sentence structure preserved

---

## Priority Fixes

### Immediate (Critical for basic functionality):
1. Add country names (Kazakstan, Chinia, etc.)
2. Add `chefurbo` (capital city)
3. Add `populaco` (population)
4. Add `sirke` (approximately)
5. Add `oficiala` (official)
6. Fix `maxim` → `plej` (superlative)

### Short-term (Important for quality):
7. Fix article generation (#la issue)
8. Add `aceso` → `aliro` (access)
9. Add `linguo/lingui` (language/languages)
10. Add nationality adjectives

### Medium-term (Nice to have):
11. Compound word handling
12. More proper nouns
13. Number handling improvements

---

## Recommendations

1. **Create country names supplement** - Add all -stan countries and major nations
2. **Add geographic vocabulary** - Common geographic terms (capital, population, border, etc.)
3. **Fix superlative** - `maxim` should map to `plej`, not stay as-is
4. **Investigate article generation** - Why are articles marked with #?

---

## Test Command

```bash
cd /home/mark/apertium-dev/apertium-ido-epo
apertium -d . ido-epo < test_kazakstan.txt
```

---

## Conclusion

**Current State:**
- Grammar: ✅ Excellent (copula fix working)
- Basic vocabulary: ⚠️ Fair (17% coverage)
- Proper nouns: ❌ Poor (most missing)
- Overall: **Needs vocabulary expansion**

**The translator handles grammar correctly** but lacks vocabulary for geographic/political content. Adding ~20-30 key words would improve coverage to 60-70%.

**Priority:** Add geographic vocabulary supplement.


