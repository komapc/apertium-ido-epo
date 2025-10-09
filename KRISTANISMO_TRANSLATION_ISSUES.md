# Kristanismo Translation Issues - Esperanto to Ido

## Step 2: Prioritized Translation Issues

### Current Baseline Performance

**Test Input:** "Kristanismo estas tutmonda religio bazita sur la instruoj de Jesuo Kristo."
**Current Output:** `@Kristanismo @esti @tutmonda religio #bazar @sur @la @instruo @de @Jesuo @Kristo@.@`
**Issues:** Multiple missing dictionary entries, incorrect analysis

**Test Input:** "Ĝi estas la plej granda religio en la mondo."
**Current Output:** `@Prpers @esti @la plej granda religio en @la mondo@.@`
**Issues:** Pronoun not translated, "plej" not handled, duplicate "la"

**Test Input:** "Oni kalkulas, ke ekzistas ĉirkaŭ 2,4 miliardoj da kristanoj."
**Current Output:** `@Oni kontas@, ke @ekzisti cirke @2,4 miliardi @da #Kristano@.@`
**Issues:** "Oni" not translated, "da" not converted to "di", verb form issues

---

## Priority Classification

### HIGH PRIORITY (Systematic/Frequent Patterns)

#### 1. **Partitive Construction: "da" → "di"**
- **Frequency:** Very common with quantities
- **Pattern:** `NUMBER/QUANTITY da NOUN` → `NUMBER/QUANTITY di NOUN`
- **Current Status:** "da" appears untranslated (@da)
- **Solution:** Transfer rule + bilingual dictionary entry
- **Examples:**
  - "miliardoj da kristanoj" → "miliardi di kristani"
  - "taso da kafo" → "taso di kafeo"

#### 2. **Superlative: "plej" → "maxim"**
- **Frequency:** Very common in descriptive text
- **Pattern:** `plej ADJECTIVE` → `maxim ADJECTIVE`
- **Current Status:** "plej" passes through unchanged
- **Solution:** Transfer rule for superlative construction
- **Examples:**
  - "la plej granda" → "la maxim granda"
  - "plej bona" → "maxim bona"

#### 3. **Impersonal Pronoun: "oni" → "on"**
- **Frequency:** Very common, formal writing
- **Pattern:** Subject pronoun
- **Current Status:** Not in dictionary (@Oni)
- **Solution:** Add to bilingual dictionary with proper POS tags
- **Examples:**
  - "Oni diras" → "On dicas"
  - "Oni kredas" → "On kredas"

#### 4. **Neuter Pronoun: "ĝi" → "ol"**
- **Frequency:** Very common for inanimate objects
- **Pattern:** Third-person neuter
- **Current Status:** Appears as @Prpers (analysis exists but not in bilingual)
- **Solution:** Add to bilingual dictionary
- **Examples:**
  - "Ĝi estas granda" → "Ol esas granda"
  - "ĝin" → "olu" (accusative)

#### 5. **Ordinal Number Suffix: "-a" → "-ma"**
- **Frequency:** Common in historical/sequential contexts
- **Pattern:** `NUMBER + -a` → `NUMBER + -ma`
- **Current Status:** Unknown
- **Solution:** Transfer rule for ordinal transformation
- **Examples:**
  - "1-a jarcento" → "1ma yar-cento"
  - "2-a libro" → "2ma libro"

---

### MEDIUM PRIORITY (Vocabulary/Lexical)

#### 6. **Common Adverbs**
- "ĉirkaŭ" → "cirkum" (approximately) - **DONE** (appears as "cirke" in output)
- Need to verify other common adverbs

#### 7. **Core Vocabulary Gaps**
Missing essential words identified:
- "kristanismo" → "kristanismo" (Christianity)
- "tutmonda" → "tut-mondala" (worldwide)
- "bazita" → "bazita" (based)
- "instruoj" → "instruadi" (teachings)
- "mondo" → "mondo" (world)
- "ekzisti" → "existar" (to exist)

#### 8. **Religious/Specialized Vocabulary**
- "Jesuo"/"Kristo" → "Iesu"/"Kristo" (Jesus/Christ)
- "religio" → "religio" (religion)
- "kristano" → "kristano" (Christian)

#### 9. **Geographic Names**
- "Judujo" → "Judea" (Judea/Judaea)
- Need systematic approach to geographic name conversion

---

### LOW PRIORITY (Edge Cases)

#### 10. **Compound Word Hyphenation**
- EO: "jarcento" (year-century)
- IO: "yar-cento" (hyphenated)
- Frequency: Moderate, affects readability
- Solution: Dictionary entries or post-processing

#### 11. **Rare Vocabulary Differences**
- Handle as discovered through corpus analysis
- Build over time through testing

---

## Step 6: Systematic Pattern Analysis

### Pattern 1: Partitive "da" Usage

**Search Query:** All occurrences of "da" as partitive marker

**Expected Pattern:**
```
QUANTIFIER da NOUN[plural]
```

**Examples from Wikipedia:**
- "2,4 miliardoj da kristanoj" (2.4 billion Christians)
- "miloj da homoj" (thousands of people)
- "multe da tempo" (much time)

**Transfer Rule Needed:** Convert "da" → "di" in partitive context

---

### Pattern 2: Superlative "plej + ADJ"

**Search Query:** All "plej ADJECTIVE" constructions

**Expected Pattern:**
```
[ARTICLE] plej ADJECTIVE [NOUN]
```

**Examples from Wikipedia:**
- "la plej granda religio" (the largest religion)
- "plej grava artikolo" (most important article)
- "plej multaj sekvantoj" (most followers)

**Transfer Rule Needed:** Replace "plej" with "maxim"

---

### Pattern 3: Pronoun "ĝi" Usage

**Search Query:** All forms of "ĝi"

**Forms:**
- "ĝi" (nominative) → "ol"
- "ĝin" (accusative) → "olu"
- "al ĝi" (dative) → "ad ol"
- "ĝia" (possessive) → "olu" / "olua"

**Examples from Wikipedia:**
- "Ĝi estas la plej granda" → "Ol esas la maxim granda"
- "oni kredas ĝin" → "on kredas olu"

---

### Pattern 4: Pronoun "oni" Usage

**Search Query:** All forms of "oni"

**Forms:**
- "oni" (nominative) → "on"
- "onin" (accusative) → "onu"
- "al oni" (dative) → "ad on"

**Examples from Wikipedia:**
- "Oni kalkulas" → "On kalkulas"
- "oni diras" → "on dicas"

---

### Pattern 5: Ordinal Numbers

**Search Query:** Pattern `\d+-a`

**Forms:**
- "1-a" → "1ma" (first)
- "2-a" → "2ma" (second)
- "21-a" → "21ma" (twenty-first)

**Examples from Wikipedia:**
- "en la 1-a jarcento" → "en la 1ma yar-cento"
- "la 4-a libro" → "la 4ma libro"

---

## Corpus Statistics Needed

### To Extract:
1. **Frequency count of "da" constructions** - Estimate impact
2. **Frequency count of "plej + adjective"** - Estimate impact
3. **Frequency count of "ĝi" vs "li/ŝi/ili"** - Pronoun distribution
4. **Frequency count of "oni" usage** - Impersonal constructions
5. **Frequency count of ordinals** - Historical/sequential contexts

### Sample Size:
- Kristanismo article: ~3,000 words
- 5 additional Wikipedia articles for validation
- Target: 15,000+ word corpus

---

## Success Metrics

### Before Fixes:
- **Unknown words (@):** ~60% of test sentences
- **Incorrect constructions (#):** ~20% of test sentences
- **Accurate translation:** ~20%

### Target After Fixes:
- **Unknown words (@):** <10%
- **Incorrect constructions (#):** <5%
- **Accurate translation:** >85%

---

## Implementation Order

1. ✅ Document issues (this file)
2. ⏳ Add dictionary entries (Step 3)
3. ⏳ Create transfer rules (Step 4)
4. ⏳ Build test corpus (Step 6)
5. ⏳ Validate and iterate
6. ⏳ Document final coverage

---

_Document created: 2025-10-09_
_Test article: https://eo.wikipedia.org/wiki/Kristanismo_

