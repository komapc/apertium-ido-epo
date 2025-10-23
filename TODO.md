# TODO - Apertium Ido-Esperanto Translation Pair

**Last Updated:** October 23, 2025

## 🎯 Current Priorities

### ✅ 0. Verify Merged PRs in Production **[NEW - Oct 23, 2025]**
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

### 1. Improve Grammatical Rules
**Status:** Planning
**Priority:** High

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

### 2. Add More Tests
**Status:** Planning
**Priority:** High

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


