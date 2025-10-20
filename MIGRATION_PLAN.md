# Detailed Migration Plan - Vendor Repos First

**Status:** DRAFT - Ready for execution  
**Date:** October 20, 2025  
**Phase:** Vendor separation and submodule setup

## Phase 1: Vendor Repos Separation

### Step 1.1: Identify current vendor repos

Current vendor repositories at root:
- `/home/mark/apertium-dev/apertium/` - Core Apertium runtime
- `/home/mark/apertium-dev/lttoolbox/` - Lexical toolkit
- `/home/mark/apertium-dev/apertium-ido/` - Ido monolingual
- `/home/mark/apertium-dev/apertium-epo/` - Esperanto monolingual
- `/home/mark/apertium-dev/apertium-bel/` - Belarusian monolingual
- `/home/mark/apertium-dev/apertium-rus/` - Russian monolingual
- `/home/mark/apertium-dev/apertium-bel-rus/` - Belarusian-Russian pair
- `/home/mark/apertium-dev/apertium-fra/` - French monolingual

**Decision needed:** Are bel, rus, bel-rus, fra repos actively used or historical?

### Step 1.2: Create new directory structure

```bash
# Create the new apertium directory structure
mkdir -p /home/mark/apertium-dev/apertium/apertium-dev/vendor
mkdir -p /home/mark/apertium-dev/apertium/apertium-dev/build
mkdir -p /home/mark/apertium-dev/apertium/apertium-dev/tests
mkdir -p /home/mark/apertium-dev/apertium/apertium-dev/docs/{analyses,progress,guides}
mkdir -p /home/mark/apertium-dev/apertium/apertium-dev/data/{raw,processed}
```

### Step 1.3: Check Git remotes for vendor repos

Commands to verify submodule source URLs:
```bash
cd /home/mark/apertium-dev/apertium && git remote -v
cd /home/mark/apertium-dev/lttoolbox && git remote -v
cd /home/mark/apertium-dev/apertium-ido && git remote -v
cd /home/mark/apertium-dev/apertium-epo && git remote -v
```

Expected upstream URLs:
- `apertium`: https://github.com/apertium/apertium.git
- `lttoolbox`: https://github.com/apertium/lttoolbox.git
- `apertium-ido`: https://github.com/apertium/apertium-ido.git
- `apertium-epo`: https://github.com/apertium/apertium-epo.git

### Step 1.4: Convert to submodules

**Option A: Fresh submodule initialization (recommended)**
```bash
cd /home/mark/apertium-dev

# Remove old vendor directories (after backing up any local changes)
# WARNING: Check for uncommitted changes first!
git status apertium/
git status lttoolbox/
git status apertium-ido/
git status apertium-epo/

# If no local changes, remove:
rm -rf apertium lttoolbox apertium-ido apertium-epo

# Initialize as submodules in new location
cd apertium/apertium-dev
git submodule add https://github.com/apertium/apertium.git vendor/apertium
git submodule add https://github.com/apertium/lttoolbox.git vendor/lttoolbox
git submodule add https://github.com/apertium/apertium-ido.git vendor/apertium-ido
git submodule add https://github.com/apertium/apertium-epo.git vendor/apertium-epo

# Initialize and update submodules
git submodule update --init --recursive

# Pin to stable commits (example - adjust as needed)
cd vendor/apertium && git checkout stable && cd ../..
cd vendor/lttoolbox && git checkout stable && cd ../..
```

**Option B: Preserve git history by moving**
```bash
# If vendor repos have important local changes:
cd /home/mark/apertium-dev
mv apertium apertium/apertium-dev/vendor/
mv lttoolbox apertium/apertium-dev/vendor/
mv apertium-ido apertium/apertium-dev/vendor/
mv apertium-epo apertium/apertium-dev/vendor/

# Then convert to submodules in-place (more complex, ask if needed)
```

### Step 1.5: Submodule configuration

Create `.gitmodules` at `/home/mark/apertium-dev/.gitmodules`:
```
[submodule "apertium/apertium-dev/vendor/apertium"]
	path = apertium/apertium-dev/vendor/apertium
	url = https://github.com/apertium/apertium.git
	branch = stable
[submodule "apertium/apertium-dev/vendor/lttoolbox"]
	path = apertium/apertium-dev/vendor/lttoolbox
	url = https://github.com/apertium/lttoolbox.git
	branch = stable
[submodule "apertium/apertium-dev/vendor/apertium-ido"]
	path = apertium/apertium-dev/vendor/apertium-ido
	url = https://github.com/apertium/apertium-ido.git
	branch = master
[submodule "apertium/apertium-dev/vendor/apertium-epo"]
	path = apertium/apertium-dev/vendor/apertium-epo
	url = https://github.com/apertium/apertium-epo.git
	branch = master
```

### Step 1.6: Update build references

**Before:**
- Builds reference `../apertium/`, `../lttoolbox/`, etc.

**After:**
- Builds reference `vendor/apertium/`, `vendor/lttoolbox/`, etc.
- Or use environment variables (preferred)

**Environment variables approach:**
```bash
# In apertium/apertium-dev/Makefile or build scripts
VENDOR_DIR ?= $(CURDIR)/vendor
APERTIUM_DIR ?= $(VENDOR_DIR)/apertium
LTTOOLBOX_DIR ?= $(VENDOR_DIR)/lttoolbox
APERTIUM_IDO_DIR ?= $(VENDOR_DIR)/apertium-ido
APERTIUM_EPO_DIR ?= $(VENDOR_DIR)/apertium-epo

# Update PATH and LD_LIBRARY_PATH
export PATH := $(APERTIUM_DIR)/bin:$(LTTOOLBOX_DIR)/bin:$(PATH)
export PKG_CONFIG_PATH := $(APERTIUM_DIR)/lib/pkgconfig:$(LTTOOLBOX_DIR)/lib/pkgconfig:$(PKG_CONFIG_PATH)
```

### Step 1.7: Test builds with vendor submodules

```bash
cd /home/mark/apertium-dev/apertium/apertium-dev/vendor

# Build lttoolbox first (dependency)
cd lttoolbox
./autogen.sh
./configure --prefix=$(pwd)/installed
make
make install
cd ..

# Build apertium (depends on lttoolbox)
cd apertium
./autogen.sh
./configure --prefix=$(pwd)/installed --with-lttoolbox=$(pwd)/../lttoolbox/installed
make
make install
cd ..

# Verify tools are available
export PATH=$(pwd)/lttoolbox/installed/bin:$(pwd)/apertium/installed/bin:$PATH
which lt-comp
which apertium-preprocess-transfer
```

### Step 1.8: Handle other language repos

**Question for user:** What to do with these?
- `apertium-bel/` - Move to `apertium/apertium-dev/` or archive?
- `apertium-rus/` - Move to `apertium/apertium-dev/` or archive?
- `apertium-bel-rus/` - Move to `apertium/apertium-dev/` or archive?
- `apertium-fra/` - Move to `apertium/apertium-dev/` or archive?

**Recommendation:** If not actively used, move to `apertium/apertium-dev/archived/` or remove.

---

## Phase 2: Core Pair Move

### Step 2.1: Move apertium-ido-epo

```bash
cd /home/mark/apertium-dev
mv apertium-ido-epo apertium/apertium-dev/
```

### Step 2.2: Update Makefile paths

Inside `apertium/apertium-dev/apertium-ido-epo/`:
- Update any relative paths to vendor repos
- Update output paths to use `../build/` instead of local directory

### Step 2.3: Move duplicate dictionary files

Remove these from root (they're duplicates):
```bash
cd /home/mark/apertium-dev
rm -f apertium-ido.ido.dix
rm -f apertium-epo.epo.dix  # Note: check .gitignore, this is a symlink
rm -f apertium-ido-epo.ido-epo.dix
rm -f apertium-ido-epo.ido-epo.t1x
rm -f apertium-ido-epo.epo-ido.t1x
rm -f apertium-ido-epo.pc.in
rm -f apertium-ido-epo.post-*.dix
rm -f *.bin  # All compiled binaries
```

### Step 2.4: Update root Makefile

See section below for new root Makefile.

---

## Phase 3: Tools Move

### Step 3.1: Create tools structure

```bash
mkdir -p /home/mark/apertium-dev/tools/extractor
mkdir -p /home/mark/apertium-dev/tools/web
mkdir -p /home/mark/apertium-dev/tools/python
mkdir -p /home/mark/apertium-dev/tools/shell
```

### Step 3.2: Move extractor

```bash
cd /home/mark/apertium-dev
mv ido-esperanto-extractor tools/extractor/
```

Update paths in:
- `tools/extractor/ido-esperanto-extractor/scripts/*.py`
- Any hardcoded references to `../apertium-ido-epo/`

### Step 3.3: Move web app

```bash
cd /home/mark/apertium-dev
mv ido-epo-translator-web tools/web/
```

Update paths in:
- `tools/web/ido-epo-translator-web/.github/workflows/*.yml`
- `tools/web/ido-epo-translator-web/scripts/*.sh`
- `tools/web/ido-epo-translator-web/wrangler.toml`

### Step 3.4: Move shared scripts

```bash
cd /home/mark/apertium-dev

# Python utilities
mv analyze_five_articles.py tools/python/
mv analyze_ido_articles.py tools/python/
mv analyze_translations.py tools/python/
mv convert_to_paradigms.py tools/python/
mv date_normalizer.py tools/python/
mv detailed_error_analysis.py tools/python/
mv fetch_and_translate_wikipedia.py tools/python/
mv generate_numbers.py tools/python/
mv sort_dictionary.py tools/python/
mv translate_articles.py tools/python/
mv translate_specific_articles.py tools/python/

# Shell utilities
mv analyze_tests.sh tools/shell/
mv compare_results.sh tools/shell/
mv test_ala_paradigm.sh tools/shell/

# Move scripts/ dir contents
mv scripts/analyze_ido_monodix.py tools/python/
mv scripts/fix_ido_monodix_safe.py tools/python/
rm -rf scripts/  # if empty
```

---

## Phase 4: Tests Consolidation

### Step 4.1: Merge test directories

```bash
cd /home/mark/apertium-dev

# Move root test/ to apertium/apertium-dev/tests/
cp -r test/* apertium/apertium-dev/tests/
rm -rf test/

# Move root tests/ if it exists
if [ -d tests ]; then
    cp -r tests/* apertium/apertium-dev/tests/
    rm -rf tests/
fi

# Organize by language pair
cd apertium/apertium-dev/tests
mkdir -p ido-epo epo-ido
mv ido-epo-* ido-epo/
mv epo-ido-* epo-ido/
```

### Step 4.2: Remove duplicate tests from apertium-ido-epo

```bash
cd /home/mark/apertium-dev/apertium/apertium-dev/apertium-ido-epo
# Check if test/ exists and has duplicates
# If so, remove and point to ../tests/ instead
```

---

## Phase 5: Documentation Move

### Step 5.1: Move analysis files

```bash
cd /home/mark/apertium-dev
mv *_ANALYSIS.md apertium/apertium-dev/docs/analyses/
mv *_SUMMARY.md apertium/apertium-dev/docs/progress/
mv *_FIX*.md apertium/apertium-dev/docs/progress/
mv *_REPORT*.md apertium/apertium-dev/docs/analyses/
mv BEFORE_AFTER_COMPARISON.md apertium/apertium-dev/docs/analyses/
mv development_guide.md apertium/apertium-dev/docs/guides/
mv NEXT_STEPS_RECOMMENDATIONS.md apertium/apertium-dev/docs/progress/
mv PR_*.md apertium/apertium-dev/docs/progress/
```

### Step 5.2: Create index documents

Create `apertium/apertium-dev/docs/README.md` with links to all docs.

---

## Phase 6: Update .gitignore

```bash
cd /home/mark/apertium-dev
mv .gitignore.new .gitignore
```

---

## Phase 7: Update CI/CD

### GitHub Actions updates needed:
1. **Submodule initialization:**
   ```yaml
   - name: Checkout code
     uses: actions/checkout@v3
     with:
       submodules: recursive
   ```

2. **Path updates:**
   - Change references from `apertium-ido-epo/` to `apertium/apertium-dev/apertium-ido-epo/`
   - Update artifact paths

3. **Web deployment:**
   - Update paths in `tools/web/ido-epo-translator-web/.github/workflows/`

---

## Phase 8: Cleanup

### Step 8.1: Remove duplicates

```bash
cd /home/mark/apertium-dev/apertium/apertium-dev/apertium-ido-epo

# Remove duplicate analysis scripts
rm -f analyze_five_articles.py
rm -f analyze_ido_articles.py
rm -f analyze_translations.py
rm -f convert_to_paradigms.py
rm -f date_normalizer.py
rm -f detailed_error_analysis.py
rm -f fetch_and_translate_wikipedia.py
rm -f generate_numbers.py
rm -f sort_dictionary.py
rm -f translate_articles.py
rm -f translate_specific_articles.py
```

### Step 8.2: Remove stray files

```bash
cd /home/mark/apertium-dev
rm -f ", new)\nif pair_counts:\n    top=pair_counts.most_common(1)[0][0]\n    print(TOP_PAIR,top)\n    for lemma,o,n in entries:\n        if (o,n)==top:\n            print(*,lemma)\n            break\nPY"
```

### Step 8.3: Clean build artifacts

```bash
cd /home/mark/apertium-dev
rm -f *.bin
rm -rf autom4te.cache
rm -f config.log config.status
```

---

## Verification Steps

After each phase:
1. Test builds: `make -C apertium/apertium-dev`
2. Test tools: `make -C tools/extractor/ido-esperanto-extractor`
3. Test web: `cd tools/web/ido-epo-translator-web && npm install && npm run build`
4. Run tests: `make -C apertium/apertium-dev test`
5. Check git status: `git status` (should not show unintended changes)

---

## Rollback Plan

If anything breaks:
1. Stash changes: `git stash`
2. Reset to last known good state: `git reset --hard HEAD`
3. Review what went wrong
4. Adjust plan and retry

---

## Questions Before Proceeding

1. **Vendor repos:** Should I use Option A (fresh submodules) or Option B (preserve history)?
2. **Inactive language pairs:** Archive or keep apertium-bel, apertium-rus, apertium-bel-rus, apertium-fra?
3. **Root Makefile:** Should it delegate to all subprojects or just apertium-dev?
4. **Python environment:** Single requirements.txt at root or per-tool?
5. **Data directory:** Keep at `/home/mark/apertium-dev/data/` or move under `apertium/apertium-dev/data/`?

---

**Ready to execute Phase 1 (vendor separation) after user confirmation.**

