# Final Repository Structure

**Date:** October 20, 2025  
**Status:** ✅ COMPLETE - Absolute Minimal Root Achieved

## Philosophy

The root `apertium-dev/` is **NOT a git repository itself** - it's a **workspace container** that holds independent projects. Each subdirectory is self-contained with its own:
- Git repository
- README
- Build system
- Dependencies
- Documentation

## Root Structure (6 Items Only!)

```
/home/mark/apertium-dev/
├── apertium/              # Apertium language work
│   └── apertium-dev/      # Language pairs, vendor deps, tests, data
├── tools/                 # Supporting tools
│   ├── extractor/         # Dictionary extraction pipeline
│   ├── web/               # Web translation interface
│   ├── python/            # Python utilities
│   ├── shell/             # Shell scripts
│   └── venv/              # Shared Python environment
├── docs/                  # Workspace documentation
│   └── restructure/       # Restructure planning docs
├── Makefile               # Top-level orchestrator
├── apertium-ido-epo       # Symlink (compatibility)
└── README.md              # Workspace overview
```

## What Lives Where

### `apertium/apertium-dev/` - Apertium Language Work
**Purpose:** All Apertium linguistic resources
**Contains:**
- `vendor/` - Vendor submodules (lttoolbox, apertium, apertium-ido, apertium-epo)
- `apertium-ido-epo/` - Main Ido-Esperanto pair
- `archived/` - Inactive language repos (bel, rus, bel-rus, fra)
- `tests/` - All language pair tests
- `docs/` - Linguistic documentation
- `data/` - Corpora, Wikipedia extracts
- `outputs/` - Analysis outputs
- `build/` - Compiled binaries (gitignored)
- `bilingual_embedding/` - Embedding data
- Project metadata: AUTHORS, CONTRIBUTING, COPYING, ChangeLog, NEWS, goal.md

**Git repo:** Yes - this is the main `apertium-ido-epo` repository

### `tools/` - Supporting Tools
**Purpose:** Tools that support Apertium development
**Contains:**
- `extractor/ido-esperanto-extractor/` - Dictionary extraction from Wiktionary
- `web/ido-epo-translator-web/` - Web-based translation interface
- `python/` - 14 Python utility scripts
- `shell/` - 3 shell utility scripts
- `venv/` - Shared Python virtual environment

**Git repos:** Each tool has its own git repository

### `docs/` - Workspace Documentation
**Purpose:** Documentation about the workspace itself (not linguistic docs)
**Contains:**
- `restructure/` - Planning docs for this restructure
  - STRUCTURE.md
  - MIGRATION_PLAN.md
  - CI_CD_UPDATE_PLAN.md
  - etc.
- `ROOT_README.md` - Original root README (archived)
- `FINAL_STRUCTURE.md` - This file

### Root Files

**`Makefile`** - Top-level orchestrator
- `make core` - Build Apertium pairs
- `make extractor` - Run dictionary extraction
- `make web` - Build web interface
- `make test` - Run all tests
- `make help` - Show all commands

**`README.md`** - Minimal workspace overview
- Points to each subproject's README
- Shows basic usage

**`apertium-ido-epo`** - Symlink for compatibility
- Points to `apertium/apertium-dev/apertium-ido-epo/`
- Temporary during transition
- Remove after CI/CD is updated

## Key Principles

### 1. Independence
Each subdirectory is a complete, independent project:
- Can be cloned separately
- Has its own build system
- Manages its own dependencies
- Contains its own documentation

### 2. No Root Git Repo
The root is just a container. The `.git` directory at root belongs to `apertium-ido-epo`, which has been restructured but maintains its git history.

### 3. Clear Boundaries
- **Linguistic work** → `apertium/`
- **Tools** → `tools/`
- **Workspace docs** → `docs/`

### 4. Minimal Root
Only 6 items at root:
- 2 directories (apertium, tools)
- 1 docs directory
- 1 orchestrator (Makefile)
- 1 overview (README.md)
- 1 compatibility symlink (temporary)

## Comparison

### Before Restructure (Oct 10, 2025)
```
150+ items at root including:
- Scattered dictionaries and transfer files
- 100+ duplicate files
- Scripts everywhere
- Tests in 3 locations
- 40+ doc files mixed with code
- Build artifacts in git
- Vendor repos as loose directories
```

### After Restructure (Oct 20, 2025)
```
6 items at root:
- apertium/ (organized Apertium work)
- tools/ (organized tools)
- docs/ (workspace docs)
- Makefile (orchestrator)
- README.md (overview)
- apertium-ido-epo (symlink)

89% reduction in root clutter
All projects self-contained
Clean separation of concerns
```

## Benefits

✅ **Clarity** - Obvious where everything lives  
✅ **Independence** - Each project is self-contained  
✅ **Scalability** - Easy to add new language pairs or tools  
✅ **Clean git diffs** - No build artifacts, no duplicates  
✅ **Easy CI/CD** - Clear paths, submodule support  
✅ **Maintainability** - Logical organization  
✅ **Minimal root** - Just a workspace container  

## Usage

### Build Everything
```bash
cd /home/mark/apertium-dev
make help        # Show all commands
make core        # Build Apertium pairs
make test        # Run tests
```

### Work on Specific Projects
```bash
# Work on language pair
cd apertium/apertium-dev/apertium-ido-epo
make
make test

# Run extractor
cd tools/extractor/ido-esperanto-extractor
make

# Develop web app
cd tools/web/ido-epo-translator-web
npm install
npm run dev
```

### Use Utilities
```bash
# Python tools
cd tools/python
python analyze_translations.py

# With shared venv
source tools/venv/bin/activate
python tools/python/analyze_translations.py
```

## Future Considerations

### Fully Independent Projects?
If you want to make each project completely independent:
1. Remove the top-level git repo
2. Each subdirectory becomes its own workspace
3. Remove the orchestrating Makefile
4. Clone projects individually as needed

### Monorepo Alternative
Current structure is a hybrid - mainly organized workspace with git at the pair level. Could also:
1. Make root a true monorepo (single git for all)
2. Use git submodules for everything
3. Use workspace tools (npm workspaces, etc.)

## Conclusion

This structure balances:
- **Organization** - Clear, logical layout
- **Independence** - Self-contained projects
- **Convenience** - Orchestrator for common tasks
- **Minimalism** - Only 6 items at root

The workspace is now a **clean, professional container** for Apertium development work.

