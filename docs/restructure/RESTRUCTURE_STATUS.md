# Repository Restructure - Current Status

**Date:** October 20, 2025  
**Branch:** `feature/repo-restructure-vendor`  
**Phase Completed:** Phase 1 (Vendor Separation) ✅

---

## What's Been Done

### ✅ Phase 1: Vendor Separation (COMPLETE)

**Goal:** Separate vendor dependencies into submodules under `apertium/vendor/`

**Accomplished:**
1. Created new directory structure:
   - `apertium/vendor/` - for vendor submodules
   - `apertium/build/` - for build artifacts
   - `apertium/tests/` - for tests (empty, ready)
   - `apertium/docs/` - for documentation (empty, ready)

2. Cleaned up old submodule configuration:
   - Removed 10 old submodule entries
   - Fixed git worktrees issue

3. Added 4 new vendor submodules:
   - ✅ `vendor/lttoolbox` → https://github.com/apertium/lttoolbox.git
   - ✅ `vendor/apertium` → https://github.com/apertium/apertium.git
   - ✅ `vendor/apertium-ido` → https://github.com/komapc/apertium-ido.git
   - ✅ `vendor/apertium-epo` → https://github.com/apertium/apertium-epo.git

4. Installed Makefile for `apertium/`

5. Partially built vendor tools:
   - ✅ lttoolbox: Fully built and installed (14 tools available)
   - 🔄 apertium: Partially compiled (interrupted but can resume)

**Files Changed:** 20 files, 5 commits  
**Git Status:** Clean, all changes committed

---

## Current State

### Directory Structure (Partial)
```
/home/mark/apertium-ido-epo/
├── apertium/
│   └── apertium-dev/
│       ├── vendor/                    # ✅ Created
│       │   ├── lttoolbox/            # ✅ Submodule (built)
│       │   ├── apertium/             # ✅ Submodule (partial)
│       │   ├── apertium-ido/         # ✅ Submodule
│       │   └── apertium-epo/         # ✅ Submodule
│       ├── build/                     # ✅ Created (empty)
│       ├── tests/                     # ✅ Created (empty)
│       ├── docs/                      # ✅ Created (empty)
│       ├── data/                      # ✅ Created (empty)
│       └── Makefile                   # ✅ Installed
├── apertium-ido-epo/                  # ⏳ Not moved yet
├── ido-esperanto-extractor/           # ⏳ Not moved yet
├── ido-epo-translator-web/            # ⏳ Not moved yet
├── apertium-bel/                      # ⏳ To be archived
├── apertium-rus/                      # ⏳ To be archived
├── apertium-bel-rus/                  # ⏳ To be archived
├── apertium-fra/                      # ⏳ To be archived
├── test/                              # ⏳ To be consolidated
├── tests/                             # ⏳ To be consolidated
├── scripts/                           # ⏳ To be moved to tools/
├── [analysis scripts]                 # ⏳ To be moved to tools/python/
└── [documentation files]              # ⏳ To be moved to docs/
```

### What's Working
- ✅ Git submodules configured correctly
- ✅ New directory structure in place
- ✅ lttoolbox fully built and available
- ✅ All planning documents created
- ✅ Branch is clean and ready for next phase

### What's Not Done Yet
- ⏳ apertium core (partially built, can resume)
- ⏳ Move main language pair to new location
- ⏳ Move tools (extractor, web) to `tools/`
- ⏳ Consolidate tests
- ⏳ Move scripts to `tools/python/` and `tools/shell/`
- ⏳ Move documentation to `docs/`
- ⏳ Archive unused language repos
- ⏳ Update CI/CD workflows
- ⏳ Remove duplicates

---

## Next Steps

### Immediate: Continue Restructure (Recommended)

Since vendor submodules are configured and lttoolbox is built, we can continue restructuring without waiting for the full apertium build.

**Phase 2: Core Pair Move**
1. Move `apertium-ido-epo/` to `apertium/`
2. Remove duplicate `.dix` files from root
3. Create temporary symlink for compatibility
4. Update pair Makefile (if needed)

**Estimated time:** 15 minutes

**Phase 3: Tools Move**
1. Create `tools/` structure
2. Move `ido-esperanto-extractor` to `tools/extractor/`
3. Move `ido-epo-translator-web` to `tools/web/`
4. Move scripts to `tools/python/` and `tools/shell/`

**Estimated time:** 20 minutes

**Phases 4-8:** Tests, docs, CI/CD, cleanup (~2 hours)

---

## Alternative: Pause and Review

If you want to review the vendor setup before continuing:

1. Finish building apertium:
   ```bash
   cd /home/mark/apertium-ido-epo/apertium/apertium-dev
   make vendor  # Resume where it left off
   ```

2. Test vendor tools:
   ```bash
   export PATH=/home/mark/apertium-ido-epo/apertium/vendor/installed/bin:$PATH
   lt-comp --version
   # After full build:
   apertium-preprocess-transfer --version
   ```

3. Review and come back later

---

## Recommendation

**Proceed with Phase 2 now** - we don't need the full apertium build to continue restructuring. The build can finish later when we actually need to compile the language pair.

Benefits:
- Keep momentum
- Complete all file moves in one session
- Test everything together
- Single comprehensive PR

---

## Questions

1. **Continue now or pause?**
   - Recommend: Continue (momentum)

2. **Finish apertium build first?**
   - Recommend: No, not needed yet (can build when compiling pair)

3. **Keep working or review planning docs?**
   - Recommend: Keep working (planning docs are solid)

---

**Ready for Phase 2?** Say "continue" to proceed with moving the core pair.

**Want to pause?** Say "pause" and I'll:
- Push the current branch
- Create a summary of what to do next
- Wait for you to review and come back

