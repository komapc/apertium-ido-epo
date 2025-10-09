# Ido-Esperanto Language Pair for Apertium

An Apertium language pair for translating between **Ido** and **Esperanto**.

## Data Source

Dictionary entries were extracted from **Ido Wiktionary** ([io.wiktionary.org](https://io.wiktionary.org/)) and supplemented with manually added entries for function words, proper nouns, ordinals, and common compounds.

- **Extraction scripts:** [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)
- **Esperanto package:** [apertium-epo](https://github.com/apertium/apertium-epo)

## Requirements

* `lttoolbox` >= 3.5.1
* `apertium` >= 3.6.1
* `apertium-ido` >= 0.1.0
* `apertium-epo` >= 0.1.0

## Installation

### From Source

```bash
./autogen.sh
./configure
make
sudo make install
```

### Development Build

For testing without installation:

```bash
./autogen.sh
./configure
make
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

For development (without installation):

```bash
# Ido → Esperanto
echo "me havas granda kato" | apertium -d . ido-epo

# Esperanto → Ido
echo "mi havas grandan katon" | apertium -d . epo-ido
```

## Files

* `apertium-ido.ido.dix` - Ido morphological dictionary
* `apertium-ido-epo.ido-epo.dix` - Bilingual dictionary
* `apertium-ido-epo.ido-epo.t1x` - Ido→Esperanto transfer rules
* `apertium-ido-epo.epo-ido.t1x` - Esperanto→Ido transfer rules

## Key Differences

Transfer rules handle the main grammatical differences between Ido and Esperanto:
- Adjective agreement (Ido: invariable → Esperanto: agrees in number and case)
- Accusative case on direct objects
- Verb infinitives (Ido: -ar → Esperanto: -i)

## Testing

Run the regression tests:

```bash
make test
```

This will run all test cases defined in `test/tests.json` using `apertium-regtest`.

## Statistics

* **Bilingual dictionary entries:** 7,335
* **Transfer rules:** Complete coverage for both directions
* **Test cases:** 40+ sentences covering basic and grammar features

## Coverage

The language pair handles:
- Basic vocabulary (nouns, verbs, adjectives, adverbs)
- Adjective agreement (Ido invariable → Esperanto number/case agreement)
- Accusative case marking on direct objects
- Verb infinitives (Ido `-ar` → Esperanto `-i`)
- Personal pronouns and demonstratives
- Prepositions and conjunctions
- Numerals and ordinals

## Contributing

Contributions are welcome! This language pair is part of the Apertium project.

To contribute:
1. Test the language pair and identify errors
2. Add new dictionary entries or improve transfer rules
3. Submit issues or pull requests to the repository

For questions or discussion:
- Mailing list: [apertium-stuff@lists.sourceforge.net](mailto:apertium-stuff@lists.sourceforge.net)
- IRC: #apertium on irc.oftc.net
- Wiki: https://wiki.apertium.org/

## License

GPL v2.0. Dictionary data extracted from Ido Wiktionary (CC-BY-SA 3.0 / GFDL).

