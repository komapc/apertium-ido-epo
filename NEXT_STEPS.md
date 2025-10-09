# Next Steps for Ido-Esperanto Translation System

**Date:** 2025-10-09  
**Current Status:** CG-enabled system with critical fixes implemented  
**Current Accuracy:** ~70% (up from ~37% baseline)

---

## 🎯 IMMEDIATE PRIORITIES (High Impact)

### 1. **Vocabulary Expansion** ⭐⭐⭐⭐⭐
**Impact:** Highest - most `@` errors are missing vocabulary  
**Effort:** Low - straightforward dictionary additions

**Missing High-Frequency Words:**
- **Proper nouns:** Kristanismo, Tibet, Jesuo, Kristo, Everest
- **Common verbs:** ekzisti → existar, instrui → instruar, orinjinar
- **Adjectives:** tutmonda/tutmondala, baza, religioza
- **Nouns:** instruo → instruado, cirke → cirke

**Action Items:**
```bash
# Create systematic vocabulary list from test articles
grep -o '@[^@]*' tests/ | sort | uniq -c | sort -rn > missing_vocabulary.txt

# Add top 100 most frequent missing words
# Estimated time: 2-3 hours
# Expected accuracy gain: +10-15%
```

---

### 2. **Fix Adjective Generation Issues** ⭐⭐⭐⭐
**Impact:** High - many `#` errors are adjective paradigm issues  
**Effort:** Low-Medium

**Current Issues:**
- `#alta`, `#bela`, `#granda` - Ido adjectives showing `#`
- Likely missing paradigm entries or wrong tag combinations

**Action Items:**
- Investigate Ido adjective paradigm (`a__adj`)
- Check if adjectives need singular tag (Ido adjectives are invariable)
- Add missing common adjectives with correct paradigm

**Estimated time:** 1-2 hours  
**Expected accuracy gain:** +5-10%

---

### 3. **Prpers Pronoun Handling** ⭐⭐⭐⭐
**Impact:** High - `Ĝi` showing as `@Prpers`  
**Effort:** Low

**Issue:** 
- Esperanto uses special lemma `Prpers` for personal pronouns
- Need mapping: `Prpers<prn><subj><p3><nt><sg>` → `ol<prn>` (Ido)

**Action Items:**
```xml
<!-- Add to bilingual dictionary -->
<e><p><l>ol<s n="prn" /></l><r>prpers<s n="prn" /><s n="subj" /><s n="p3" /><s n="nt" /><s n="sg" /></r></p></e>
<e><p><l>il<s n="prn" /></l><r>prpers<s n="prn" /><s n="subj" /><s n="p3" /><s n="m" /><s n="sg" /></r></p></e>
<e><p><l>elu<s n="prn" /></l><r>prpers<s n="prn" /><s n="subj" /><s n="p3" /><s n="f" /><s n="sg" /></r></p></e>
```

**Estimated time:** 30 minutes  
**Expected accuracy gain:** +3-5%

---

## 🔧 MEDIUM PRIORITIES (Important but Complex)

### 4. **Multiword Unit Handling** ⭐⭐⭐
**Impact:** Medium - affects contractions and some partitives  
**Effort:** High

**Issues:**
- `Miloj da` analyzed as single unit → can't translate
- Contractions `dil`, `del` need expansion to `di la`, `de la`

**Approaches:**
1. **Preprocess step:** Expand contractions before morphology
2. **MWU entries:** Add multiword entries to dictionaries
3. **Postprocess:** Handle after generation

**Estimated time:** 4-6 hours  
**Expected accuracy gain:** +5%

---

### 5. **Transfer Rule Enhancement** ⭐⭐⭐
**Impact:** Medium - improves grammatical accuracy  
**Effort:** Medium

**Needed Rules:**
- **Accusative removal:** Strip `-n` when translating EPO→IDO (Ido doesn't have accusative)
- **Plural adjective agreement:** Handle EPO plural adjectives → IDO invariable adjectives
- **Ordinal numbers:** Test and verify `7ma` → `sepa` pattern works universally

**Example Transfer Rule (Accusative Removal):**
```xml
<!-- Strip accusative case from nouns when translating to Ido -->
<rule>
  <pattern>
    <pattern-item n="nom"/>
  </pattern>
  <action>
    <out>
      <lu>
        <clip pos="1" side="tl" part="lem"/>
        <clip pos="1" side="tl" part="a_nom"/>
        <clip pos="1" side="tl" part="nbr"/>
        <!-- Skip cas (case) - Ido doesn't have it -->
      </lu>
    </out>
  </action>
</rule>
```

**Estimated time:** 3-4 hours  
**Expected accuracy gain:** +3-5%

---

### 6. **Relative Pronoun Tag Support** ⭐⭐
**Impact:** Low-Medium  
**Effort:** Medium

**Issue:** Ido generator can't handle `<rel><nn>` tags

**Options:**
1. Add `rel` and `nn` to Ido symbol definitions
2. Create `__rel_prn` paradigm
3. Strip tags in transfer (simpler)

**Estimated time:** 2 hours  
**Expected accuracy gain:** +2%

---

## 📈 LONG-TERM IMPROVEMENTS (Polish & Scale)

### 7. **Expand CG Rules** ⭐⭐⭐
**Impact:** Medium - improves analysis accuracy  
**Effort:** Ongoing

**Current CG Rules:** 7 rules  
**Target:** 20-30 rules

**Patterns to Add:**
- More preposition disambiguation
- Verb vs noun disambiguation
- Adjective vs adverb patterns
- Number context rules

---

### 8. **Bidirectional Improvements** ⭐⭐
**Impact:** Medium  
**Effort:** Medium

**Focus Areas:**
- IDO→EPO direction needs more work (currently ~65% vs 70% for EPO→IDO)
- Esperanto monolingual dictionary completeness
- Esperanto generator paradigm issues (`#` errors in IDO→EPO)

---

### 9. **Test Suite Development** ⭐⭐⭐⭐
**Impact:** High for maintenance  
**Effort:** Low-Medium

**Create:**
- Regression test suite (prevent breaking working translations)
- Coverage tests (ensure all grammatical patterns tested)
- Performance benchmarks

**Structure:**
```
tests/
  regression/
    kristanismo_sentences.txt
    tibet_sentences.txt
  grammar/
    superlatives.txt
    ordinals.txt
    partitive.txt
  vocabulary/
    high_frequency_words.txt
```

---

### 10. **Documentation** ⭐⭐
**Impact:** Medium for collaboration  
**Effort:** Low

**Create:**
- Architecture overview
- Dictionary entry guidelines
- Transfer rule examples
- Contributing guide

---

## 🎯 RECOMMENDED IMMEDIATE ACTION PLAN

**Week 1-2: Quick Wins (Get to 85% accuracy)**
1. ✅ Add top 100 missing vocabulary words (3 hours)
2. ✅ Fix adjective generation issues (2 hours)
3. ✅ Add Prpers pronoun mappings (30 min)
4. ✅ Test and verify fixes (1 hour)

**Expected Result:** ~85% accuracy ✅

**Week 3-4: Medium Improvements**
5. Transfer rule enhancements (accusative, adjectives)
6. Multiword unit basic handling
7. Expand CG rules (10 more rules)

**Expected Result:** ~88-90% accuracy

**Month 2+: Polish & Scale**
8. Comprehensive test suite
9. Bidirectional improvements
10. Documentation and community readiness

**Expected Result:** 90%+ accuracy, production-ready

---

## 📊 SUCCESS METRICS

**Current Status:**
- ✅ CG system implemented
- ✅ Critical fixes done (max→plej, esti→esas, da→di partial)
- ✅ Test sentences documented
- ⭐ **Current accuracy: ~70%**

**Milestone 1 (Immediate):** 85% accuracy
- Top 100 vocabulary added
- Adjective generation fixed
- Prpers pronouns working

**Milestone 2 (1 month):** 90% accuracy  
- Transfer rules enhanced
- MWU basic handling
- CG expanded

**Milestone 3 (2 months):** 93%+ accuracy
- Comprehensive coverage
- Bidirectional parity
- Production-ready

---

## 🚀 GETTING STARTED

**Start Here:**
```bash
# 1. Generate missing vocabulary list
cd /home/mark/apertium-dev/apertium-ido-epo
cat tests/interesting_sentences.txt TRANSLATION_ANALYSIS_TIBET.md | \
  grep -o '@[A-Za-z]*' | sort | uniq -c | sort -rn > missing_words.txt

# 2. Check adjective paradigm
echo "alta" | lt-proc ido-epo.automorf.bin
echo "^alta<adj>$" | lt-proc -g epo-ido.autogen.bin

# 3. Add Prpers mappings to apertium-ido-epo.ido-epo.dix

# 4. Test improvements
echo "Ĝi estas alta monto." | apertium -d . epo-ido
```

---

## 📝 NOTES

- **Prioritize vocabulary first** - highest ROI
- **Test frequently** - use interesting_sentences.txt as regression suite
- **Document patterns** - add to analysis docs as you discover them
- **Commit often** - small, focused commits are easier to debug

**Questions? Check:**
- `TRANSLATION_ANALYSIS_TIBET.md` - detailed pattern analysis
- `CG_OPTION_A_SUMMARY.txt` - CG implementation details
- `tests/interesting_sentences.txt` - working patterns

---

**Good luck! The foundation is solid - now it's mostly vocabulary and polish! 🎉**

