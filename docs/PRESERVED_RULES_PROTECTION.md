# Preserved Rules Protection - CRITICAL PROJECT RULE

**Date:** October 26, 2025  
**Status:** ✅ ACTIVE PROTECTION MECHANISM

---

## 🚨 CRITICAL RULE: Preserved Rules Must Include All Fixes

### Current Status
**✅ CONFIRMED:** The extractor has a preserved rules mechanism that protects morphological rules from being overwritten.

**⚠️ CRITICAL ISSUE:** Our recent fixes are NOT fully protected yet!

### What's Protected
- ✅ Basic morphological paradigms (`o__n`, `a__adj`, etc.)
- ✅ Symbol definitions (`n`, `adj`, `adv`, `vblex`, etc.)
- ✅ `percent` symbol (added for number recognition)
- ✅ `ciph` symbol (added for number recognition)

### What's NOT Protected (URGENT)
- ✅ `numeros` paradigm (for number recognition) - **NOW PROTECTED**
- ✅ `final` section with `<par n="numeros"/>` activation - **NOW PROTECTED**
- ❌ POS tagger in `modes.xml` (epo-ido pipeline)
- ❌ Transfer rules for number handling
- ❌ Post-generation rules (including the problematic `-ala` rule)

---

## 🔧 Required Actions

### 1. Update Preserved Rules File
**File:** `/home/mark/apertium-dev/projects/extractor/rules/apertium-ido.ido.dix.rules`

**Add missing elements:**
```xml
<!-- Number recognition paradigm -->
<pardef n="numeros">
  <e><re>[0-9]+([.,][0-9]+)*</re><p><l></l><r><s n="num"/><s n="ciph"/><s n="sp"/><s n="nom"/></r></p></e>
  <e><re>[0-9]+([.,][0-9]+)*</re><p><l></l><r><s n="num"/><s n="ciph"/><s n="sp"/><s n="acc"/></r></p></e>
  <e><re>[0-9]+([.,][0-9]+)*%</re><p><l></l><r><s n="num"/><s n="percent"/><s n="sp"/><s n="nom"/></r></p></e>
  <e><re>[0-9]+([.,][0-9]+)*%</re><p><l></l><r><s n="num"/><s n="percent"/><s n="sp"/><s n="acc"/></r></p></e>
</pardef>
```

**Add final section:**
```xml
<section id="final" type="inconditional">
  <e>
    <par n="numeros"/>
  </e>
</section>
```

### 2. Protect Pipeline Configuration
**File:** `modes.xml` - The POS tagger addition must be preserved:
```xml
<program name="apertium-tagger -g $2">
  <file name="/usr/share/apertium/apertium-epo/epo.prob"/>
</program>
```

**Status:** ⚠️ **MANUAL PROTECTION REQUIRED** - This is not in preserved rules file, must be manually preserved during extractor runs.

### 3. Protect Transfer Rules
**File:** `apertium-ido-epo.epo-ido.t1x` - Number handling rules must be preserved:
```xml
<def-cat n="num_ciph">
  <cat-item tags="num.ciph.sp.nom"/>
  <cat-item tags="num.ciph.sp.acc"/>
  <cat-item tags="num.percent.sp.nom"/>
  <cat-item tags="num.percent.sp.acc"/>
</def-cat>

<rule>
  <pattern>
    <pattern-item n="num_ciph"/>
  </pattern>
  <action>
    <out>
      <lu>
        <clip pos="1" side="tl" part="whole"/>
      </lu>
    </out>
  </action>
</rule>
```

**Status:** ⚠️ **MANUAL PROTECTION REQUIRED** - Transfer rules are not in preserved rules file, must be manually preserved during extractor runs.

### 4. Protect Post-Generation Rules
**File:** `apertium-ido-epo.post-epo.dix` - Contains problematic `-ala` rule:
```xml
<!-- Suffix transformations: -ala → -a (relational adjectives) -->
<e><p><l>ala</l><r>a</r></p></e>
```

**Status:** ⚠️ **MANUAL PROTECTION REQUIRED** - Post-generation rules are not in preserved rules file, must be manually preserved during extractor runs.

---

## 🛡️ Protection Mechanism

### How It Works
1. **Rules File:** `/home/mark/apertium-dev/projects/extractor/rules/apertium-ido.ido.dix.rules`
2. **Merge Script:** `/home/mark/apertium-dev/projects/extractor/scripts/merge_with_extractor.py`
3. **Process:** Rules + Word Entries → Complete Dictionary

### Current Workflow
```bash
# Extractor generates word entries
python3 scripts/export_apertium.py

# Merge script combines rules + words
python3 scripts/merge_with_extractor.py

# Result: Complete dictionary with preserved rules
```

---

## ⚠️ CRITICAL WARNING

**DO NOT RUN EXTRACTOR** until preserved rules are updated with all current fixes!

**Current fixes that would be lost:**
- Number recognition (`numeros` paradigm)
- POS tagger in pipeline
- Transfer rules for numbers
- All morphological improvements

---

## ✅ Verification Checklist

- [ ] `numeros` paradigm added to preserved rules
- [ ] `final` section added to preserved rules  
- [ ] POS tagger configuration documented
- [ ] Transfer rules documented
- [ ] Post-generation rules documented
- [ ] Merge script tested with updated rules
- [ ] Full pipeline tested after extractor run

---

## 📝 Notes

- The extractor exports to `dist/` directory only (no automatic commits)
- Manual deployment required to copy to repositories
- Rules are version controlled separately from word entries
- This mechanism prevents loss of morphological work during dictionary regeneration

**Last Updated:** October 26, 2025  
**Next Review:** After extractor run with updated preserved rules
