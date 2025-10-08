# Ido-Esperanto Language Pair for Apertium

An Apertium language pair for translating between **Ido** and **Esperanto**.

## Data Source

Dictionary entries were extracted from **Ido Wiktionary** ([io.wiktionary.org](https://io.wiktionary.org/)) and supplemented with manually added entries for function words, proper nouns, ordinals, and common compounds.

- **Extraction scripts:** [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)
- **Esperanto package:** [apertium-epo](https://github.com/apertium/apertium-epo)

## Requirements

* `lttoolbox`
* `apertium`
* `apertium-epo`

## Compiling

```bash
make
make modes
```

## Usage

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

## License

GPL v2.0. Dictionary data extracted from Ido Wiktionary (CC-BY-SA 3.0 / GFDL).

