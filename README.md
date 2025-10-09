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
- **-ala paradigm:** 20 common adjectives with morphological inflection

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
✅ -ala adjective paradigm (20 adjectives)

### Esperanto→Ido (Functional)

✅ Constraint Grammar disambiguation (7 rules)  
✅ Superlative structures (plej → maxim)  
✅ Partitive expressions (da → di)  
✅ Determiner handling (la)  
✅ Pronoun disambiguation (oni)  
✅ Verb tense conversion  
✅ Number pass-through (1-1000 + decimals)

### Grammar Transformations

The system handles the main differences between Ido and Esperanto:

| Feature | Ido | Esperanto |
|---------|-----|-----------|
| Adjective agreement | Invariable | Agrees in number/case |
| Accusative case | None | -n on objects |
| Verb infinitive | -ar | -i |
| Plurals | -i | -j |

## Known Limitations & Ongoing Work

### Ido→Esperanto
- Some verb forms show `@` (invariable form conflicts) - ~10-15 cases
- Missing specialized vocabulary (~100-200 terms)
- Some -ala adjectives not yet analyzed (debugging in progress)

### Esperanto→Ido  
- Object-first word order (OVS) not fully supported
- Some multiword units need expansion
- Passive voice constructions need refinement

### Active Development Areas
- Expanding test coverage with real Wikipedia articles
- Adding more -ala adjective roots
- Improving generator for edge cases
- Multiword expression handling

## Data Sources

Dictionary entries extracted from:
- [Ido Wiktionary](https://io.wiktionary.org/)
- Manual additions for function words and proper nouns
- Extraction tools: [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

For questions or discussion:
- Mailing list: [apertium-stuff@lists.sourceforge.net](mailto:apertium-stuff@lists.sourceforge.net)
- IRC: #apertium on irc.oftc.net
- Wiki: https://wiki.apertium.org/

## License

GPL v2.0

Dictionary data from Ido Wiktionary (CC-BY-SA 3.0 / GFDL).

## Authors

- Mark (komapc) - Initial development and data extraction
