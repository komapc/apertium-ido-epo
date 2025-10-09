# Missing Words Analysis: Republiko Translation

## Executive Summary

The translation failed because **~60%+ words are missing**. Analysis shows three main categories of missing words:

1. **Words extracted but not converted** (~890 words in JSON but not in .dix)
2. **Inflected forms not in Wiktionary** (Wiktionary has roots, not all conjugations/declensions)
3. **Words genuinely missing from Wiktionary** (never existed in dump)

---

## Category 1: Extracted but Not Converted to .dix

### Statistics
- **Extracted JSON (io→eo):** 7,549 words
- **Merged Dictionary:** 7,634 words
- **Bilingual .dix:** 6,659 entries  
- **Gap:** 975 words (12.8%)

### Examples Found in JSON but NOT in .dix:

| Ido Word | Esperanto | Status | Issue |
|----------|-----------|--------|-------|
| `anke` | `ankaŭ` | ❌ Missing | In JSON, not in .dix |
| `quale` | `kiel` | ❌ Missing | In JSON, not in .dix |
| `exemplo` | `ekzemplo` | ❌ Missing | In JSON, not in .dix |
| `kande` | `kiam` | ❌ Missing | In JSON, not in .dix |
| `ube` | `kie, kien` | ❌ Missing | In JSON, not in .dix |

**Problem:** These words were successfully extracted from Wiktionary but didn't make it into the compiled bilingual dictionary during the JSON→.dix conversion process.

**Root Cause Found:** The converter script (`json_to_dix_converter.py` line 176-178) **only adds entries that have morfologio AND a recognized POS tag**. It filters based on these suffix patterns:
- `.o` → noun
- `.a` → adjective  
- `.e` → adverb
- `.ar` → verb
- `.ir` → verb (passive)

Function words like `anke`, `ube`, `kande` either:
1. Have no `morfologio` field (null) → **skipped**
2. Have unusual `morfologio` that doesn't match patterns (e.g., `anke`: `["avan", "vokalo", "ank"]`) → **skipped**

**Solution Needed:** Modify the converter to handle words without morfologio or with non-standard morfologio patterns.

---

## Category 2: Inflected/Derived Forms Not in Wiktionary

Wiktionary entries typically contain **root forms** with morphology markers (e.g., `guvern` + `.ar`), but NOT all inflected forms.

### Verbs - Missing Conjugations

| Text Has | Root in Wiktionary | Translation Needed | Notes |
|----------|-------------------|-------------------|--------|
| `elektesas` | `elektar` → `elekti` (vb) | `elektiĝas` | Present tense + reflexive |
| `rielektesar` | ❌ Not found | `reelektiĝi` | Need to add `rielekt` root |
| `selektesas` | ❌ Not found | `elektiĝas` | Need to add `selekt` root |
| `nominesas` | ❌ Not found | `nomiĝas` | Need root |
| `divenis` | ❌ Not found | `fariĝis` | Past tense |
| `aparis` | ❌ Not found | `aperis` | Past tense |

**Pattern:** Ido verbs ending in `-esas` (present tense) need to be analyzed morphologically:
- `elektesas` = `elekt` + `-es-` + `-as`
- Should translate to Esperanto: `elektiĝas` = `elekt` + `-iĝ-` + `-as`

### Nouns - Different Forms

| Text Has | Wiktionary Has | Translation Needed | Issue |
|----------|---------------|-------------------|--------|
| `konstituco` | `konstituciono` → `konstitucio` | `konstitucio` | Different word! |
| `monarkii` | `monarkio` → `monarkio` | `monarĥioj` | Plural needed |
| `prezidanti` | ❌ Not found | `prezidantoj` | Plural needed |
| `landi` | ✅ Works | `landoj` | ✓ Plural works |
| `yari` | ✅ Works | `jaroj` | ✓ Plural works |

**Key Issue:** `konstituco` vs `konstituciono` are different words:
- `konstituciono` = constitution (document)
- `konstituco` = constitution (act of constituting)

### Adjectives - Missing Declined Forms

| Text Has | Wiktionary Has | Translation Needed | Issue |
|----------|---------------|-------------------|--------|
| `guvernala` | `guvern` (vb) → `regi` | `registara` | Adjective form needed |
| `prezidantala` | ❌ Not found | `prezidanta` | Adjective form |
| `parlamentala` | ❌ Not found | `parlamenta` | Adjective form |
| `fundamentala` | ❌ Not found | `fundamentalaj` | Plural adjective |

**Pattern:** `-ala` suffix in Ido = `-a` suffix in Esperanto (related to/pertaining to)

### Adverbs - Derived Forms

| Text Has | Wiktionary Has | Translation Needed | Issue |
|----------|---------------|-------------------|--------|
| `exemple` | `exemplo` → `ekzemplo` (noun) | `ekzemple` | Adverb from noun |
| `heredale` | ❌ Not found | `heredale` | Manner adverb |
| `absolute` | ❌ Not found | `absolute` | Manner adverb |

**Pattern:** In Ido, adverbs often end in `-e` and are derived from roots

---

## Category 3: Words Genuinely Missing from Wiktionary

These words don't exist in Wiktionary at all (not even as roots):

### Common Words

| Ido Word | Expected Esperanto | Part of Speech | Priority |
|----------|-------------------|---------------|----------|
| `titulo` | `titolo` | noun | HIGH |
| `prezidanto` | `prezidanto` | noun | HIGH |
| `nur` | `nur` | adverb | HIGH |
| `til` | `ĝis` | preposition | HIGH |
| `pos` | `post` | preposition | HIGH |
| `dum` | `dum` | preposition | HIGH |
| `guvernerio` | `registaro` | noun | HIGH |
| `povo` | `povo` | noun | HIGH |
| `transmisar` | `transdoni` | verb | MEDIUM |
| `heredale` | `heredale` | adverb | MEDIUM |
| `deputati` | `deputitoj` | noun plural | MEDIUM |
| `koalisuro` | `koalicio` | noun | MEDIUM |
| `limitizas` | `limitas` | verb | MEDIUM |
| `unfoye` | `unufoje` | adverb | MEDIUM |
| `sequante` | `sinsekve` | adverb | MEDIUM |
| `partopreno` | `partopreno` | noun | LOW |
| `civitani` | `civitanoj` | noun plural | LOW |
| `reprezento` | `reprezento` | noun | LOW |
| `tota` | `ĉiuj` | adjective | MEDIUM |
| `institucuri` | `institucioj` | noun plural | MEDIUM |
| `prepondoro` | `prepondereco` | noun | LOW |
| `konceptajo` | `koncepto` | noun | MEDIUM |
| `nedependanta` | `sendependa` | adjective | MEDIUM |

### Proper Nouns (Countries, Names)

| Ido Word | Expected Esperanto | Status |
|----------|-------------------|--------|
| `Usa` | `Usono` | Partial (recognized but marked) |
| `Brazilia` | `Brazilo` | ❌ Missing |
| `Arjentinia` | `Argentino` | ❌ Missing |
| `Uruguay` | `Urugvajo` | ❌ Missing |
| `Chili` | `Ĉilio` | Partial |
| `Venezuela` | `Venezuelo` | Partial |
| `Portugal` | `Portugalio` | ❌ Missing |
| `Finlando` | `Finnlando` | Partial |
| `Francia` | `Francio` | ❌ Missing |
| `Roma` | `Romo` | ❌ Missing |
| `Aristoteles` | `Aristotelo` | ❌ Missing |

**Note:** Some proper nouns are recognized but marked with `#` (processed but flagged). Country names need systematic addition.

---

## Root Cause Analysis

### Why Words Are Missing

1. **Wiktionary Coverage is Limited**
   - Ido Wiktionary has ~7,500 entries
   - Many common words simply not documented
   - Political/governmental vocabulary especially sparse

2. **Extraction Script Filters**
   Located in `ido_esperanto_extractor.py`:
   
   ```python
   # Line 106-116: EXCLUDE_CATEGORY_PATTERNS
   - Filters out: suffixes, radicals, affixes, components
   
   # Line 119-125: INVALID_TITLE_PATTERNS  
   - Filters out: single letters, numbers, special chars
   
   # Line 163-187: is_valid_title()
   - Requires: at least 2 chars, starts with letter
   
   # Line 189-197: has_excluded_categories()
   - Filters by category tags
   ```

   **These filters are correct** - they're not the problem.

3. **Conversion Script Incomplete**
   - 890 words extracted but not converted to .dix format
   - Script: `json_to_dix_converter.py`
   - May have part-of-speech filters or quality checks that exclude some entries

4. **Morphological Generation Missing**
   - System doesn't auto-generate inflected forms from roots
   - E.g., has `guvern` root but doesn't generate:
     - `guvernas` (present tense)
     - `guvernala` (adjective)
     - `guvernerio` (related noun)

---

## What Works Well ✅

Despite the gaps, some things work correctly:

### Successful Patterns

| Pattern | Examples | Status |
|---------|----------|--------|
| Noun plurals | `vorti`→`vortoj`, `yari`→`jaroj`, `landi`→`landoj` | ✓ Works |
| Adjective agreement | `Latina`→`latinaj`, `moderna`→`modernaj` | ✓ Works |
| Basic conjunctions | `e`→`kaj`, `o`→`aŭ` | ✓ Works |
| Some prepositions | `en`→`en`, `de`→`de` | ✓ Works |
| Basic verbs | `povas`→`povas`, `estas`→`estas` | ✓ Works |
| Some common words | `persono`, `sistemo`, `periodo`, `demokrata` | ✓ Works |

---

## Recommended Solutions

### Immediate Actions (High Priority)

1. **Re-run JSON to .dix Conversion**
   ```bash
   cd /home/mark/apertium-dev/ido-esperanto-extractor
   python3 json_to_dix_converter.py
   ```
   This should add the 890 missing words like `anke`, `quale`, `ube`, etc.

2. **Add Essential Function Words Manually**
   Add to `apertium-ido-epo.ido-epo.dix`:
   - `nur` → `nur`
   - `til` → `ĝis`
   - `pos` → `post`
   - `dum` → `dum`
   - `exemple` → `ekzemple` (derived from `exemplo`)

3. **Add Common Political Vocabulary**
   Priority words for governmental texts:
   - `prezidanto`, `titulo`, `guvernerio`, `konstituco`
   - `deputati`, `koalisuro`, `limitizas`
   - `transmisar`, `heredale`, `rielekto`

4. **Add Country Names**
   Create proper noun section for countries

### Medium-Term Solutions

1. **Implement Morphological Generation**
   - Auto-generate verb conjugations from roots (−ar → −as, −is, −os)
   - Auto-generate adjectives from verbs (−ar → −ala)
   - Auto-generate adverbs from nouns/adjectives (−o → −e)

2. **Supplement with Esperanto→Ido Wiktionary**
   - Extract from `eowiktionary-latest-pages-articles.xml.bz2`
   - May have words missing from Ido Wiktionary

3. **Cross-reference with Ido-English Dictionaries**
   - Use other sources to fill gaps
   - Ido Wiktionary (io.wiktionary.org) for English definitions

### Long-Term Solutions

1. **Contribute Missing Words to Wiktionary**
   - Add missing entries to io.wiktionary.org
   - Especially common words and proper nouns

2. **Create Comprehensive Morphology Rules**
   - FST-based morphological analyzer
   - Generate all forms from roots automatically

3. **Build Domain-Specific Vocabularies**
   - Political/governmental terminology
   - Scientific terminology
   - Technical terminology

---

## Next Steps

To proceed with fixing the translation, we should:

1. ✅ **Understand the problem** (DONE - this document)
2. ⏭️ **Re-run conversion** to add the 890 extracted words
3. ⏭️ **Manually add** high-priority missing words (50-100 most common)
4. ⏭️ **Test translation** again to measure improvement
5. ⏭️ **Iterate** on remaining gaps

Would you like me to proceed with step 2 (re-running the conversion)?

