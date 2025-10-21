# Apertium Development Workspace

This is a workspace directory containing multiple Apertium projects and tools.

## Projects

### Core Apertium Resources
- **[apertium/](apertium/)** - Apertium language resources
  - Language pairs (Ido-Esperanto, etc.)
  - Vendor dependencies (lttoolbox, apertium core)
  - Tests and documentation

### Tools
- **[tools/extractor/](tools/extractor/)** - Dictionary extraction pipeline
- **[tools/web/](tools/web/)** - Web translation interface (moved to [Vortaro](https://github.com/komapc/vortaro))
- **[tools/python/](tools/python/)** - Python utilities
- **[tools/shell/](tools/shell/)** - Shell scripts

## Quick Start

```bash
# Build Apertium language pairs
make core

# Run dictionary extractor
make extractor

# Build web translator
make web

# Run tests
make test

# Show all available commands
make help
```

## Structure

Each subdirectory is an independent project with its own README:
- See `apertium/README.md` for Apertium pair documentation
- See `tools/extractor/ido-esperanto-extractor/README.md` for extractor docs
- See [Vortaro](https://github.com/komapc/vortaro) for the web translator (moved to separate repository)

## Documentation

Planning and restructure documentation is in `docs/restructure/`.

