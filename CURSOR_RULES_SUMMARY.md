# Cursor Rules Summary

**Created:** October 10, 2025  
**Location:** `.cursor/rules/`

## Overview

Created 6 comprehensive Cursor rules to guide AI assistance with this project. These rules automatically provide context, enforce workflows, and reference key documentation.

## Rules Created

### 1. **project-context.mdc** (Always Applied)
**Type:** `alwaysApply: true`  
**Purpose:** High-level project overview and quick reference  
**Contains:**
- Current project state (dictionary cleanup just completed)
- Critical reminders (PR workflow, quality standards)
- Quick command reference
- Links to all other rules

**Key Info:**
- Project status: Dictionary cleaned (6,667 entries, 0% errors)
- Translation quality: 75-92%
- Immediate priorities listed

---

### 2. **git-workflow.mdc** (Always Applied)
**Type:** `alwaysApply: true`  
**Purpose:** Enforce PR workflow - NEVER push to main  
**Contains:**
- Mandatory workflow: feature branch → commit → push branch → PR
- Branch naming conventions (feature/, fix/, refactor/, docs/, test/)
- Repository information

**Critical Rule:** All changes must go through pull requests. No direct pushes to main/master.

---

### 3. **project-progress.mdc** (Always Applied)
**Type:** `alwaysApply: true`  
**Purpose:** Track what's done and what's next  
**Contains:**
- Recently completed tasks (with checkmarks)
- Priority tasks organized by urgency (🔴 HIGH, 🟡 MEDIUM, 🟢 LOW)
- Links to detailed documentation
- Progress tracking guidelines

**Current Status:**
- ✅ Dictionary cleanup completed (4,253 errors fixed)
- Next: Testing & validation, coordination patterns, rebuild

---

### 4. **apertium-development.mdc** (On-Demand)
**Type:** `description: "Guidelines for Apertium development work"`  
**Purpose:** Comprehensive development guide  
**Contains:**
- Project structure explanation
- Dictionary file format (.dix) with examples
- Transfer rules (.t1x) guidelines
- Development workflow (build, test, commit)
- Common issues & solutions
- Performance considerations
- Quality standards checklist

**Size:** ~7 KB - comprehensive reference

---

### 5. **dictionary-quality.mdc** (Applied to *.dix files)
**Type:** `globs: *.dix` + `description`  
**Purpose:** Quality standards for dictionary editing  
**Contains:**
- Recent cleanup reference (Oct 10, 2025)
- Lemma-stem-paradigm consistency rules
- Paradigm assignment table (15+ patterns)
- Common error examples (all fixed)
- Validation tools and scripts
- Current statistics

**Quality Standards:**
- Correct paradigm for each word type
- Stem must match lemma minus ending
- No duplicates
- Alphabetically sorted
- No pipe characters

---

### 6. **documentation-map.mdc** (On-Demand)
**Type:** `description: "Map of all documentation files"`  
**Purpose:** Navigate 25+ documentation files  
**Contains:**
- Complete file index organized by purpose
- Quick search guide ("What needs to be done?" → link)
- Navigation guidance for different tasks
- File organization principles

**Key Sections:**
- Critical docs (read first)
- Recent work docs
- Historical docs
- Analysis docs
- Development guides
- Project directory structure

---

## How Rules Work Together

```
┌─────────────────────────┐
│  project-context.mdc    │ ← Always loaded: Quick overview
│  (Always Applied)       │
└─────────┬───────────────┘
          │
          ├─→ git-workflow.mdc (Always Applied: PR enforcement)
          ├─→ project-progress.mdc (Always Applied: Task status)
          │
          ├─→ documentation-map.mdc (On-demand: File navigation)
          ├─→ apertium-development.mdc (On-demand: Dev guidelines)
          └─→ dictionary-quality.mdc (Auto for .dix files: Quality standards)
```

## Usage by Task Type

### Starting New Session
**Auto-loaded:**
- `project-context.mdc` - Current state
- `git-workflow.mdc` - Workflow reminder
- `project-progress.mdc` - Task status

**Manually invoke:**
- `documentation-map.mdc` - Find relevant docs
- "What documentation shows next steps?" → Gets next steps doc

### Editing Dictionary Files
**Auto-loaded:**
- All 3 always-applied rules
- `dictionary-quality.mdc` (triggered by .dix glob)

**Available:**
- `apertium-development.mdc` - General guidelines

### Working on Transfer Rules
**Auto-loaded:**
- All 3 always-applied rules

**Manually invoke:**
- "Show me transfer rule guidelines" → Gets apertium-development.mdc
- "What's the next priority?" → Gets project-progress.mdc details

### Committing Changes
**Auto-loaded:**
- `git-workflow.mdc` - Reminds to create PR, not push to main

**Check:**
- `project-progress.mdc` - Update if completing a task

## Benefits

### 1. **Automatic Context**
AI always knows:
- Current project status
- What was just completed
- What needs to be done next
- Critical workflows to follow

### 2. **Quality Enforcement**
- PR workflow enforced (no direct main pushes)
- Dictionary quality standards available when editing .dix files
- Development guidelines readily accessible

### 3. **Navigation Help**
- 25+ docs organized and indexed
- Quick search guide for common questions
- Cross-references between related docs

### 4. **Knowledge Preservation**
- Work is documented in rules
- Future sessions start with full context
- Progress is tracked systematically

### 5. **Consistency**
- Same guidelines every time
- No need to repeat context
- Standards are codified

## Rule Maintenance

### When to Update

**project-progress.mdc:**
- After completing any task (mark with ✅)
- When starting new major work
- Update "Last Updated" date

**apertium-development.mdc:**
- When discovering new patterns
- When adding new tools or workflows
- When common issues emerge

**dictionary-quality.mdc:**
- When new error patterns are found
- When quality standards change
- After major dictionary work

**documentation-map.mdc:**
- When creating new documentation files
- When moving or reorganizing files
- When changing file purposes

**git-workflow.mdc:**
- Rarely - only if workflow policy changes

**project-context.mdc:**
- After major milestones
- When statistics change significantly
- When priorities shift

### How to Update

1. Edit the .mdc file directly in `.cursor/rules/`
2. Maintain the frontmatter (metadata between `---`)
3. Keep cross-references up to date (use `(mdc:path)` syntax)
4. Update dates and statistics
5. No need to rebuild - changes are immediate

## File Sizes

```
project-context.mdc       ~4.7 KB  (Quick reference)
git-workflow.mdc          ~1.1 KB  (Simple rule)
project-progress.mdc      ~3.5 KB  (Task tracker)
apertium-development.mdc  ~7.0 KB  (Comprehensive guide)
dictionary-quality.mdc    ~5.9 KB  (Quality standards)
documentation-map.mdc     ~7.8 KB  (File index)
────────────────────────────────
Total                    ~30.0 KB  (Efficient context)
```

## Cross-References

All rules reference each other using `(mdc:path)` syntax:
- Enables one-click navigation
- Keeps documentation interconnected
- Makes information easy to find

Example network:
```
project-context.mdc
  ├─→ git-workflow.mdc
  ├─→ project-progress.mdc
  │   └─→ NEXT_STEPS_RECOMMENDATIONS.md
  ├─→ apertium-development.mdc
  ├─→ dictionary-quality.mdc
  │   ├─→ DICTIONARY_FIXES_SUMMARY.md
  │   └─→ SUSPICIOUS_PATTERNS_FIXED.md
  └─→ documentation-map.mdc
      └─→ [All 25+ project docs]
```

## Success Metrics

✅ **Achieved:**
- All critical workflows documented
- Project state captured
- 25+ existing docs indexed
- Quality standards codified
- Navigation made easy

📊 **Measurable Benefits:**
- Reduces context setup time (from minutes to seconds)
- Enforces PR workflow (prevents accidental main pushes)
- Provides instant access to relevant guidelines
- Tracks progress systematically

## Quick Start for New Users

1. Open any file in the project
2. Cursor will automatically load:
   - `project-context.mdc` (what's this project?)
   - `git-workflow.mdc` (how do I commit?)
   - `project-progress.mdc` (what's next?)
3. Ask questions like:
   - "What needs to be done next?"
   - "How do I edit the dictionary?"
   - "Show me the git workflow"
4. Rules will automatically reference relevant docs

## Related Documentation

- **All rules:** `.cursor/rules/*.mdc`
- **Project docs:** See `documentation-map.mdc` for complete index
- **Next steps:** See `NEXT_STEPS_RECOMMENDATIONS.md`
- **Recent work:** See `DICTIONARY_FIXES_SUMMARY.md`

---

**Note:** These rules are designed to work together. Each provides a different level of detail, from quick overview (project-context) to comprehensive guides (apertium-development, dictionary-quality).

