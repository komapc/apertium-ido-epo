# Repository Structure Plan

**Version:** 1.0  
**Date:** October 20, 2025  
**Status:** DRAFT - Not yet implemented

## Overview

This document describes the planned restructuring of the apertium-dev repository to achieve:
- Clear separation of Apertium language resources, tools, and vendor dependencies
- Consistent build artifact locations
- Elimination of duplicates and scattered scripts
- Better git hygiene and CI/CD paths

## Target Directory Layout

```
/home/mark/apertium-dev/
├── apertium/                           # All Apertium language resources
│   └── apertium-dev/                   # Main development tree
│       ├── vendor/                     # Upstream Apertium dependencies (submodules)
│       │   ├── apertium/              # Core Apertium runtime (submodule)
│       │   ├── lttoolbox/             # Lexical toolkit (submodule)
│       │   ├── apertium-ido/          # Ido monolingual (submodule)
│       │   └── apertium-epo/          # Esperanto monolingual (submodule)
│       ├── apertium-ido-epo/          # Ido-Esperanto pair (main project)
│       │   ├── apertium-ido.ido.dix
│       │   ├── apertium-epo.epo.dix
│       │   ├── apertium-ido-epo.ido-epo.dix
│       │   ├── apertium-ido-epo.ido-epo.t1x
│       │   ├── apertium-ido-epo.epo-ido.t1x
│       │   ├── modes.xml
│       │   ├── scripts/               # Pair-specific scripts
│       │   └── ...
│       ├── apertium-bel/              # Belarusian mono (existing)
│       ├── apertium-rus/              # Russian mono (existing)
│       ├── apertium-bel-rus/          # Belarusian-Russian pair (existing)
│       ├── apertium-fra/              # French mono (existing)
│       ├── tests/                     # Consolidated test suite
│       │   ├── ido-epo/
│       │   │   ├── basic-input.txt
│       │   │   ├── grammar-input.txt
│       │   │   └── ...
│       │   ├── epo-ido/
│       │   └── README.md
│       ├── build/                     # All build artifacts (gitignored)
│       │   ├── ido-epo.autobil.bin
│       │   ├── ido-epo.automorf.bin
│       │   └── ...
│       ├── data/                      # Corpora and test data
│       │   ├── raw/                   # Original Wikipedia articles, etc.
│       │   └── processed/             # Analyzed/normalized data
│       ├── docs/                      # Project documentation and analyses
│       │   ├── analyses/              # Translation analyses, reports
│       │   ├── progress/              # PR summaries, session notes
│       │   └── guides/                # Development guides
│       ├── Makefile                   # Orchestrator for all pairs
│       ├── README.md
│       └── .gitignore
├── tools/                             # Supporting tools and utilities
│   ├── extractor/
│   │   └── ido-esperanto-extractor/   # Dictionary extraction pipeline
│   │       ├── scripts/
│   │       ├── work/
│   │       ├── reports/
│   │       ├── build/                 # Extractor build artifacts
│   │       └── ...
│   ├── web/
│   │   └── ido-epo-translator-web/    # Web translation UI
│   │       ├── src/
│   │       ├── dist/                  # Web build artifacts
│   │       ├── scripts/
│   │       └── ...
│   ├── python/                        # Shared Python utilities
│   │   ├── analyze_translations.py
│   │   ├── analyze_ido_articles.py
│   │   ├── fetch_and_translate_wikipedia.py
│   │   ├── sort_dictionary.py
│   │   ├── date_normalizer.py
│   │   └── ...
│   └── shell/                         # Shared shell scripts
│       ├── analyze_tests.sh
│       └── compare_results.sh
├── outputs/                           # Analysis outputs (optional, can be gitignored)
├── venv/                              # Python virtual environment
├── Makefile                           # Top-level orchestrator
├── README.md                          # Project overview
└── .gitignore                         # Global ignore rules
```

## Key Principles

### 1. Vendor Dependencies
- All upstream Apertium repos under `apertium/apertium-dev/vendor/`
- Managed as Git submodules pinned to stable commits
- Never duplicate vendor files into first-party projects

### 2. Build Artifacts
- Apertium pair builds go to `apertium/apertium-dev/build/`
- Extractor builds go to `tools/extractor/ido-esperanto-extractor/build/`
- Web builds go to `tools/web/ido-epo-translator-web/dist/`
- All build directories are gitignored

### 3. Scripts
- **Pair-specific scripts** stay in `apertium/apertium-dev/apertium-ido-epo/scripts/`
- **Shared analysis/utility scripts** go to `tools/python/` or `tools/shell/`
- **Tool-specific scripts** stay within their tool directories (e.g., extractor scripts, web scripts)
- No loose scripts at repository root

### 4. Tests
- Consolidated under `apertium/apertium-dev/tests/`
- Organized by language pair: `tests/ido-epo/`, `tests/epo-ido/`
- Root Makefile provides `make test` target that runs all tests

### 5. Documentation
- Project docs and analyses under `apertium/apertium-dev/docs/`
- Organized by type: `docs/analyses/`, `docs/progress/`, `docs/guides/`
- Each subproject keeps its own README

## Script Inventory and Destinations

### Root-level Python scripts → `tools/python/`
- `analyze_five_articles.py` - Analysis utility
- `analyze_ido_articles.py` - Analysis utility
- `analyze_translations.py` - Analysis utility
- `convert_to_paradigms.py` - Dictionary utility
- `date_normalizer.py` - Normalization utility
- `detailed_error_analysis.py` - Analysis utility
- `fetch_and_translate_wikipedia.py` - Testing utility
- `generate_numbers.py` - Testing utility
- `sort_dictionary.py` - Dictionary utility
- `translate_articles.py` - Testing utility
- `translate_specific_articles.py` - Testing utility

### Root-level shell scripts → `tools/shell/`
- `analyze_tests.sh` - Test analysis
- `compare_results.sh` - Test comparison
- `test_ala_paradigm.sh` - Specific test

### Scripts already in subdirectories (keep where they are)
- `scripts/analyze_ido_monodix.py` → move to `tools/python/`
- `scripts/fix_ido_monodix_safe.py` → move to `tools/python/`
- `scripts/build_ido_wiki_lexicon.py` → duplicate, keep one in pair scripts
- Extractor scripts stay in `tools/extractor/ido-esperanto-extractor/scripts/`
- Web scripts stay in `tools/web/ido-epo-translator-web/scripts/`

### Duplicate analysis scripts in apertium-ido-epo/
These are duplicates of root scripts; after consolidation, remove from apertium-ido-epo:
- `apertium-ido-epo/analyze_five_articles.py`
- `apertium-ido-epo/analyze_ido_articles.py`
- `apertium-ido-epo/analyze_translations.py`
- `apertium-ido-epo/convert_to_paradigms.py`
- `apertium-ido-epo/date_normalizer.py`
- `apertium-ido-epo/detailed_error_analysis.py`
- `apertium-ido-epo/fetch_and_translate_wikipedia.py`
- `apertium-ido-epo/generate_numbers.py`
- `apertium-ido-epo/sort_dictionary.py`
- `apertium-ido-epo/translate_articles.py`
- `apertium-ido-epo/translate_specific_articles.py`

## Duplicates to Remove

### Dictionary and transfer files at root
These exist both at root and inside `apertium-ido-epo/`:
- `apertium-ido.ido.dix` (root) → keep only in `apertium/apertium-dev/apertium-ido-epo/`
- `apertium-epo.epo.dix` (root) → keep only in `apertium/apertium-dev/apertium-ido-epo/`
- `apertium-ido-epo.ido-epo.dix` (root) → keep only in `apertium/apertium-dev/apertium-ido-epo/`
- `apertium-ido-epo.ido-epo.t1x` (root) → keep only in `apertium/apertium-dev/apertium-ido-epo/`
- `apertium-ido-epo.epo-ido.t1x` (root) → keep only in `apertium/apertium-dev/apertium-ido-epo/`
- All `.bin` files at root → these should be in `build/` directory

### Test files at root
- `test/` directory at root → move contents to `apertium/apertium-dev/tests/`
- `tests/` directory at root → merge with above

### Documentation files at root
Move to `apertium/apertium-dev/docs/`:
- All `*_ANALYSIS.md`, `*_SUMMARY.md`, `*_FIX*.md` files
- `BEFORE_AFTER_COMPARISON.md`
- `development_guide.md`
- Progress tracking files

## Makefile Strategy

### Top-level `/home/mark/apertium-dev/Makefile`
Orchestrates all subprojects:
```makefile
# Project paths
APERTIUM_DEV = apertium/apertium-dev
EXTRACTOR = tools/extractor/ido-esperanto-extractor
WEB = tools/web/ido-epo-translator-web

.PHONY: all core extractor web test clean

all: core

core:
	$(MAKE) -C $(APERTIUM_DEV)

extractor:
	$(MAKE) -C $(EXTRACTOR)

web:
	cd $(WEB) && npm run build

test:
	$(MAKE) -C $(APERTIUM_DEV) test

clean:
	$(MAKE) -C $(APERTIUM_DEV) clean
	$(MAKE) -C $(EXTRACTOR) clean
	cd $(WEB) && npm run clean
```

### `/home/mark/apertium-dev/apertium/apertium-dev/Makefile`
Enhanced version of current Makefile with:
- `BUILD_DIR = build/` prefix for all artifacts
- Environment variables for vendor paths
- Targets for all language pairs
- Centralized test runner

## Git Hygiene

### .gitignore additions
```gitignore
# Build artifacts
build/**
**/build/**
**/*.bin
**/*.att.gz
**/*.mode
**/autom4te.cache/**
**/config.log
**/config.status

# Python
**/__pycache__/**
**/*.pyc
venv/
**/.pytest_cache/

# Node
**/node_modules/**
**/dist/**

# Workspace
outputs/
**/.deps/
**/modes/

# Temporary files
*~
*.bak
*.backup
*.tmp
```

### Submodule configuration
Initialize vendor repos as submodules:
```bash
cd apertium/apertium-dev
git submodule add https://github.com/apertium/apertium.git vendor/apertium
git submodule add https://github.com/apertium/lttoolbox.git vendor/lttoolbox
git submodule add https://github.com/apertium/apertium-ido.git vendor/apertium-ido
git submodule add https://github.com/apertium/apertium-epo.git vendor/apertium-epo
```

## Migration Plan

### Phase 1: Foundation (No file moves)
1. Create `apertium/apertium-dev/` directory structure
2. Add/update `.gitignore`
3. Create `STRUCTURE.md` (this document)
4. Update root `Makefile` with new path variables (but keep working with old paths)

### Phase 2: Vendor separation
1. Initialize submodules under `apertium/apertium-dev/vendor/`
2. Update pair build scripts to reference vendor paths
3. Test builds work with new vendor layout
4. Remove old vendor copies after verification

### Phase 3: Core move
1. Move `apertium-ido-epo/` to `apertium/apertium-dev/`
2. Move other language repos to `apertium/apertium-dev/`
3. Update Makefiles and paths
4. Test builds

### Phase 4: Tools move
1. Move `ido-esperanto-extractor/` to `tools/extractor/`
2. Move `ido-epo-translator-web/` to `tools/web/`
3. Update scripts and paths

### Phase 5: Scripts consolidation
1. Create `tools/python/` and `tools/shell/`
2. Move shared scripts from root
3. Remove duplicates from `apertium-ido-epo/`
4. Update import paths and shebangs

### Phase 6: Tests consolidation
1. Create `apertium/apertium-dev/tests/` structure
2. Move test files from root `test/` and `tests/`
3. Update test runner and Makefile

### Phase 7: Documentation
1. Create `apertium/apertium-dev/docs/` structure
2. Move analysis and progress files
3. Update cross-references

### Phase 8: Cleanup
1. Remove empty directories
2. Remove duplicate files
3. Remove build artifacts from source control
4. Update CI/CD paths
5. Remove temporary symlinks

## Temporary Compatibility

During migration, use symlinks to avoid breaking existing workflows:
```bash
# At root, link to new locations
ln -s apertium/apertium-dev/apertium-ido-epo/apertium-ido.ido.dix .
ln -s apertium/apertium-dev/build/*.bin .
```

Remove symlinks after all scripts and CI are updated to new paths.

## CI/CD Updates Required

1. Update GitHub Actions workflows to:
   - Initialize submodules: `git submodule update --init --recursive`
   - Use new paths for builds and tests
   - Update artifact paths
2. Update deployment scripts in web app
3. Update webhook paths on EC2

## Verification Checklist

After migration:
- [ ] `make core` builds successfully
- [ ] `make test` passes all tests
- [ ] `make extractor` runs pipeline
- [ ] `make web` builds web app
- [ ] All scripts run from new locations
- [ ] CI/CD pipelines pass
- [ ] Documentation is accurate
- [ ] No duplicate files remain
- [ ] Build artifacts are gitignored
- [ ] Submodules are properly initialized

## Questions for User

1. Should `outputs/` directory be gitignored or kept in version control?
2. Should we keep `data/` at top level or move under `apertium/apertium-dev/data/`?
3. Any specific scripts that should stay at root for convenience?
4. Preferred approach for Python dependencies: single root `requirements.txt` or per-tool?

---
**Next Steps:** Review this structure plan, then proceed with Phase 1 implementation.

