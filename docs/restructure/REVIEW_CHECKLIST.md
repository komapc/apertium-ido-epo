# Restructure Review Checklist

Use this checklist to review the restructuring plan before execution.

## 📋 Planning Documents to Review

- [ ] **STRUCTURE.md** - Understand the final directory layout
- [ ] **MIGRATION_PLAN.md** - Review the step-by-step migration process
- [ ] **SYMLINKS_AND_DUPLICATES.md** - Check which files will be removed
- [ ] **CI_CD_UPDATE_PLAN.md** - Verify CI/CD changes are acceptable
- [ ] **Makefile.new** - Review top-level build orchestration
- [ ] **Makefile.apertium-dev** - Review apertium-dev Makefile
- [ ] **.gitignore.new** - Verify ignore patterns are correct
- [ ] **RESTRUCTURE_SUMMARY.md** - Overall summary and timeline

## ❓ Questions to Answer

### Migration Strategy
- [ ] **Vendor repos:** Fresh submodules (A) or preserve history (B)?
      _Recommendation: A_

- [ ] **Inactive language pairs:** What to do with bel/rus/bel-rus/fra?
      _Recommendation: Archive under apertium/apertium-dev/archived/_

- [ ] **Root Makefile scope:** All subprojects or just apertium-dev?
      _Recommendation: All (core, extractor, web)_

- [ ] **Python dependencies:** Single requirements.txt or per-tool?
      _Recommendation: Per-tool_

- [ ] **Data directory:** Root level or under apertium/apertium-dev/?
      _Recommendation: Root level_

### CI/CD Preferences
- [ ] **Old workflow files:** Keep as .disabled or delete?
      _Recommendation: Delete after migration_

- [ ] **CI caching:** Cache vendor builds in GitHub Actions?
      _Recommendation: Yes_

- [ ] **Extractor schedule:** Automatic weekly or manual only?
      _Recommendation: Manual only_

- [ ] **Build notifications:** Need webhook notifications?
      _Recommendation: Use GitHub built-in_

## 🎯 Execution Approach

Choose one:

- [ ] **Option 1:** All at once (one feature branch, one PR)
      - Fastest but riskier
      - ~10-13 hours
      - Single comprehensive PR

- [ ] **Option 2:** Phased PRs (4 separate PRs)
      - Safer, easier to review
      - Can pause between phases
      - More controlled

- [ ] **Option 3:** Vendor-first (start small)
      - Minimal risk
      - Test vendor setup first
      - Decide on rest later

## ✅ Pre-Execution Checklist

- [ ] All uncommitted work is stashed or committed
- [ ] Current build is working (`make` succeeds)
- [ ] Current tests pass (`make test`)
- [ ] Backup created (just in case): `cp -r /home/mark/apertium-dev /tmp/apertium-dev-backup`
- [ ] Ready to create feature branch

## 🔍 Post-Migration Verification

After migration, verify:

- [ ] Vendor submodules initialized: `git submodule status`
- [ ] Vendor builds: `make -C apertium/apertium-dev vendor`
- [ ] Pair builds: `make -C apertium/apertium-dev pair`
- [ ] Tests pass: `make -C apertium/apertium-dev test`
- [ ] Web builds: `cd tools/web/ido-epo-translator-web && npm run build`
- [ ] Extractor runs: `cd tools/extractor/ido-esperanto-extractor && make`
- [ ] No unexpected files in `git status`
- [ ] No broken symlinks: `find . -xtype l`
- [ ] CI workflows pass on feature branch

## 🚨 Red Flags to Watch For

Stop and investigate if you see:

- [ ] More than 200 files in `git status --short`
- [ ] Build errors referencing old paths
- [ ] Missing submodules in `vendor/`
- [ ] Tests failing that previously passed
- [ ] CI failing with path-not-found errors
- [ ] Webpack/Vite build errors in web app

## 📝 Communication Plan

- [ ] Create PR with clear description
- [ ] Link to RESTRUCTURE_SUMMARY.md in PR description
- [ ] Tag any reviewers
- [ ] Document any deviations from plan
- [ ] Update project README after merge

## 🎉 Success Criteria

Migration is successful when:

- [ ] All builds work (`make core`, `make web`, `make extractor`)
- [ ] All tests pass
- [ ] CI/CD pipelines green
- [ ] No duplicate files remain
- [ ] Documentation updated
- [ ] Team notified of new structure

---

**Ready to proceed?** Answer the questions above and choose your execution approach!

