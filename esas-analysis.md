# Analysis: "esar" (to be) - Critical Bug Found

## Issue Summary

The verb **"esar"** (to be) is defined with the **WRONG PARADIGM** in `apertium-ido.ido.dix`.

---

## Current State (BROKEN)

**File:** `apertium-ido.ido.dix` line 19816-19819

```xml
<e lm="esar">
  <i>es</i>
  <par n="a__adj"/>    ← WRONG! This is an adjective paradigm
</e>
```

### Result:
- ❌ "esas" is not recognized: `^esas/*esas$`
- ❌ All verb forms fail: esar, esas, esis, esos, etc.
- ❌ The system treats "es-" as an adjective stem

---

## Correct Configuration (NEEDED)

```xml
<e lm="esar">
  <i>es</i>
  <par n="ar__vblex"/>    ← CORRECT! This is the verb paradigm
</e>
```

### What This Generates:

The `ar__vblex` paradigm produces all Ido verb forms:

| Form | Suffix | Tag | Meaning |
|------|--------|-----|---------|
| es**ar** | -ar | `<vblex><inf>` | to be (infinitive) |
| es**as** | -as | `<vblex><pri>` | is/are (present) |
| es**is** | -is | `<vblex><pii>` | was/were (past) |
| es**os** | -os | `<vblex><fti>` | will be (future) |
| es**us** | -us | `<vblex><cni>` | would be (conditional) |
| es**ez** | -ez | `<vblex><imp>` | be! (imperative) |

---

## Testing

### Before Fix:
```bash
echo "esas" | lt-proc ido-epo.automorf.bin
# Output: ^esas/*esas$  ← Unknown word
```

### After Fix (Expected):
```bash
echo "esas" | lt-proc ido-epo.automorf.bin
# Output: ^esas/esar<vblex><pri>$  ← Recognized as present tense of "esar"
```

---

## Impact

This is a **CRITICAL BUG** because:

1. **"esar"** is the most fundamental verb in Ido (equivalent to "to be")
2. It appears in almost every sentence
3. Without it, basic sentences like "La kato esas granda" cannot be translated
4. This affects ALL 20 test sentences from the Wikipedia article

---

## Root Cause

Someone added "esar" to the dictionary but mistakenly used:
- `a__adj` (adjective paradigm for words ending in -a)
- Instead of `ar__vblex` (verb paradigm for verbs ending in -ar)

This is a simple typo/copy-paste error.

---

## Bilingual Dictionary Check

After fixing the monolingual entry, we need to ensure the bilingual dictionary has:

```xml
<e>
  <p>
    <l>esar<s n="vblex"/></l>
    <r>esti<s n="vblex"/></r>
  </p>
</e>
```

And that all tense tags are handled in transfer rules:
- `<pri>` → `<pri>` (present)
- `<pii>` → `<pii>` (past)
- `<fti>` → `<fti>` (future)
- etc.

---

## Priority

**FIX IMMEDIATELY** - This is blocking basic translation functionality.


