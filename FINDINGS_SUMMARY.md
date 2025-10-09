# Summary: Why Words Are Missing

## Quick Answer

**Most missing words fall into 3 categories:**

### ✅ Category 1: In Dump, Extracted, But Filtered During Conversion (975 words, ~13%)
- **Status:** In JSON, NOT in .dix
- **Examples:** `anke`, `ube`, `kande`, `quale`
- **Cause:** Converter script filters out words without standard morfologio patterns
- **Fix:** Modify converter to include function words

### ⚠️ Category 2: Base Forms Only, Missing Inflections  
- **Status:** Root exists, inflected forms missing
- **Examples:** `elektesas` (has `elektar`), `guvernala` (has `guvern`)
- **Cause:** Wiktionary has roots (`.ar`, `.o`), not conjugated/declined forms
- **Fix:** Add morphological generation or manual entries

### ❌ Category 3: Never in Wiktionary (~100+ high-priority words)
- **Status:** Not in dump at all
- **Examples:** `prezidanto`, `titulo`, `nur`, `til`, `pos`
- **Cause:** Simply not documented in Ido Wiktionary
- **Fix:** Manual addition required

---

## Detailed Findings

### 1. The Converter Filter Problem (ROOT CAUSE)

**File:** `ido-esperanto-extractor/json_to_dix_converter.py` (lines 176-193)

**How it works:**
```python
for word_entry in self.data['words']:
    ido_word = word_entry.get('ido_word', '')
    esperanto_words = word_entry.get('esperanto_words', [])
    morfologio = word_entry.get('morfologio', [])
    
    # Analyze morphology to get POS
    root, pos_tag, suffixes = self.analyze_morfologio(morfologio)
    
    if pos_tag:  # ← ONLY adds entries with recognized POS!
        # Create bilingual entry
        ...
```

**Recognized patterns:**
- `.o` → noun (e.g., `exemplo` → `ekzemplo`)
- `.a` → adjective (e.g., `granda` → `granda`)
- `.e` → adverb (e.g., `quale` → `kiel`)
- `.ar` → verb (e.g., `elektar` → `elekti`)
- `.ir` → verb passive

**What gets filtered:**
```json
// anke - has weird morfologio, doesn't match .e pattern
{
  "ido_word": "anke",
  "esperanto_translations": [["ankaŭ"]],
  "morfologio": ["avan", "vokalo", "ank"]  ← doesn't end with .e
}

// ube - no morfologio at all
{
  "ido_word": "ube",
  "esperanto_translations": [["kie, kien"]],
  "morfologio": null  ← no morphology info
}

// kande - no morfologio
{
  "ido_word": "kande",
  "esperanto_translations": [["kiam"]],
  "morfologio": null
}
```

**Impact:** ~975 words (12.8%) filtered out, including many essential function words.

---

### 2. Inflection/Derivation Problem

Wiktionary entries contain **dictionary forms** (lemmas), not inflected forms.

#### Example: Verb Conjugations

**What Wiktionary has:**
```json
{
  "ido_word": "elektar",  // infinitive
  "esperanto_translations": [["elekti"]],
  "morfologio": ["elekt", ".ar"]
}
```

**What the text needs:**
- `elektesas` (present tense) → should be `elektiĝas`
- `elektis` (past tense) → should be `elektis`
- `elektos` (future tense) → should be `elektos`

**Current system behavior:** 
- Has root `elektar` in dictionary
- Cannot generate `elektesas` because no morphological analyzer
- Result: `#unknown`

#### Example: Noun Declension

**What Wiktionary has:**
```json
{
  "ido_word": "monarkio",  // singular
  "esperanto_translations": [["monarkio"]],
  "morfologio": ["monark", ".i.o"]
}
```

**What the text needs:**
- `monarkii` (plural) → should be `monarĥioj`

**Current system behavior:**
- Has singular `monarkio`
- Cannot generate plural `monarkii` 
- Result: `#unknown`

#### Example: Adjective Derivation

**What Wiktionary has:**
```json
{
  "ido_word": "guvernar",  // verb
  "esperanto_translations": [["regi"]],
  "morfologio": ["guvern", ".ar"]
}
```

**What the text needs:**
- `guvernala` (adjective "governmental") → should be `registara`
- `guvernerio` (noun "government") → should be `registaro`

**Current system behavior:**
- Has verb `guvernar` 
- Cannot derive adjective `guvernala` or noun `guvernerio`
- Result: `#unknown`

---

### 3. Simply Not in Wiktionary

These words don't exist in Ido Wiktionary at all:

#### High-Priority Function Words (0/6)
- `nur` → `nur` (only)
- `til` → `ĝis` (until)
- `pos` → `post` (after)
- `dum` → `dum` (during)
- `segun` → `laŭ` (according to)
- `kom` → `kiel` (as, like)

#### Essential Nouns (0/15)
- `prezidanto` → `prezidanto` (president)
- `titulo` → `titolo` (title)
- `guvernerio` → `registaro` (government)
- `povo` → `povo` (power)
- `konstituco` → `konstitucio` (constitution)
- `deputati` → `deputitoj` (deputies)
- `koalisuro` → `koalicio` (coalition)
- `partopreno` → `partopreno` (participation)
- `civitani` → `civitanoj` (citizens)
- `reprezento` → `reprezento` (representation)
- `institucuri` → `institucioj` (institutions)
- `prepondoro` → `prepondereco` (preponderance)
- `konceptajo` → `koncepto` (concept)

Note: `konstituciono` exists but `konstituco` is a different word!

#### Essential Verbs (0/10)
- `transmisar` → `transdoni` (transmit)
- `nominesas` → `nomiĝas` (is called)
- `limitizas` → `limitas` (limits)
- `aparis` → `aperis` (appeared)
- `divenis` → `fariĝis` (became)
- `adoptis` → `adoptis` (adopted)
- `rielektesar` → `reelektiĝi` (be re-elected)
- `disputar` → `disputi` (contest)

#### Essential Adjectives/Adverbs (0/10)
- `exemple` → `ekzemple` (for example)
- `heredale` → `heredale` (hereditarily)
- `absolute` → `absolute` (absolutely)
- `nedependanta` → `sendependa` (independent)
- `fundamentala` → `fundamentalaj` (fundamental)
- `unfoye` → `unufoje` (once)
- `sequante` → `sinsekve` (consecutively)
- `tota` → `ĉiuj` (all)

#### Proper Nouns (0/11)
- `Roma` → `Romo` (Rome)
- `Brazilia` → `Brazilo` (Brazil)
- `Arjentinia` → `Argentino` (Argentina)
- `Uruguay` → `Urugvajo` (Uruguay)
- `Chili` → `Ĉilio` (Chile)
- `Venezuela` → `Venezuelo` (Venezuela)
- `Portugal` → `Portugalio` (Portugal)
- `Francia` → `Francio` (France)
- `Aristoteles` → `Aristotelo` (Aristotle)

Note: Some like `Usa`, `Finlando` are partially recognized.

---

## Why This Happened

### Wiktionary Limitations
1. **Small size:** Ido Wiktionary has only ~7,500 entries
2. **Limited scope:** Focuses on basic vocabulary
3. **Missing domains:** Political, technical, scientific terms sparse
4. **Lemmas only:** Dictionary forms, not inflections

### Extraction Decisions
The filters in `ido_esperanto_extractor.py` are **correct**:
- Exclude suffixes/radicals ✓
- Exclude invalid titles ✓  
- Exclude malformed entries ✓

These prevent garbage from entering the dictionary.

### Conversion Decisions
The filters in `json_to_dix_converter.py` are **too strict**:
- Requiring morfologio ✗ (loses function words)
- Requiring standard patterns ✗ (loses irregular words)
- No fallback for words without morfologio ✗

### System Design Limitations
- No morphological analyzer to generate forms
- No derivation rules (verb → adjective, noun → adverb)
- No manual supplement for common words
- No proper noun handling

---

## What Works Well ✅

Despite gaps, some patterns work correctly:

| Feature | Examples | Status |
|---------|----------|--------|
| Noun plurals | `vorti`→`vortoj`, `landi`→`landoj` | ✓ |
| Adjective agreement | `moderna`→`modernaj` | ✓ |
| Basic conjunctions | `e`→`kaj`, `o`→`aŭ` | ✓ |
| Some prepositions | `en`→`en`, `de`→`de` | ✓ |
| Core vocabulary | `persono`, `sistemo`, `demokrata` | ✓ |

---

## Verification Commands

```bash
# Check extracted JSON
cd /home/mark/apertium-dev/ido-esperanto-extractor
jq '.metadata.total_words' dictionary_io_eo.json  # 7,549

# Check merged dictionary
jq '.words | length' dictionary_merged.json  # 7,634

# Check bilingual dictionary
cd /home/mark/apertium-dev/apertium-ido-epo
grep -c '<e>' apertium-ido-epo.ido-epo.dix  # 6,659

# Check specific word
jq '.words[] | select(.ido_word == "anke")' dictionary_merged.json
```

---

## Conclusion

**Main findings:**
1. ✅ **Not a filter problem** - extraction filters are appropriate
2. ⚠️ **Converter is too strict** - loses 975 words (13%) with non-standard morfologio  
3. ❌ **Wiktionary coverage gaps** - ~100+ essential words missing
4. ⚠️ **No morphological generation** - can't handle inflections

**Recommendation:** Fix converter first (biggest impact), then add missing words manually.

