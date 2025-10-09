# Apertium Ido-Esperanto

Machine translation system for **Ido ↔ Esperanto** using the Apertium platform.

## Status

**Ido→Esperanto:** Functional (65-70% quality)  
**Esperanto→Ido:** Experimental (not recommended for production use)

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

- **Bilingual dictionary:** 7,795 entries
- **Ido monolingual:** 6,748 entries  
- **Transfer rules:** Complete for both directions
- **Test coverage:** 130 sentences

## Language Features

### Ido→Esperanto (Working)

✅ Accusative case on direct objects  
✅ Adjective agreement (number and case)  
✅ Copula distinction (nominative predicates)  
✅ Plural forms (-j, -jn)  
✅ Past/present tenses  
✅ Personal pronouns  
✅ Basic word order (SVO)

### Grammar Transformations

The system handles the main differences between Ido and Esperanto:

| Feature | Ido | Esperanto |
|---------|-----|-----------|
| Adjective agreement | Invariable | Agrees in number/case |
| Accusative case | None | -n on objects |
| Verb infinitive | -ar | -i |
| Plurals | -i | -j |

## Known Limitations

- Specialized vocabulary gaps (~200-300 terms)
- Object-first word order (OVS) not fully supported
- Esperanto→Ido direction has limited coverage

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
