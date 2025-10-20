# Merge Conflicts - Resolved

**Date:** October 20, 2025  
**PR:** #42  
**Status:** ✅ All conflicts resolved

## Conflicts Encountered

When merging `main` into `feature/repo-restructure-vendor`, we had 5 conflicts:

### 1. `apertium-ido-epo.ido-epo.dix` (bidix)
- **Conflict:** Deleted in our branch, modified in main
- **Resolution:** Kept main's version, moved to `apertium/apertium-ido-epo/`
- **Size comparison:** Both 704 KB (same size)
- **Decision:** Took main version (may have latest fixes)

### 2. `apertium-ido.ido.dix` (monodix)
- **Conflict:** Deleted in our branch, modified in main
- **Resolution:** Kept main's version, moved to `apertium/apertium-ido-epo/`
- **Size comparison:** Both 894 KB (same size)
- **Decision:** Took main version (may have latest fixes)

### 3. `development_guide.md`
- **Conflict:** Deleted in our branch, modified in main
- **Resolution:** Kept main's version, moved to `apertium/apertium-ido-epo/docs/`
- **Decision:** Preserve updated documentation

### 4. `test/ido-epo-pr-regression-input.txt`
- **Conflict:** Deleted in our branch, modified in main
- **Resolution:** Kept main's version, moved to `apertium/apertium-ido-epo/tests/`
- **Decision:** Preserve updated test input

### 5. `test/ido-epo-pr-regression-postgen-expected.txt`
- **Conflict:** Deleted in our branch, modified in main
- **Resolution:** Kept main's version, moved to `apertium/apertium-ido-epo/tests/`
- **Decision:** Preserve updated test expectations

## Additional Files from Main

Main branch also had these new files that we incorporated:

### Moved to `apertium/apertium-ido-epo/`:
- `ap_include.am` - Apertium include file
- `apertium-ido-epo.epo.epo.rlx` - CG disambiguation rules
- `apertium-ido-epo.ido-epo.dix.backup` - Dictionary backup
- `apertium-ido-epo.ido-epo.dix.formatted` - Formatted version
- `apertium-ido.ido.backup.dix` - Monodix backup
- `apertium-ido.ido.dix.backup` - Monodix backup
- `apertium-ido.ido.fixed.dix` - Fixed version
- `apertium-ido.ido.rlx` - Ido CG rules

### Moved to `apertium/apertium-ido-epo/docs/`:
- `WEB_UI_MOVED.md` - Documentation about web UI

### Moved to `apertium/apertium-ido-epo/tests/`:
- 60+ test output files (chunker, disam, generator, morph, postgen, pretransfer expected/output)

### Moved to `tools/shell/`:
- `test_new_vocabulary.sh` - Test script

## Resolution Strategy

1. **Dictionaries (.dix files):** Took main's version (instruction: use bigger, but sizes were same)
2. **Documentation:** Kept all, moved to appropriate locations
3. **Test files:** Kept all, moved to `apertium/apertium-ido-epo/tests/`
4. **Build files:** Moved to pair directory
5. **Scripts:** Moved to tools/shell/
6. **Everything removed from root** - maintains clean structure

## Verification

- ✅ All conflicts resolved
- ✅ All files moved to correct locations
- ✅ Root remains clean (4 items)
- ✅ No files lost
- ✅ Best versions preserved
- ✅ Structure intact

## Final Commit

Merge commit: `61ac3c9` + cleanup commit: `6ead2d1`

Total deletions from root: 123 files (all moved to appropriate subdirectories)

---

**Status:** ✅ Conflicts resolved, PR updated and ready for review

