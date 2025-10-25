# Phase 1: Vendor Separation - Progress Report

**Date:** October 20, 2025  
**Status:** ✅ COMPLETED (Submodule setup done, build in progress)

## Completed Steps

### 1. Git housekeeping ✅
- Removed old worktrees from git index
- Added .worktrees/ to .gitignore  
- Fixed submodule conflicts

### 2. Removed old submodule configuration ✅
- Removed 10 old submodule entries from git index:
  - apertium, lttoolbox (vendor tools)
  - apertium-ido, apertium-epo (monolingual)
  - apertium-bel, apertium-rus, apertium-bel-rus, apertium-fra (unused)
  - apertium-ido-epo (main pair - will relocate)
  - ido-esperanto-extractor (tool - will relocate)

### 3. Created new directory structure ✅
```
apertium/
└── apertium-dev/
    ├── vendor/          # New vendor submodules
    ├── build/           # For compiled artifacts
    ├── tests/           # For consolidated tests
    ├── docs/            # For documentation
    └── data/            # For corpora
```

### 4. Added vendor submodules in new location ✅
- `apertium/vendor/lttoolbox` → https://github.com/apertium/lttoolbox.git
- `apertium/vendor/apertium` → https://github.com/apertium/apertium.git
- `apertium/vendor/apertium-ido` → https://github.com/komapc/apertium-ido.git (your fork)
- `apertium/vendor/apertium-epo` → https://github.com/apertium/apertium-epo.git

All submodules cloned successfully.

### 5. Installed Makefile ✅
- Copied `Makefile.apertium-dev` to `apertium/Makefile`
- Makefile configured to:
  - Build vendor dependencies to `vendor/installed/`
  - Set PATH and PKG_CONFIG_PATH for vendor tools
  - Build pairs to `build/` directory

### 6. Started vendor build 🔄
- Command: `make vendor`
- lttoolbox: Building successfully (cmake configured, compiling)
- apertium: Started compiling (depends on lttoolbox)
- **Note:** Full build takes ~10-15 minutes

## Git Commits Made

1. `9a82943` - docs: Add restructure planning documents and extractor pipeline changes
2. `4ae187e` - fix: Remove worktrees from git index and ignore them
3. `d1fc158` - refactor: Remove old submodule configurations for restructure
4. `a780ee6` - feat: Add vendor submodules under apertium/vendor

## Verification Status

- ✅ Directory structure created
- ✅ Submodules added to .gitmodules
- ✅ Submodules cloned
- ✅ Makefile installed
- 🔄 Vendor build in progress (lttoolbox compiling, apertium started)
- ⏳ Vendor binaries not yet available (need full build to complete)

## Next Steps (Phase 2)

**After vendor build completes:**

1. Verify vendor tools work:
   ```bash
   export PATH=/home/mark/apertium-ido-epo/apertium/vendor/installed/bin:$PATH
   which lt-comp
   which apertium-preprocess-transfer
   ```

2. Move apertium-ido-epo to new location:
   ```bash
   mv /home/mark/apertium-ido-epo/apertium-ido-epo /home/mark/apertium-ido-epo/apertium/
   ```

3. Update pair Makefile to use vendor tools

4. Test pair build

## Current Branch

- Branch: `feature/repo-restructure-vendor`
- 4 commits ahead of `feature/extractor-regeneration-pipeline`
- Ready for continued work

## Pause Point Decision

**Option A:** Let vendor build complete (10-15 min), then continue with Phase 2
**Option B:** Stop here, push branch, review submodule setup, continue later
**Option C:** Skip full vendor build for now, proceed with moves (can build later)

**Recommendation:** Option C - Continue with restructuring; vendor can build when needed.

---

**Phase 1 Status:** ✅ Vendor submodule setup complete!  
**Can proceed to Phase 2:** Yes (move apertium-ido-epo)

