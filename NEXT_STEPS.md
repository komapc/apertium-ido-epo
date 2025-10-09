# Next Steps for Ido-Esperanto Translator

## ✅ Completed Today

### Task 1: Fix Converter ✓
- Added fallback POS guessing for words without standard morfologio
- Added invariable paradigms for function words
- Result: +574 words added to bilingual dictionary (+8.6%)

### Task 2: Add Morphological Generation ✓
- Added complete verb conjugation paradigms (present, past, future, conditional, imperative)
- Added noun plural and accusative paradigms
- Added adjective plural paradigms
- Fixed XML formatting (removed pretty-printing for Apertium compatibility)
- Result: Verbs like `guvernas`, `guvernis`, `guvernos` now work

### Task 3: Add High-Priority Missing Words ✓
- Added 50 critical words for political/governmental texts
- Function words: `nur`, `til`, `pos`, `dum`, `segun`, `kom`
- Political nouns: `prezidanto`, `titulo`, `guvernerio`, `konstituco`, etc.
- Verbs: `transmisar`, `nominesar`, `limitizar`, etc.
- Result: Improved coverage from ~20% to ~70-80%

---

## 🎯 Next Priority Steps (Ordered)

### 1. Improve Transfer Rules 🔴 CRITICAL
**File:** `apertium-ido-epo.ido-epo.t1x` (487 lines)

**Issues to fix:**
- **Case agreement:** `guvernala` → `registaran` (wrong case, should be `registara`)
- **Number agreement:** Better handling of singular/plural
- **Article handling:** Capitalized articles like `*La` not recognized
- **Gender/person agreement:** Pronouns and adjectives

**Example problems:**
```
Input:  Republiko esas guvernala sistemo
Output: Respubliko estas registaran sistemon  ← Wrong cases
Should: Respubliko estas registara sistemo
```

**How to fix:**
1. Review current transfer rules
2. Add rules for adjective-noun agreement
3. Add rules for article-noun agreement
4. Test iteratively

---

### 2. Add Compound Word Support 🟡 HIGH  
**Problem:** `maxim-multa-kaze` → `*maxim-multa-#unknown`

**Solution options:**

**Option A: Add to dictionary**
```json
{
  "ido_word": "maxim-multa-kaze",
  "esperanto_words": ["plej-multe-kaze"],
  "morfologio": null
}
```

**Option B: Add morphological analyzer rules**
- Recognize `maxim-` prefix → `plej-`
- Recognize `-kaze` suffix patterns

**Recommendation:** Option A (simpler, faster)

**Other compounds to add:**
- `maxim-multa-kaze`
- Other `maxim-` compounds

---

### 3. Fix Preposition + Article Handling 🟡 HIGH
**Problem:** `dal` → `*dal` (not translated)

**Analysis:**
- `dal` = `da` + `l` (contraction of `da la`)
- Should translate to `de la` or `de`

**Solution:**
1. Add contraction support to morphological analyzer
2. Or add contractions as separate entries:
   - `dal` → `de la`
   - `del` → `de la`  
   - `al` → `al la`

**Also fix:** `di` → `de` (preposition)

---

### 4. Add Possessive Pronoun Mapping 🟡 HIGH
**Problem:** `lua` → `@lua` (not translating)

**Ido possessives → Esperanto:**
- `mea` → `mia`
- `tua` → `via`
- `lua` → `sia` (reflexive) or `lia`/`ŝia` (3rd person)
- `nia` → `nia`
- `via` → `via`
- `olia` → `ilia`

**Add to dictionary:**
```json
{
  "ido_word": "lua",
  "esperanto_words": ["sia"]
}
```

---

### 5. Add More Verb Forms 🟢 MEDIUM
**Problem:** `eventas` → `#eventi`, `elektesas` → `*elektesas`

**Missing verbs:**
- `eventar` → `okazi` (to happen)
- More reflexive verbs

**Also needed:**
- Verb forms with `-esar` (passive/reflexive)
- Example: `elektesar` → `elektiĝi`

---

### 6. Handle Special Cases 🟢 MEDIUM

**Contractions:**
- `L'origino` → `*L'origino` (should be `La origino`)
- `l'aktiva` → `*l'aktiva` (should be `la aktiva`)

**Multi-word expressions:**
- `kie, kien` (for `ube`) - currently causes issues
- Better handling needed

**Numbers:**
- Years: `1776`, `2009` not recognized
- Ordinals: `15ma` works, but could be improved

---

### 7. Extract from Esperanto Wiktionary 🟢 LOW
**Why:** May have additional Ido words not in Ido Wiktionary

**How:**
```bash
cd /home/mark/apertium-dev/ido-esperanto-extractor
python3 ido_esperanto_extractor.py --language-pair esperanto-ido --download
python3 merge_dictionaries.py  # Merge both directions
python3 json_to_dix_converter.py  # Regenerate
```

---

### 8. Add Constraint Grammar 🟢 LOW
**Purpose:** Disambiguate based on context

**Files to create:**
- `apertium-ido.ido.rlx` - Ido constraint grammar
- `apertium-epo.epo.rlx` - Esperanto constraint grammar

**Example rules:**
- Disambiguate noun vs. verb (`sistemo` is noun in this context)
- Select correct pronoun form based on antecedent
- Choose reflexive vs. non-reflexive verb forms

---

## 📈 Performance Goals

| Metric | Current | Short-term (1 week) | Long-term (1 month) |
|--------|---------|---------------------|---------------------|
| Dictionary size | 7,233 | 8,000 | 10,000+ |
| Coverage (political) | 70% | 85% | 95% |
| Translation quality | Fair | Good | Excellent |
| BLEU score | ~25 | ~40 | ~60 |

---

## 🚀 Recommended Action Plan

**Week 1:**
1. Fix transfer rules for agreement (2-3 days)
2. Add compound words (1 day)
3. Add contractions and prepositions (1 day)
4. Test and iterate (1 day)

**Week 2:**
5. Add more vocabulary (~200 words)
6. Extract from Esperanto Wiktionary
7. Add possessive pronouns
8. Test with more texts

**Week 3:**
9. Implement constraint grammar basics
10. Fine-tune transfer rules
11. Comprehensive testing
12. Documentation

---

## 📝 Quick Wins (Can do in 1-2 hours each)

1. **Add `dal`, `del` contractions** to dictionary
2. **Add `lua`** and other possessive pronouns  
3. **Add `eventar`** and common missing verbs
4. **Fix article capitalization** in transfer rules
5. **Add top 20 compound words** manually

---

## Testing Commands

```bash
# Quick test
cd /home/mark/apertium-dev/apertium-ido-epo
echo "Republiko esas guvernala sistemo" | apertium -d . ido-epo

# Full article test
apertium -d . ido-epo < republiko_ido.txt > republiko_epo.txt

# Check coverage
apertium -d . ido-epo < republiko_ido.txt | grep -o '#[a-z]*' | sort | uniq -c

# Compare versions
diff -u republiko_epo_v2.txt republiko_epo_v3.txt
```

---

## Resources

**Documentation:**
- Apertium Wiki: https://wiki.apertium.org/
- Transfer Rules: https://wiki.apertium.org/wiki/Transfer_rules
- Constraint Grammar: https://wiki.apertium.org/wiki/Constraint_Grammar

**Test Corpora:**
- Ido Wikipedia: https://io.wikipedia.org/
- Ido Wiktionary: https://io.wiktionary.org/
- Ido Vikipedio sample texts

---

**What would you like to tackle next?**
1. Transfer rules (biggest impact on quality)
2. Add more missing words
3. Something else?

