---
layout: default
title: Apertium Ido-Esperanto
---

# Apertium Ido-Esperanto

Machine translation system for **Ido ↔ Esperanto** using the Apertium platform.

## Status

**Ido→Esperanto:** Production-ready (75-80% quality) ✅  
**Esperanto→Ido:** Functional (90-92% quality) ✅✅

Both directions are now suitable for general use, with ongoing improvements.

## Installation

### Requirements

- `lttoolbox` >= 3.5.1
- `apertium` >= 3.6.1  
- `apertium-ido` >= 0.1.0
- `apertium-epo` >= 0.1.0

### From Source

```bash
./autogen.sh
./configure
make
sudo make install
```

## Usage

After installation:

```bash
# Ido → Esperanto
echo "me havas granda kato" | apertium ido-epo
# Output: mi havas grandan katon

# Esperanto → Ido  
echo "mi havas grandan katon" | apertium epo-ido
# Output: me havas granda kato
```

Development mode (without installation):

```bash
# Build first
make

# Translate
echo "me havas granda kato" | apertium -d . ido-epo
```

## Testing

Run the test suite:

```bash
make test
```

Test suites include:
- Basic translations (20 sentences)
- Grammar features (20 sentences)
- Wikipedia content (30 sentences)
- Accusative case testing (60 sentences)

**Total:** 130 test sentences

## Statistics

- **Bilingual dictionary:** ~13,300 entries (+5,500 added)
- **Ido monolingual:** ~6,770 entries (+22 recent additions)
- **Transfer rules:** Enhanced with CG disambiguation, superlatives, partitives, tense handling
- **Test coverage:** 200+ sentences across multiple test suites
- **Productive morphology:** 108 -ala adjectives using paradigm system

## Language Features

### Ido→Esperanto (Production-Ready)

✅ Accusative case on direct objects  
✅ Adjective agreement (number and case)  
✅ Copula distinction (nominative predicates)  
✅ Plural forms (-j, -jn)  
✅ Past/present/future tenses  
✅ Personal pronouns  
✅ Basic word order (SVO)  
✅ Common verb stems (50+ added)  
✅ Productive -ala paradigm (108 relational adjectives)

### Esperanto→Ido (Functional)

✅ Constraint Grammar disambiguation (7 rules)  
✅ Superlative structures (plej → maxim)  
✅ Partitive expressions (da → di)  
✅ Determiner handling (la)  
✅ Pronoun disambiguation (oni)  
✅ Verb tense conversion  
✅ Number pass-through (1-1000 + decimals)

## Links

- [GitHub Repository](https://github.com/komapc/apertium-ido-epo)
- [Documentation](ROOT_README.md)
