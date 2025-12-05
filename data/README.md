# Source Data

This directory contains source data used for generating dictionaries.

## Files

### `pardefs.xml`
Paradigm definitions for Ido morphology.

**CRITICAL FORMAT REQUIREMENT:**
All `<s/>` tags within `<r>` elements MUST be on a single line without whitespace between them.

**Correct:**
```xml
<r><s n="n"/><s n="pl"/><s n="nom"/></r>
```

**Incorrect (causes morphological analyzer to output tags with newlines):**
```xml
<r>
  <s n="n"/>
  <s n="pl"/>
  <s n="nom"/>
</r>
```

## Why This Matters

The Apertium morphological analyzer (`lt-proc`) interprets whitespace in the paradigm definitions literally. If tags are spread across multiple lines with indentation, the compiled transducer will output tags with embedded newlines, breaking the translation pipeline at the bilingual dictionary lookup stage.

## Paradigms Defined

- `o__n` - Nouns ending in -o (singular: -o, plural: -i)
- `a__adj` - Adjectives ending in -a
- `e__adv` - Adverbs ending in -e
- `ar__vblex` - Verbs with infinitive -ar and various tenses
- Other function word paradigms (prepositions, determiners, etc.)

