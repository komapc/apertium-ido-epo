# Contributing to Apertium-ido-epo

Thank you for your interest in contributing to the Ido-Esperanto language pair!

## How to Contribute

### Reporting Bugs

If you find translation errors or bugs:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/apertium/apertium-ido-epo/issues)
2. If not, create a new issue with:
   - Example input text (in Ido or Esperanto)
   - Actual output
   - Expected output
   - Which direction (ido-epo or epo-ido)

### Improving Translations

To improve dictionary entries or transfer rules:

1. Fork the repository
2. Make your changes:
   - **Dictionary entries:** Edit `apertium-ido-epo.ido-epo.dix`
   - **Transfer rules:** Edit `apertium-ido-epo.ido-epo.t1x` or `apertium-ido-epo.epo-ido.t1x`
3. Test your changes:
   ```bash
   make
   echo "test sentence" | apertium -d . ido-epo
   ```
4. Add test cases in `test/` directory
5. Submit a pull request

### Adding New Words

When adding new dictionary entries:

```xml
<e><p><l>idoword<s n="n" /></l><r>esperantoword<s n="n" /></r></p></e>
```

Common part-of-speech tags:
- `<s n="n" />` - noun
- `<s n="vblex" />` - verb
- `<s n="adj" />` - adjective
- `<s n="adv" />` - adverb
- `<s n="pr" />` - preposition

### Testing

Before submitting:

```bash
# Build
make clean && make

# Test both directions
echo "me havas granda kato" | apertium -d . ido-epo
echo "mi havas grandan katon" | apertium -d . epo-ido

# Run regression tests
make test
```

### Coding Standards

- Use UTF-8 encoding
- Follow XML formatting in existing files
- Add comments for complex transfer rules
- Keep entries alphabetically sorted (when practical)
- Validate XML before committing

### Pull Request Process

1. Update test cases if needed
2. Ensure all tests pass
3. Update documentation if you're changing functionality
4. Write clear commit messages
5. Reference any related issues

### Key Differences Between Ido and Esperanto

When writing transfer rules, remember:

**Adjectives:**
- Ido: invariable (`granda kato`, `granda kati`)
- Esperanto: agrees in number and case (`grandan katon`, `grandajn katojn`)

**Accusative:**
- Ido: only on pronouns
- Esperanto: on direct objects (`-n`)

**Infinitives:**
- Ido: `-ar` (irar, manjar)
- Esperanto: `-i` (iri, manĝi)

## Getting Help

- **Mailing list:** [apertium-stuff@lists.sourceforge.net](mailto:apertium-stuff@lists.sourceforge.net)
- **IRC:** #apertium on irc.oftc.net
- **Wiki:** https://wiki.apertium.org/wiki/Apertium-ido-epo

## Code of Conduct

Be respectful, constructive, and collaborative. We welcome contributors of all skill levels!

## License

By contributing, you agree that your contributions will be licensed under GPL v2.0.

