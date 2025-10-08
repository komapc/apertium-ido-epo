# Ido-Esperanto Language Pair for Apertium

This is an Apertium language pair for translating between **Ido** and **Esperanto**.

## Data Source

This language pair was automatically generated from **Ido Wiktionary** ([io.wiktionary.org](https://io.wiktionary.org/)) data using extraction and conversion scripts.

- **Source:** Ido Wiktionary dump (io.wiktionary.org)
- **Extraction date:** October 2025
- **Extraction & conversion scripts:** [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)
- **Ido monolingual package:** [apertium-ido](https://github.com/komapc/apertium-ido)
- **Esperanto monolingual package:** [apertium-epo](https://github.com/apertium/apertium-epo) (existing)

## Requirements

You will need the following software installed:

* `lttoolbox` (>= 3.5.1)
* `apertium` (>= 3.6.1)
* `apertium-epo` - Esperanto monolingual package

## Compiling

```bash
make
make modes
```

## Usage

### Ido → Esperanto

```bash
$ echo "kato" | apertium -d . ido-epo
kato

$ echo "granda domo" | apertium -d . ido-epo
granda domo

$ echo "bona libro" | apertium -d . ido-epo
bona libro
```

### Esperanto → Ido

```bash
$ echo "kato" | bash modes/epo-ido.mode
kato

$ echo "domo" | bash modes/epo-ido.mode
domo

$ echo "bona" | bash modes/epo-ido.mode
bona
```

## Translation Pipeline

### Ido → Esperanto
1. **Morphological analysis** (Ido)
2. **Pretransfer**
3. **Bilingual dictionary lookup**
4. **Transfer** (adds Esperanto-specific tags)
5. **Generation** (Esperanto)

### Esperanto → Ido
1. **Morphological analysis** (Esperanto)
2. **Pretransfer**
3. **Bilingual dictionary lookup**
4. **Transfer** (removes gender, simplifies agreement)
5. **Generation** (Ido)

## Files

* `apertium-ido.ido.dix` - Ido morphological dictionary (6,748 entries)
* `apertium-ido-epo.ido-epo.dix` - Bilingual dictionary (6,467 entries)
* `apertium-ido-epo.ido-epo.t1x` - Ido→Esperanto transfer rules
* `apertium-ido-epo.epo-ido.t1x` - Esperanto→Ido transfer rules
* `modes.xml` - Translation modes
* `Makefile` - Build system

## Coverage

Since Ido and Esperanto are closely related constructed languages with similar grammar and much shared vocabulary, this language pair achieves excellent coverage:

- **Vocabulary overlap:** ~50-60% identical or cognate
- **Grammar similarity:** Very high (both agglutinative, SVO word order)
- **Translation quality:** Good for basic texts

## License

### Code and Dictionaries

This package is licensed under the **GNU General Public License v2.0**.

### Source Data Attribution

The dictionary entries were extracted from **Ido Wiktionary** ([io.wiktionary.org](https://io.wiktionary.org/)), which is licensed under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/) and the [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html).

**Attribution:**
- Original data: Ido Wiktionary contributors
- Extracted and processed by: Mark (komapc)
- Extraction tools: [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)
- Ido monolingual: [apertium-ido](https://github.com/komapc/apertium-ido)
- Esperanto monolingual: [apertium-epo](https://github.com/apertium/apertium-epo)

The transformation from Wiktionary format to Apertium bilingual dictionary format constitutes a substantial transformation and adaptation of the data, released here under GPL v2.0, compatible with the original CC-BY-SA and GFDL licenses.

## Generation Process

This language pair was created using the following automated process:

1. **Extract** Ido words with Esperanto translations from Ido Wiktionary XML dump
2. **Parse** morphological information (roots and suffixes)
3. **Convert** to Apertium monolingual dictionary format (Ido)
4. **Map** Ido roots to Esperanto lemmas in bilingual dictionary
5. **Generate** transfer rules for grammatical differences
6. **Compile** and test the complete translation pipeline

See the [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor) repository for the complete extraction and conversion scripts.

## Language Notes

### Ido Grammar
- **Nouns:** -o (singular), -i (plural), -n (accusative)
- **Adjectives:** -a (invariable)
- **Adverbs:** -e
- **Verbs:** -ar (infinitive), -as (present), -is (past), -os (future), -ez (imperative), -us (conditional)

### Esperanto Grammar
- **Nouns:** -o (singular), -oj (plural), -n (accusative)
- **Adjectives:** -a (with agreement: -aj for plural, -an/-ajn for accusative)
- **Adverbs:** -e
- **Verbs:** -i (infinitive), -as (present), -is (past), -os (future), -u (imperative/subjunctive)

### Key Differences Handled by Transfer Rules
- Esperanto adjectives agree in number and case → Ido adjectives are invariable
- Esperanto has grammatical gender on some nouns → Ido has no grammatical gender
- Verb infinitives: Ido -ar, Esperanto -i

## Contributing

Contributions are welcome! You can:

- Improve bilingual dictionary coverage
- Enhance transfer rules for better word order
- Add support for more complex grammatical constructions
- Report translation errors

## For More Information

* **Apertium:** [https://wiki.apertium.org/wiki/Apertium](https://wiki.apertium.org/wiki/Apertium)
* **Ido language:** [https://en.wikipedia.org/wiki/Ido](https://en.wikipedia.org/wiki/Ido)
* **Esperanto language:** [https://en.wikipedia.org/wiki/Esperanto](https://en.wikipedia.org/wiki/Esperanto)
* **Language pair HOWTO:** [https://wiki.apertium.org/wiki/Apertium_New_Language_Pair_HOWTO](https://wiki.apertium.org/wiki/Apertium_New_Language_Pair_HOWTO)

## Help and Support

* **Mailing list:** apertium-stuff@lists.sourceforge.net
* **IRC:** #apertium on irc.oftc.net
* **GitHub Issues:** [https://github.com/komapc/apertium-ido-epo/issues](https://github.com/komapc/apertium-ido-epo/issues)

## See Also

- [apertium-ido](https://github.com/komapc/apertium-ido) - Ido monolingual dictionary
- [apertium-epo](https://github.com/apertium/apertium-epo) - Esperanto monolingual dictionary
- [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor) - Extraction and conversion tools

