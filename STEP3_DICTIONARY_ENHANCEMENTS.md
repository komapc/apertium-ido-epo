# Step 3: Dictionary Enhancements for EPO-IDO Translation

## Missing Entries to Add to `apertium-ido-epo.ido-epo.dix`

### HIGH PRIORITY - Core Function Words

#### 1. Impersonal Pronoun "oni" → "on"

```xml
<!-- Impersonal pronoun: oni → on -->
<e><p><l>on<s n="prn"/></l><r>oni<s n="prn"/><s n="tn"/><s n="sg"/><s n="nom"/></r></p></e>
<e><p><l>on<s n="prn"/></l><r>oni<s n="prn"/><s n="tn"/><s n="pl"/><s n="nom"/></r></p></e>
<e><p><l>on<s n="prn"/></l><r>oni<s n="prn"/><s n="tn"/><s n="sg"/><s n="acc"/></r></p></e>
<e><p><l>on<s n="prn"/></l><r>oni<s n="prn"/><s n="tn"/><s n="pl"/><s n="acc"/></r></p></e>
<e><p><l>onu<s n="prn"/></l><r>onin<s n="prn"/><s n="tn"/><s n="sg"/><s n="acc"/></r></p></e>
<e><p><l>onu<s n="prn"/></l><r>onin<s n="prn"/><s n="tn"/><s n="pl"/><s n="acc"/></r></p></e>
```

#### 2. Partitive Marker "da" → "di"

```xml
<!-- Partitive marker: da → di -->
<e><p><l>di<s n="pr"/></l><r>da<s n="pr"/></r></p></e>
```

**NOTE:** This may already exist as "de → di" but "da" is specifically partitive.

#### 3. Superlative "plej" → "maxim"

```xml
<!-- Superlative marker: plej → maxim -->
<e><p><l>maxim<s n="adv"/></l><r>plej<s n="adv"/></r></p></e>
```

**Current status:** Entry exists for "plej" compound words but not standalone.

### MEDIUM PRIORITY - Religious Vocabulary

#### 4. Religion Core Terms

```xml
<!-- Christianity-related terms -->
<e><p><l>kristanismo<s n="n"/></l><r>kristanismo<s n="n"/></r></p></e>
<e><p><l>kristano<s n="n"/></l><r>kristano<s n="n"/></r></p></e>
<e><p><l>kristana<s n="adj"/></l><r>kristana<s n="adj"/></r></p></e>
<e><p><l>religio<s n="n"/></l><r>religio<s n="n"/></r></p></e>
<e><p><l>religioza<s n="adj"/></l><r>religia<s n="adj"/></r></p></e>

<!-- Jesus/Christ -->
<e><p><l>Iesu<s n="np"/></l><r>Jesuo<s n="np"/></r></p></e>
<e><p><l>Kristo<s n="np"/></l><r>Kristo<s n="np"/></r></p></e>

<!-- Religious concepts -->
<e><p><l>eklezio<s n="n"/></l><r>eklezio<s n="n"/></r></p></e>
<e><p><l>biblio<s n="n"/></l><r>Biblio<s n="n"/></r></p></e>
<e><p><l>testamento<s n="n"/></l><r>testamento<s n="n"/></r></p></e>
```

#### 5. Common Verbs and Adjectives

```xml
<!-- Based/founded -->
<e><p><l>bazita<s n="adj"/></l><r>bazita<s n="adj"/></r></p></e>
<e><p><l>bazar<s n="vblex"/></l><r>bazi<s n="vblex"/></r></p></e>

<!-- Teaching/instruction -->
<e><p><l>instruado<s n="n"/></l><r>instruoj<s n="n"/></r></p></e>
<e><p><l>instruar<s n="vblex"/></l><r>instrui<s n="vblex"/></r></p></e>

<!-- Worldwide/global -->
<e><p><l>tut-mondala<s n="adj"/></l><r>tutmonda<s n="adj"/></r></p></e>
<e><p><l>mondala<s n="adj"/></l><r>monda<s n="adj"/></r></p></e>

<!-- Exist -->
<e><p><l>existar<s n="vblex"/></l><r>ekzisti<s n="vblex"/></r></p></e>

<!-- Calculate/count -->
<e><p><l>kontar<s n="vblex"/></l><r>kalkuli<s n="vblex"/></r></p></e>

<!-- Originate -->
<e><p><l>orinjinar<s n="vblex"/></l><r>origini<s n="vblex"/></r></p></e>
```

#### 6. Geographic Names

```xml
<!-- Judea/Judaea -->
<e><p><l>Judea<s n="np"/></l><r>Judujo<s n="np"/></r></p></e>
<e><p><l>Judeana<s n="adj"/></l><r>juda<s n="adj"/></r></p></e>
```

#### 7. Time/Historical Terms

```xml
<!-- Century -->
<e><p><l>yar-cento<s n="n"/></l><r>jarcento<s n="n"/></r></p></e>
<e><p><l>yarcento<s n="n"/></l><r>jarcento<s n="n"/></r></p></e>

<!-- Billion -->
<e><p><l>miliardo<s n="n"/></l><r>miliardo<s n="n"/></r></p></e>
<e><p><l>miliardi<s n="n"/></l><r>miliardoj<s n="n"/></r></p></e>
```

### VERIFICATION NEEDED

Check if these already exist in the dictionary:

- ✓ "cirke" ← "ĉirkaŭ" (appears to work in test output)
- ✓ "mondo" ← "mondo" (common word, likely exists)
- ? "tutmonda" / "tut-mondala" (compound, may need entry)
- ? "kristanoj" plural form handling

## Implementation Notes

1. **Pronoun "oni"** - Currently shows as `@Oni` (unknown), needs entry
2. **Partitive "da"** - Shows as `@da` (unknown), needs entry  
3. **Superlative "plej"** - Passes through unchanged, needs entry
4. **Neuter pronoun "ĝi"** - Listed but shows as `@Prpers`, check bilingual mapping

## Testing Commands

After adding entries, test with:

```bash
cd /home/mark/apertium-dev/apertium-ido-epo
make

# Test individual patterns
echo "Oni kalkulas" | apertium -d . epo-ido
# Expected: On kontas

echo "miliardoj da kristanoj" | apertium -d . epo-ido  
# Expected: miliardi di kristani

echo "la plej granda religio" | apertium -d . epo-ido
# Expected: la maxim granda religio

echo "Ĝi estas granda" | apertium -d . epo-ido
# Expected: Ol esas granda
```

## Priority Order for Addition

1. **oni** → on (impersonal pronoun) - CRITICAL
2. **da** → di (partitive) - CRITICAL  
3. **plej** → maxim (superlative) - CRITICAL
4. **ĝi** → ol (check why current entry isn't working)
5. Religious vocabulary (kristanismo, etc.)
6. Common verbs (existar, kontar, etc.)
7. Geographic names (Judea, etc.)

---

_Document created: 2025-10-09_
_Based on: Kristanismo Wikipedia article analysis_

