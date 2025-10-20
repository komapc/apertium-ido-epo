# Restructure Execution Plan

**Date:** October 20, 2025  
**Approach:** Option 3 - Vendor-first (phased, safest)  
**Branch:** Will use current feature branch or create new one

## Decisions Made (Using Recommendations)

### Migration Strategy
- ✅ **Vendor repos:** Fresh submodules (Option A)
- ✅ **Inactive language pairs:** Move bel/rus/bel-rus/fra to `apertium/archived/`
- ✅ **Root Makefile scope:** Delegate to all subprojects (core, extractor, web)
- ✅ **Python dependencies:** Per-tool (not centralized)
- ✅ **Data directory:** Keep at root level

### CI/CD Preferences
- ✅ **Old workflow files:** Delete after successful migration
- ✅ **CI caching:** Yes, cache vendor builds
- ✅ **Extractor schedule:** Manual only (no automatic weekly runs)
- ✅ **Build notifications:** Use GitHub built-in notifications

### Execution Approach
- ✅ **Option 3 selected:** Vendor-first approach
  - Start with vendor separation only
  - Test thoroughly
  - Proceed with rest only after verification

---

## Phase 1: Vendor Separation (Starting Now)

### Current Status
- On branch: `feature/extractor-regeneration-pipeline`
- Uncommitted changes exist
- Need to decide: commit current work first or stash?

### Steps for Phase 1

#### 1.1 Create directory structure
```bash
mkdir -p apertium/vendor
mkdir -p apertium/build
mkdir -p apertium/tests
mkdir -p apertium/docs/{analyses,progress,guides}
mkdir -p apertium/data/{raw,processed}
```

#### 1.2 Check vendor repo remotes
```bash
cd apertium && git remote -v
cd ../lttoolbox && git remote -v
cd ../apertium-ido && git remote -v
cd ../apertium-epo && git remote -v
```

#### 1.3 Remove old vendor directories (after confirming no local changes)
```bash
# Check for uncommitted changes in each
cd /home/mark/apertium-ido-epo
git status apertium/ lttoolbox/ apertium-ido/ apertium-epo/

# If clean, remove them
rm -rf apertium lttoolbox apertium-ido apertium-epo
```

#### 1.4 Initialize vendor submodules
```bash
cd /home/mark/apertium-ido-epo/apertium/apertium-dev

# Add submodules
git submodule add https://github.com/apertium/apertium.git vendor/apertium
git submodule add https://github.com/apertium/lttoolbox.git vendor/lttoolbox
git submodule add https://github.com/apertium/apertium-ido.git vendor/apertium-ido
git submodule add https://github.com/apertium/apertium-epo.git vendor/apertium-epo

# Initialize and update
git submodule update --init --recursive
```

#### 1.5 Install Makefile.apertium-dev
```bash
cp /home/mark/apertium-ido-epo/Makefile.apertium-dev /home/mark/apertium-ido-epo/apertium/Makefile
```

#### 1.6 Test vendor build
```bash
cd /home/mark/apertium-ido-epo/apertium/apertium-dev
make vendor
```

#### 1.7 Verification
- [ ] Submodules present in `vendor/`
- [ ] `vendor/installed/` created with binaries
- [ ] `lt-comp` works from `vendor/installed/bin/`
- [ ] `apertium-preprocess-transfer` works

---

## Phase 2: Core Pair Move (After Phase 1 Success)

Will execute only after Phase 1 is verified working.

#### 2.1 Move apertium-ido-epo
```bash
mv /home/mark/apertium-ido-epo/apertium-ido-epo /home/mark/apertium-ido-epo/apertium/
```

#### 2.2 Update pair Makefile to use vendor
- Update paths to reference `../vendor/installed/bin/`
- Set BUILD_DIR to `../build/`

#### 2.3 Test pair build
```bash
cd /home/mark/apertium-ido-epo/apertium/apertium-dev
make pair
```

#### 2.4 Create temporary symlink for compatibility
```bash
cd /home/mark/apertium-ido-epo
ln -s apertium/apertium-ido-epo apertium-ido-epo
```

---

## Phase 3: Tools Move (After Phase 2 Success)

#### 3.1 Create tools structure
```bash
mkdir -p /home/mark/apertium-ido-epo/tools/{extractor,web,python,shell}
```

#### 3.2 Move projects
```bash
mv ido-esperanto-extractor tools/extractor/
mv ido-epo-translator-web tools/web/
```

#### 3.3 Move scripts
```bash
# Move Python utilities
mv analyze_*.py tools/python/
mv translate_*.py tools/python/
mv *_normalizer.py tools/python/
mv sort_dictionary.py tools/python/
# ... (full list in MIGRATION_PLAN.md)

# Move shell scripts
mv analyze_tests.sh tools/shell/
mv compare_results.sh tools/shell/
mv test_ala_paradigm.sh tools/shell/
```

---

## Pause Points

We will pause and verify after:
- ✅ Phase 1 complete → Test vendor builds work
- ⏸️ Phase 2 complete → Test pair builds work
- ⏸️ Phase 3 complete → Test all tools work
- ⏸️ All phases → Run full integration test

---

## Current Action: Start Phase 1

**Waiting for confirmation:**
1. Should I commit/stash your current changes on `feature/extractor-regeneration-pipeline` first?
2. Or create a new branch `feature/repo-restructure`?
3. Or work directly on current branch?

**Recommendation:** Create new branch `feature/repo-restructure-vendor` specifically for this work.

---

## Next Steps After Your Confirmation

1. Handle current branch state (commit/stash/new branch)
2. Execute Phase 1.1-1.7
3. Report results and verification status
4. Wait for your approval to continue to Phase 2


