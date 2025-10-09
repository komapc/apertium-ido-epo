# Step 2: Priority Analysis - Esperanto to Ido Translation Issues

## Executive Summary

Based on analysis of the Kristanismo Wikipedia article, we've identified **7 major issue categories** affecting translation quality. Issues are prioritized by **frequency**, **impact**, and **implementation complexity**.

---

## HIGH PRIORITY ISSUES (Systematic & Frequent)

### Priority 1: Partitive Construction "da" → "di"
- **Frequency:** Common in all quantitative expressions
- **Impact:** CRITICAL - Affects readability and accuracy
- **Current Status:** ❌ Not handled (shows as `@da`)
- **Solution Complexity:** LOW (dictionary + transfer rule)
- **Examples Found:** 2 instances in sample text
  - "miliardoj da kristanoj" → should be "miliardi di kristani"
  - "Miloj da homoj" → should be "mili di homi"

**Implementation:**
- ✅ Add `<e><p><l>di<s n="pr"/></l><r>da<s n="pr"/></r></p></e>` to bilingual dictionary
- ✅ Add transfer rule to handle `QUANTIFIER da NOUN` pattern

**Test Command:**
```bash
echo "miloj da homoj" | apertium -d . epo-ido
# Expected: mili di homi
```

---

### Priority 2: Superlative "plej" → "maxim"
- **Frequency:** Very common in descriptive text
- **Impact:** CRITICAL - Core grammatical structure
- **Current Status:** ❌ Not handled (passes through unchanged)
- **Solution Complexity:** LOW-MEDIUM (dictionary + transfer rule)
- **Examples Found:** 2 instances in sample text
  - "la plej granda religio" → should be "la maxim granda religio"
  - "plej gravaj festoj" → should be "maxim grava festi"

**Implementation:**
- ✅ Add `<e><p><l>maxim<s n="adv"/></l><r>plej<s n="adv"/></r></p></e>` to bilingual dictionary
- ✅ Add transfer rule for `plej + ADJECTIVE` pattern
- ✅ Add transfer rule for `ARTICLE + plej + ADJECTIVE` pattern

**Test Command:**
```bash
echo "la plej granda religio" | apertium -d . epo-ido
# Expected: la maxim granda religio
```

---

### Priority 3: Impersonal Pronoun "oni" → "on"
- **Frequency:** Very common in formal/academic writing
- **Impact:** HIGH - Affects sentence structure and meaning
- **Current Status:** ❌ Not in dictionary (shows as `@Oni`)
- **Solution Complexity:** LOW (dictionary entries)
- **Examples Found:** 2 instances in sample text
  - "Oni kalkulas" → should be "On kontas"
  - "Oni kredas" → should be "On kredas"

**Implementation:**
- ✅ Add pronoun entries with all forms (nominative, accusative)
- ⚠️ May need transfer rule for special cases

**Test Command:**
```bash
echo "Oni kalkulas" | apertium -d . epo-ido
# Expected: On kontas
```

---

### Priority 4: Neuter Pronoun "ĝi" → "ol"
- **Frequency:** Very common for inanimate subjects
- **Impact:** HIGH - Core pronoun system
- **Current Status:** ⚠️ Partial (shows as `@Prpers`, entry exists but not mapping correctly)
- **Solution Complexity:** LOW (verify/fix bilingual mapping)
- **Examples Found:** 3 instances in sample text (including one in compound verb)
  - "Ĝi estas" → should be "Ol esas"

**Implementation:**
- ✅ Entry exists in dictionary, verify bilingual mapping
- ⚠️ Check why showing as @Prpers instead of translating

**Test Command:**
```bash
echo "Ĝi estas granda" | apertium -d . epo-ido
# Expected: Ol esas granda
```

---

### Priority 5: Ordinal Number Suffix "-a" → "-ma"
- **Frequency:** Common in historical and sequential contexts
- **Impact:** MEDIUM-HIGH - Affects dates, sequences
- **Current Status:** ✅ IMPLEMENTED (via dictionary for 1-31, 100, 1000)
- **Solution Complexity:** LOW (already done)
- **Examples Found:** 1 instance in sample text
  - "la 1-a jarcento" → should be "la 1ma yar-cento"

**Implementation:**
- ✅ Already implemented in dictionary for common ordinals
- ✅ No additional work needed

**Test Command:**
```bash
echo "la 1-a jarcento" | apertium -d . epo-ido
# Expected: la 1ma yar-cento
```

---

## MEDIUM PRIORITY ISSUES (Vocabulary & Lexical)

### Priority 6: Religious/Specialized Vocabulary
- **Frequency:** Domain-specific
- **Impact:** MEDIUM - Affects specific topics
- **Current Status:** ❌ Many entries missing
- **Solution Complexity:** LOW-MEDIUM (dictionary additions)

**Missing Terms Identified:**
- kristanismo → kristanismo
- kristano → kristano
- religio → religio (may exist)
- Jesuo → Iesu
- Kristo → Kristo
- eklezio → eklezio
- Biblio → Biblio

**Implementation:**
- ✅ Add specialized vocabulary entries to bilingual dictionary
- ⚠️ Verify which already exist

---

### Priority 7: Common Verbs & Adjectives
- **Frequency:** High for general text
- **Impact:** MEDIUM - Affects general translation
- **Current Status:** ❌ Many missing
- **Solution Complexity:** LOW (dictionary additions)

**Missing Terms Identified:**
- bazita → bazita (based)
- instruoj → instruadi (teachings)
- tutmonda → tut-mondala (worldwide)
- ekzisti → existar (to exist)
- kalkuli → kontar (to calculate)
- origini → orinjinar (to originate)

**Implementation:**
- ✅ Add common vocabulary to bilingual dictionary

---

### Priority 8: Geographic Names
- **Frequency:** LOW-MEDIUM
- **Impact:** MEDIUM - Affects proper nouns
- **Current Status:** ❌ Many missing
- **Solution Complexity:** LOW (dictionary additions)

**Examples:**
- Judujo → Judea
- Various country/region names

**Implementation:**
- ✅ Add geographic names to bilingual dictionary as discovered

---

## LOW PRIORITY ISSUES (Edge Cases)

### Priority 9: Compound Word Hyphenation
- **Frequency:** MEDIUM
- **Impact:** LOW - Cosmetic difference
- **Current Status:** ⚠️ Inconsistent
- **Solution Complexity:** MEDIUM (requires pattern analysis)

**Examples:**
- "jarcento" vs "yar-cento"
- "tutmonda" vs "tut-mondala"

**Implementation:**
- ⚠️ Handle via dictionary entries
- ⚠️ May need post-processing for systematic approach

---

### Priority 10: Circumflex Letter Conversion
- **Frequency:** HIGH (10 instances in sample)
- **Impact:** LOW - Automatically handled by dictionary
- **Current Status:** ✅ HANDLED (dictionary lookup handles this)
- **Solution Complexity:** NONE (already working)

**Letters:**
- ĉ → c/ch (context-dependent)
- ĝ → j
- ĥ → h
- ĵ → j
- ŝ → sh
- ŭ → u/w

**Implementation:**
- ✅ No action needed - dictionary handles automatically

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Week 1)
1. ✅ Add "da" → "di" dictionary entry
2. ✅ Add "plej" → "maxim" dictionary entry
3. ✅ Add "oni" → "on" pronoun entries
4. ✅ Fix "ĝi" → "ol" mapping issue
5. ✅ Add transfer rule for partitive construction
6. ✅ Add transfer rule for superlative construction

### Phase 2: Vocabulary Expansion (Week 2)
7. ✅ Add religious vocabulary (10-15 terms)
8. ✅ Add common verbs/adjectives (20-30 terms)
9. ✅ Add geographic names (5-10 terms)

### Phase 3: Testing & Refinement (Week 3)
10. ⚠️ Create comprehensive test suite
11. ⚠️ Test with full Kristanismo article
12. ⚠️ Identify and fix edge cases
13. ⚠️ Document coverage metrics

### Phase 4: Advanced Patterns (Week 4)
14. ⚠️ Compound superlative phrases (4+ word patterns)
15. ⚠️ Complex partitive constructions
16. ⚠️ Systematic compound word handling

---

## Success Metrics

### Baseline (Current State)
- **Unknown words (@):** ~60% in test sentences
- **Incorrect output (#):** ~20%
- **Accurate translation:** ~20%

### Target After Phase 1
- **Unknown words (@):** <30%
- **Incorrect output (#):** <10%
- **Accurate translation:** >60%

### Target After Phase 2
- **Unknown words (@):** <15%
- **Incorrect output (#):** <5%
- **Accurate translation:** >80%

### Final Target (All Phases)
- **Unknown words (@):** <10%
- **Incorrect output (#):** <5%
- **Accurate translation:** >85%

---

## Resource Requirements

### Development Time Estimate
- Phase 1: 8-12 hours
- Phase 2: 6-10 hours
- Phase 3: 4-6 hours
- Phase 4: 8-12 hours
- **Total:** 26-40 hours

### Testing Corpus Size
- Initial: Kristanismo article (~3,000 words)
- Expansion: 5 additional Wikipedia articles (~15,000 words)
- Validation: 10 articles (~30,000 words)

---

## Risk Assessment

### High Risk
1. **Transfer rule conflicts** - New rules may conflict with existing rules
   - Mitigation: Careful rule ordering and testing

2. **Dictionary bloat** - Adding too many entries may slow compilation
   - Mitigation: Focus on high-frequency terms first

### Medium Risk
3. **Edge cases** - Unusual constructions may break rules
   - Mitigation: Comprehensive testing and fallback rules

4. **Morphological complexity** - Ido/Esperanto agglutination may cause issues
   - Mitigation: Leverage existing morphological analyzers

### Low Risk
5. **Performance** - Minimal impact expected from new rules
6. **Backwards compatibility** - All changes are additive

---

_Analysis completed: 2025-10-09_
_Based on: Kristanismo Wikipedia article (https://eo.wikipedia.org/wiki/Kristanismo)_
_Methodology: Sentence-by-sentence translation analysis + automated pattern extraction_

