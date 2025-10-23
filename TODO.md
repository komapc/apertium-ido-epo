# TODO - Apertium Ido-Esperanto Translation Pair

**Last Updated:** October 23, 2025

## 🎯 Current Priorities

### 🔴 0. FIX CRITICAL MORPHOLOGY BUGS **[NEW - Oct 23, 2025]**
**Status:** CRITICAL - Blocking 80% of translations  
**Priority:** URGENT  
**Time:** 3-6 hours total

#### 🔴 **Priority 1: Complete Verb Paradigm (CRITICAL)**
**File:** `apertium-ido.ido.dix` - lines 29-91 (`<pardefs>` section)  
**Time:** 2-3 hours  
**Impact:** HIGH - Fixes most "red words" (unknown conjugated verbs)

**Problem:**
- Current `ar__vblex` paradigm only recognizes infinitives (`esar` ✅)
- Missing ALL conjugations: present (`esas` ❌), past (`esis` ❌), future (`esos` ❌)
- Result: Sentences like "Me esas bona" fail because `esas` is unknown

**Solution:**
```xml
<pardef n="ar__vblex">
  <!-- Current (only this exists): -->
  <e><p><l>ar</l><r><s n="vblex"/><s n="inf"/></r></p></e>
  
  <!-- ADD THESE: -->
  <e><p><l>as</l><r><s n="vblex"/><s n="pri"/></r></p></e>   <!-- present -->
  <e><p><l>is</l><r><s n="vblex"/><s n="pii"/></r></p></e>   <!-- past -->
  <e><p><l>os</l><r><s n="vblex"/><s n="fti"/></r></p></e>   <!-- future -->
  <e><p><l>us</l><r><s n="vblex"/><s n="cni"/></r></p></e>   <!-- conditional -->
  <e><p><l>ez</l><r><s n="vblex"/><s n="imp"/></r></p></e>   <!-- imperative -->
</pardef>
```

**Test after fix:**
```bash
echo "Me esas bona" | apertium ido-epo
# Should produce: Mi estas bona (not *esas)
```

---

#### 🔴 **Priority 2: Complete Noun Paradigm (HIGH)**
**File:** `apertium-ido.ido.dix` - same `<pardefs>` section  
**Time:** 1-2 hours  
**Impact:** MEDIUM-HIGH - Fixes plural and accusative nouns

**Problem:**
- Current `o__n` paradigm only recognizes singular nominative (`kato` ✅)
- Missing: plural (`kati` ❌), accusative (`katon` ❌, `katin` ❌)

**Solution:**
```xml
<pardef n="o__n">
  <!-- Current: -->
  <e><p><l>o</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
  
  <!-- ADD THESE: -->
  <e><p><l>on</l><r><s n="n"/><s n="sg"/><s n="acc"/></r></p></e>  <!-- singular accusative -->
  <e><p><l>i</l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>   <!-- plural nominative -->
  <e><p><l>in</l><r><s n="n"/><s n="pl"/><s n="acc"/></r></p></e>  <!-- plural accusative -->
</pardef>
```

**Test:**
```bash
echo "Me vidas katon" | apertium ido-epo
# Should recognize "katon" (cat - accusative)
```

---

#### ⚠️ **Priority 3: Complete Adjective Paradigm (MEDIUM)**
**File:** `apertium-ido.ido.dix`  
**Time:** 30 minutes - 1 hour  
**Impact:** MEDIUM - Fixes adjective agreement

**Problem:**
- Current `a__adj` only recognizes base form (`granda` ✅)
- Missing: plural (`grandi` ❌), accusative (`grandan` ❌, `grandi-n` ❌)

**Solution:**
```xml
<pardef n="a__adj">
  <e><p><l>a</l><r><s n="adj"/></r></p></e>           <!-- base -->
  <e><p><l>an</l><r><s n="adj"/><s n="acc"/></r></p></e>  <!-- accusative -->
  <e><p><l>i</l><r><s n="adj"/><s n="pl"/></r></p></e>    <!-- plural -->
  <e><p><l>in</l><r><s n="adj"/><s n="pl"/><s n="acc"/></r></p></e>  <!-- plural acc -->
</pardef>
```

---

#### 📋 **Priority 4: Document & Test (1 hour)**
- [ ] Test all paradigm changes bidirectionally (Ido→Esperanto, Esperanto→Ido)
- [ ] Run comprehensive test suite with conjugated verbs
- [ ] Document changes in CHANGELOG.md
- [ ] Create test cases for each paradigm
- [ ] Update MORPHOLOGY_EXPLANATION.md with "FIXED" status

**Success Criteria:**
- ✅ Conjugated verbs recognized: `esas`, `esis`, `esos`, `esus`
- ✅ Plural nouns recognized: `kati`, `katoj`
- ✅ Accusative forms recognized: `katon`, `grandan`
- ✅ Test sentence translates correctly: "Me esas bona" → "Mi estas bona"

**References:**
- See: `MORPHOLOGY_EXPLANATION.md` for detailed problem analysis
- Ido grammar: Verbs are regular (-ar, -as, -is, -os, -us, -ez)
- Compare with: Esperanto `apertium-epo` paradigms (similar structure)

---

### ✅ 1. Verify Merged PRs in Production **[Oct 23, 2025]**
**Status:** PRs merged, needs verification  
**Priority:** HIGH  
**Time:** 15-30 minutes

- [ ] **Test apertium-ido pkg-config Fix**
  - Verify `pkg-config --variable=srcdir apertium-ido` works
  - Test that dependent projects can find apertium-ido
  - Confirm no build errors in apertium-ido-epo
  
- [ ] **Test apertium-ido-epo Standalone Build**
  - Verify builds without vendor submodules
  - Test `make` and `make install`
  - Confirm runtime translation works correctly
  
- [ ] **Integration Test on Translator**
  - Deploy updated dictionaries to APy server
  - Run translation tests (both directions)
  - Verify no regressions from restructure

**Related PRs:**
- apertium-ido #10: "fix: Add srcdir variable to pkg-config file" (merged)
- apertium-ido-epo #48: "refactor: Remove vendor submodules" (merged)

---

### 1. Additional Morphology Improvements (After Priority 0)
**Status:** Planning  
**Priority:** Medium (After verb/noun/adjective paradigms fixed)

#### Additional Paradigms Needed:
- [ ] **Adverbial Forms** (`-e` endings)
  - Already complete (adverbs don't inflect)
  - But check: comparative/superlative (`plu bone`, `maxim bone`)

- [ ] **Participles** (if Ido has them)
  - Present participle: `-anta` (IO) → `-anta` (EO)
  - Past participle: `-inta` (IO) → `-inta` (EO)
  - Check Ido grammar for participle system

- [ ] **Correlatives** (question words, demonstratives)
  - kel, kua, kande, ube, etc.
  - Most should already be in dictionary as function words
  - Verify completeness

---

### 2. Improve Grammatical Rules
**Status:** Planning
**Priority:** High (After morphology fixed)

#### Specific Areas to Improve:
- [ ] **Verb Conjugation Rules**
  - Review Ido → Esperanto tense mappings
  - Fix edge cases in conditional/subjunctive
  - Improve imperative form handling
  
- [ ] **Pronoun Handling**
  - Review personal pronoun translations
  - Fix possessive pronoun agreement
  - Improve reflexive pronoun rules

- [ ] **Word Order & Structure**
  - Analyze and improve SVO vs SOV patterns
  - Fix subordinate clause word order
  - Improve question formation rules

- [ ] **Adjective-Noun Agreement**
  - Review plural agreement rules
  - Fix adjective position rules
  - Improve compound adjective handling

- [ ] **Preposition Mapping**
  - Review common preposition translations
  - Document exceptions and edge cases
  - Add context-sensitive rules

#### Questions to Answer:
- Which grammatical constructs currently have the **most errors**?
- Are there specific **test sentences** that fail consistently?
- What **linguistic patterns** need better coverage?

---

### 3. Add More Tests
**Status:** Planning
**Priority:** High (Run after morphology fixes)

#### Test Coverage Needed:
- [ ] **Basic Grammar Tests**
  - Verb tenses (present, past, future, conditional)
  - Noun plurals and case
  - Adjective agreement
  - Pronouns (personal, possessive, reflexive)

- [ ] **Complex Structures**
  - Subordinate clauses
  - Relative clauses (qui, kel, qua)
  - Compound sentences
  - Passive voice

- [ ] **Common Vocabulary**
  - Top 1000 most frequent words
  - Function words (prepositions, conjunctions)
  - Numbers and dates
  - Question words

- [ ] **Edge Cases**
  - Homonyms and ambiguous words
  - Proper nouns vs common nouns
  - Idiomatic expressions
  - Compound words

- [ ] **Bidirectional Testing**
  - All tests should work Ido → Esperanto
  - All tests should work Esperanto → Ido
  - Document intentional asymmetries

#### Test Format:
```
Input (Ido):     Me manjas pomo
Expected (Eo):   Mi manĝas pomon
Actual (Eo):     [test result]
Status:          ✅ Pass / ❌ Fail
```

---

## 📋 Next Actions

### Immediate (This Week)
1. **Analyze Current Translation Quality**
   - Run existing tests and document failure patterns
   - Identify top 10 most common error types
   - Prioritize rules to fix

2. **Create Comprehensive Test Suite**
   - Start with `test/grammar_basic.txt` (100 sentences)
   - Add `test/grammar_advanced.txt` (50 sentences)
   - Add `test/vocabulary_common.txt` (500 words)

3. **Document Current Rules**
   - Review `.t1x` transfer rules
   - Document what each rule does
   - Identify gaps and missing rules

### Short Term (This Month)
- [ ] Fix top 5 grammatical error patterns
- [ ] Add 200+ test sentences
- [ ] Improve verb handling rules
- [ ] Document all rule changes in CHANGELOG.md

### Long Term (Next 3 Months)
- [ ] Achieve 90%+ accuracy on common vocabulary
- [ ] Comprehensive test coverage (1000+ sentences)
- [ ] Ready for upstream Apertium integration
- [ ] Documentation for contributors

---

## 🔍 Analysis Needed

**Please clarify:**
1. What are the **most common translation errors** you're seeing?
2. Do you have **example sentences** that translate incorrectly?
3. Are there specific **linguistic constructs** causing problems?
4. What **test files** already exist that we should expand?

---

## 📊 Success Metrics

- **Translation Accuracy:** Target 90%+ on test suite
- **Test Coverage:** 1000+ sentences covering all grammar
- **Documentation:** All rules documented with examples
- **Bidirectional:** Both directions tested and working

---

## 📚 Resources

- Grammar references: `docs/guides/` (if exists)
- Current tests: `test/`
- Transfer rules: `apertium-ido-epo.ido-epo.t1x`, `apertium-ido-epo.epo-ido.t1x`
- Dictionaries: `apertium-ido-epo.ido-epo.dix`


