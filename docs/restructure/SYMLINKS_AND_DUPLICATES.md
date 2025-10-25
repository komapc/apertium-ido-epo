# Duplicates and Symlinks Plan

**Status:** DRAFT  
**Purpose:** Identify all duplicates and define temporary compatibility symlinks

## Duplicate Files to Remove

### 1. Dictionary and Transfer Files at Root

**Source of truth:** `apertium/apertium-ido-epo/`

Files to **remove** from `/home/mark/apertium-ido-epo/`:
```
apertium-ido.ido.dix           → Duplicate of apertium-ido-epo/apertium-ido.ido.dix
apertium-epo.epo.dix           → Symlink (already in .gitignore), remove
apertium-ido-epo.ido-epo.dix   → Duplicate of apertium-ido-epo/apertium-ido-epo.ido-epo.dix
apertium-ido-epo.ido-epo.t1x   → Duplicate of apertium-ido-epo/apertium-ido-epo.ido-epo.t1x
apertium-ido-epo.epo-ido.t1x   → Duplicate of apertium-ido-epo/apertium-ido-epo.epo-ido.t1x
apertium-ido-epo.pc.in         → Duplicate
apertium-ido-epo.post-epo.dix  → Duplicate
apertium-ido-epo.post-ido.dix  → Duplicate
```

### 2. Compiled Binaries at Root

All `*.bin` files at root should be removed:
```
ido-epo.autobil.bin
ido-epo.autogen.bin
ido-epo.automorf.bin
ido-epo.autopgen.bin
ido-epo.t1x.bin
epo-ido.autobil.bin
epo-ido.autogen.bin
epo-ido.automorf.bin
epo-ido.autopgen.bin
epo-ido.t1x.bin
```

**New location:** `apertium/build/`

### 3. Python Scripts

**Duplicates between root and apertium-ido-epo/:**
```
Root                                      → apertium-ido-epo/
----------------------------------------  → ----------------------------------------
analyze_five_articles.py                  → analyze_five_articles.py (DUPLICATE)
analyze_ido_articles.py                   → analyze_ido_articles.py (DUPLICATE)
analyze_translations.py                   → analyze_translations.py (DUPLICATE)
convert_to_paradigms.py                   → convert_to_paradigms.py (DUPLICATE)
date_normalizer.py                        → date_normalizer.py (DUPLICATE)
detailed_error_analysis.py                → detailed_error_analysis.py (DUPLICATE)
fetch_and_translate_wikipedia.py          → fetch_and_translate_wikipedia.py (DUPLICATE)
generate_numbers.py                       → generate_numbers.py (DUPLICATE)
sort_dictionary.py                        → sort_dictionary.py (DUPLICATE)
translate_articles.py                     → translate_articles.py (DUPLICATE)
translate_specific_articles.py            → translate_specific_articles.py (DUPLICATE)
```

**Action:**
- Move root versions to `tools/python/`
- Remove versions from `apertium-ido-epo/` (they're not pair-specific)

**Also duplicate:**
```
scripts/build_ido_wiki_lexicon.py
apertium-ido-epo/scripts/build_ido_wiki_lexicon.py
```

**Action:** Keep one in `apertium-ido-epo/scripts/` (it's pair-specific), remove from root `scripts/`

### 4. Shell Scripts

**Duplicates:**
```
Root                          → apertium-ido-epo/
----------------------------  → ----------------------------
test_ala_paradigm.sh          → test_ala_paradigm.sh (DUPLICATE)
compare_results.sh            → compare_results.sh (DUPLICATE)
analyze_tests.sh              → analyze_tests.sh (DUPLICATE)
autogen.sh                    → autogen.sh (NOT duplicate - different)
```

**Action:**
- Move root versions to `tools/shell/` if generic
- Keep pair-specific versions in `apertium-ido-epo/`
- Examine to determine which is canonical

### 5. Test Files

**Root `test/` directory:**
```
test/ido-epo-*.txt
test/epo-ido-*.txt
test/README_PR_REGRESSION_TESTS.md
test/tests.json
```

**Root `tests/` directory:**
```
tests/test_date_normalizer.py
```

**apertium-ido-epo/test/ directory:**
```
apertium-ido-epo/test/* (likely duplicates)
```

**apertium-ido-epo/tests/ directory:**
```
apertium-ido-epo/tests/test_date_normalizer.py (duplicate of root tests/)
```

**Action:**
- Consolidate all under `apertium/tests/`
- Remove duplicates from `apertium-ido-epo/test/` and `apertium-ido-epo/tests/`

### 6. Documentation Files

**Analysis and progress files scattered at root:**
```
*_ANALYSIS.md
*_SUMMARY.md
*_FIX*.md
*_REPORT*.md
BEFORE_AFTER_COMPARISON.md
development_guide.md
NEXT_STEPS_RECOMMENDATIONS.md
PR_*.md
SESSION_*.md
IMPLEMENTATION_*.md
SUSPICIOUS_PATTERNS_FIXED.md
TRANSFER_RULES_REVIEW.md
... (40+ documentation files)
```

**Many also exist in `apertium-ido-epo/`**

**Action:**
- Move authoritative versions to `apertium/docs/`
- Remove duplicates from both root and `apertium-ido-epo/`

### 7. Data Files

**Translation test data at root:**
```
austria_esperanto.txt
austria_ido.txt
austria_raw.json
egipta_mitologio_esperanto.txt
egipta_mitologio_ido.txt
egipta_mitologio_raw.json
euro_esperanto.txt
euro_ido.txt
euro_raw.json
kanada_esperanto.txt
kanada_ido.txt
kanada_io_raw.json
tolkien_esperanto.txt
tolkien_ido.txt
tolkien_raw.json
ido-eu-article.txt
ido-eu-translated-*.txt
... (also in apertium-ido-epo/)
```

**Action:**
- Move to `apertium/data/raw/`
- Remove duplicates

### 8. Output and Analysis Files

**Root:**
```
analysis_after_fixes.txt
analysis_output.txt
analysis_with_normalizer.txt
dictionary_issues.txt
detailed_error_report.txt
final_fixes_report.txt
fixes_applied.txt
... (20+ output files)
outputs/*.json
outputs/*.tsv
```

**Action:**
- Move to `apertium/docs/analyses/` or `.gitignore` if regeneratable
- Consider keeping `outputs/` but gitignoring contents

### 9. Stray/Malformed Files

**File with invalid name at root:**
```
", new)\nif pair_counts:\n    top=pair_counts.most_common(1)[0][0]\n    print(TOP_PAIR,top)\n    for lemma,o,n in entries:\n        if (o,n)==top:\n            print(*,lemma)\n            break\nPY"
```

**Action:** Remove immediately (likely accidental paste or script error)

---

## Temporary Symlinks for Compatibility

During migration, create these symlinks to avoid breaking workflows:

### At repository root `/home/mark/apertium-ido-epo/`:

```bash
# Link to relocated pair
ln -s apertium/apertium-ido-epo apertium-ido-epo

# Link to build artifacts
ln -s apertium/build/*.bin .

# Link to common scripts (if scripts expect them at root)
ln -s tools/python/analyze_translations.py analyze_translations.py
ln -s tools/python/translate_articles.py translate_articles.py

# Link to test directory
ln -s apertium/tests test

# Link to current Makefile
ln -s apertium/Makefile Makefile.pair
```

### Symlink removal plan:

**Phase 1** (Immediate): Keep all symlinks functional  
**Phase 2** (After CI update): Remove symlinks for CI-only paths  
**Phase 3** (After all scripts updated): Remove all remaining symlinks  
**Phase 4** (Final): Verify no hardcoded paths remain

---

## Verification Commands

### Find all duplicates by hash:
```bash
cd /home/mark/apertium-ido-epo
find . -type f -name "*.py" -o -name "*.sh" | xargs md5sum | sort | uniq -w32 -D
```

### Find all .bin files:
```bash
find . -name "*.bin" -type f | grep -v node_modules | grep -v venv
```

### Find all analysis markdown files:
```bash
find . -maxdepth 1 -name "*_ANALYSIS.md" -o -name "*_SUMMARY.md" -o -name "*_FIX*.md"
```

### Check for symlinks:
```bash
find . -maxdepth 1 -type l -ls
```

---

## Removal Script (Safe, with backups)

```bash
#!/bin/bash
# Safe removal script with verification

BACKUP_DIR="/tmp/apertium-dev-cleanup-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Creating backup at $BACKUP_DIR"

# Function to safely remove file (with backup)
safe_remove() {
    local file="$1"
    if [ -e "$file" ]; then
        cp -a "$file" "$BACKUP_DIR/" 2>/dev/null || true
        rm -rf "$file"
        echo "Removed: $file"
    fi
}

# Remove duplicate dictionary files
safe_remove "apertium-ido.ido.dix"
safe_remove "apertium-epo.epo.dix"
safe_remove "apertium-ido-epo.ido-epo.dix"
safe_remove "apertium-ido-epo.ido-epo.t1x"
safe_remove "apertium-ido-epo.epo-ido.t1x"
safe_remove "apertium-ido-epo.pc.in"
safe_remove "apertium-ido-epo.post-epo.dix"
safe_remove "apertium-ido-epo.post-ido.dix"

# Remove compiled binaries
safe_remove "*.bin"

# Remove stray file
safe_remove '", new)
if pair_counts:
    top=pair_counts.most_common(1)[0][0]
    print(TOP_PAIR,top)
    for lemma,o,n in entries:
        if (o,n)==top:
            print(*,lemma)
            break
PY'

echo "Cleanup complete. Backup at $BACKUP_DIR"
echo "If everything works, you can remove the backup directory"
```

---

## Summary

**Total duplicates identified:** ~100+ files  
**Disk space to recover:** ~50-100 MB (mostly .bin files and docs)  
**Risk level:** Low (all have backups or are in git history)  

**Recommended approach:**
1. Create full backup before any deletion
2. Remove duplicates in phases (not all at once)
3. Test builds after each phase
4. Keep symlinks until CI is updated
5. Final cleanup only after full verification


