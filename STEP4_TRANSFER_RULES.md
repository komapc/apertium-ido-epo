# Step 4: Transfer Rule Development for EPO-IDO

## Transfer Rules to Add to `apertium-ido-epo.epo-ido.t1x`

### Rule Categories Needed

1. **Partitive Construction** - "da" → "di"
2. **Superlative Construction** - "plej ADJ" → "maxim ADJ"
3. **Ordinal Number Transformation** - "N-a" → "Nma"
4. **Pronoun Handling** - "oni", "ĝi" special cases

---

## 1. Partitive Construction: "da" → "di"

### Pattern Analysis
- **Input:** `QUANTIFIER da NOUN[plural]`
- **Output:** `QUANTIFIER di NOUN[plural]`
- **Example:** "miliardoj da kristanoj" → "miliardi di kristani"

### Category Definitions Needed

```xml
<def-cat n="partitive">
  <cat-item tags="pr"/>  <!-- partitive marker 'da' -->
</def-cat>

<def-cat n="quantifier">
  <cat-item tags="num.*"/>
  <cat-item tags="det.*"/>
  <cat-item tags="n.*.pl.*"/>  <!-- plural nouns as quantifiers -->
</def-cat>
```

### Transfer Rule

```xml
<rule comment="Partitive: QUANTIFIER da NOUN → QUANTIFIER di NOUN">
  <pattern>
    <pattern-item n="quantifier"/>
    <pattern-item n="partitive"/>
    <pattern-item n="nom"/>
  </pattern>
  <action>
    <out>
      <lu>
        <clip pos="1" side="tl" part="whole"/>
      </lu>
      <b pos="1"/>
      <lu>
        <lit v="di"/>
        <lit-tag v="pr"/>
      </lu>
      <b pos="2"/>
      <lu>
        <clip pos="3" side="tl" part="whole"/>
      </lu>
    </out>
  </action>
</rule>
```

---

## 2. Superlative Construction: "plej ADJ" → "maxim ADJ"

### Pattern Analysis
- **Input:** `plej ADJECTIVE`
- **Output:** `maxim ADJECTIVE`
- **Example:** "la plej granda" → "la maxim granda"

### Category Definitions Needed

```xml
<def-cat n="superlative">
  <cat-item lemma="plej" tags="adv"/>
</def-cat>
```

### Transfer Rule

```xml
<rule comment="Superlative: plej ADJ → maxim ADJ">
  <pattern>
    <pattern-item n="superlative"/>
    <pattern-item n="adj"/>
  </pattern>
  <action>
    <out>
      <lu>
        <lit v="maxim"/>
        <lit-tag v="adv"/>
      </lu>
      <b pos="1"/>
      <lu>
        <clip pos="2" side="tl" part="whole"/>
      </lu>
    </out>
  </action>
</rule>
```

### Alternative: With Article

```xml
<rule comment="Superlative with article: la plej ADJ → la maxim ADJ">
  <pattern>
    <pattern-item n="det"/>
    <pattern-item n="superlative"/>
    <pattern-item n="adj"/>
  </pattern>
  <action>
    <out>
      <lu>
        <clip pos="1" side="tl" part="whole"/>
      </lu>
      <b pos="1"/>
      <lu>
        <lit v="maxim"/>
        <lit-tag v="adv"/>
      </lu>
      <b pos="2"/>
      <lu>
        <clip pos="3" side="tl" part="whole"/>
      </lu>
    </out>
  </action>
</rule>
```

---

## 3. Ordinal Number Transformation: "N-a" → "Nma"

### Pattern Analysis
- **Input:** `NUMBER-a` (e.g., "1-a", "21-a")
- **Output:** `NUMBERma` (e.g., "1ma", "21ma")
- **Example:** "la 1-a jarcento" → "la 1ma yar-cento"

### Implementation Approach

**Option A: Dictionary-based** (simpler, limited range)
Add explicit entries for common ordinals (1st-31st, 100th, 1000th):

```xml
<!-- Already exists in bilingual dictionary -->
<e><p><l>unua<s n="adj"/></l><r>1ma<s n="adj"/></r></p></e>
<e><p><l>dua<s n="adj"/></l><r>2ma<s n="adj"/></r></p></e>
<!-- etc. up to 31st, 100th, 1000th -->
```

**Option B: Transfer rule** (more complex, unlimited range)
Would require regex/pattern matching in transfer rules - not standard in Apertium.

**Recommendation:** Use dictionary-based approach (Option A) - already implemented in current dictionary.

---

## 4. Pronoun Special Cases

### 4a. Impersonal "oni" → "on"

Handled primarily in dictionary, but transfer rule for context:

```xml
<rule comment="Impersonal pronoun oni → on">
  <pattern>
    <pattern-item n="prn"/>
  </pattern>
  <action>
    <choose>
      <when>
        <test>
          <equal>
            <clip pos="1" side="sl" part="lem"/>
            <lit v="oni"/>
          </equal>
        </test>
        <out>
          <lu>
            <lit v="on"/>
            <clip pos="1" side="tl" part="a_prn"/>
            <clip pos="1" side="tl" part="nbr"/>
            <clip pos="1" side="tl" part="cas"/>
          </lu>
        </out>
      </when>
      <otherwise>
        <out>
          <lu>
            <clip pos="1" side="tl" part="whole"/>
          </lu>
        </out>
      </otherwise>
    </choose>
  </action>
</rule>
```

### 4b. Neuter "ĝi" → "ol"

Handled in dictionary - entry exists but mapping needs verification.

---

## 5. Compound Superlative Phrases

### Pattern: "la plej ADJ NOUN"

```xml
<rule comment="Article + superlative + adjective + noun">
  <pattern>
    <pattern-item n="det"/>
    <pattern-item n="superlative"/>
    <pattern-item n="adj"/>
    <pattern-item n="nom"/>
  </pattern>
  <action>
    <out>
      <lu>
        <clip pos="1" side="tl" part="whole"/>
      </lu>
      <b pos="1"/>
      <lu>
        <lit v="maxim"/>
        <lit-tag v="adv"/>
      </lu>
      <b pos="2"/>
      <lu>
        <clip pos="3" side="tl" part="whole"/>
      </lu>
      <b pos="3"/>
      <lu>
        <clip pos="4" side="tl" part="whole"/>
      </lu>
    </out>
  </action>
</rule>
```

---

## Implementation Priority

### Phase 1: Critical (Immediate)
1. ✅ Category definitions for partitive, superlative
2. ✅ Partitive "da" → "di" rule
3. ✅ Superlative "plej" → "maxim" rule

### Phase 2: Important (After testing Phase 1)
4. Article + superlative rule (3-word pattern)
5. Article + superlative + adj + noun (4-word pattern)
6. Pronoun special case handling

### Phase 3: Refinement
7. Edge cases and exceptions
8. Compound expression handling

---

## Testing Strategy

### Unit Tests for Each Rule

```bash
# Test 1: Basic partitive
echo "miloj da homoj" | apertium -d . epo-ido
# Expected: "mili di homi"

# Test 2: Partitive with numbers
echo "2,4 miliardoj da kristanoj" | apertium -d . epo-ido
# Expected: "2,4 miliardi di kristani"

# Test 3: Basic superlative
echo "plej granda" | apertium -d . epo-ido
# Expected: "maxim granda"

# Test 4: Superlative with article
echo "la plej granda religio" | apertium -d . epo-ido
# Expected: "la maxim granda religio"

# Test 5: Full sentence with both
echo "Ĝi estas la plej granda el miloj da religioj" | apertium -d . epo-ido
# Expected: "Ol esas la maxim granda de mili di religii"
```

### Regression Testing

Create test file `test/kristanismo-patterns.txt`:

```
Oni kalkulas, ke estas miloj da kristanoj.
La plej granda religio en la mondo.
Ĝi originas en la 1-a jarcento.
```

---

## Current Transfer File Structure

The file `apertium-ido-epo.epo-ido.t1x` currently has:

1. **Section `<section-def-cats>`** - Category definitions
2. **Section `<section-def-attrs>`** - Attribute definitions
3. **Section `<section-def-vars>`** - Variable definitions
4. **Section `<section-rules>`** - Transfer rules

### Location to Add New Rules

Add new rules in the `<section-rules>` section, organized by priority:
1. High-frequency patterns first (partitive, superlative)
2. Special cases after general rules
3. More specific patterns before general patterns (to match first)

---

## Notes and Caveats

### Potential Conflicts

1. **"da" vs "de"** - Both translate to "di" in Ido, but:
   - "da" = partitive (of, quantity)
   - "de" = genitive (of, possession)
   - Solution: Context-based rules or dictionary distinction

2. **"plej" compounds** - Some entries exist as:
   - "plej-granda" (hyphenated)
   - "plej granda" (separate)
   - Solution: Handle both forms

3. **Ordinal detection** - Pattern "N-a" could match:
   - Actual ordinals: "1-a jarcento"  
   - False positives: Unlikely in practice
   - Solution: Dictionary approach is safer

### Testing Coverage Goals

- ✅ Partitive constructions: 100%
- ✅ Superlative constructions: 100%
- ✅ Pronouns (oni, ĝi): 100%
- ⚠️ Ordinals: 1-31, 100, 1000 (dictionary-based)
- ⚠️ Compound patterns: 80%+

---

_Document created: 2025-10-09_
_For: apertium-ido-epo transfer rules (epo-ido direction)_

