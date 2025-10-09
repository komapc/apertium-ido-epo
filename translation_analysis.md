# Translation Analysis: Ido → Esperanto (Republiko Article)

## Sentence 1
**Ido Input:**
```
Republiko esas guvernala sistemo ube la chefo di stato (qua maxim-multa-kaze havas la titulo "prezidanto", ma en antiqua Roma esis "konsulo") elektesas dal populo o dal parlamento, e ne povas transmisar la povo heredale a lua familio, quale eventas en monarkii.
```

**Apertium Output:**
```
Respubliko estas *guvernala sistemo #kie, kien #la ĉefo de ŝtato (#kiu *maxim-multa-#unknown havas #la #unknown "#unknown", sed en antikva #unknown #esti "konsulo") #unknown *dal #popolnombro aŭ *dal parlamento, kaj ne povas #unknown #la #unknown #unknown al @lu familio, kiel #eventi en #unknown.
```

**Expected Esperanto:**
```
Respubliko estas registara sistemo kie la ĉefo de ŝtato (kiu plej-multe-kaze havas la titolon "prezidanto", sed en antikva Romo estis "konsulo") elektiĝas de la popolo aŭ de la parlamento, kaj ne povas transdoni la povon heredale al sia familio, kiel okazas en monarĥioj.
```

### Issues Found:
- ❌ `guvernala` → `*guvernala` (not translated) — should be `registara` or `regada`
- ❌ `ube` → `#kie, kien` (confusion) — should be just `kie`
- ❌ `#la` (with hash) appearing multiple times — definite article handling issues
- ❌ `maxim-multa-kaze` → `*maxim-multa-#unknown` — should be `plej-multe-kaze` or `plej ofte`
- ❌ `titulo` → `#unknown` (not in dictionary) — should be `titolo`
- ❌ `prezidanto` → `#unknown` (not in dictionary) — should be `prezidanto`
- ❌ `Roma` → `#unknown` (not in dictionary) — should be `Romo`
- ❌ `elektesas` → `#unknown` (not recognized) — should be `elektiĝas`
- ❌ `dal` → `*dal` (not translated) — should be `de la` or `de`
- ❌ `populo` → `#popolnombro` (wrong translation) — should be `popolo`
- ❌ `transmisar` → `#unknown` (not in dictionary) — should be `transdoni` or `transmeti`
- ❌ `povo` → `#unknown` (not in dictionary) — should be `povo`
- ❌ `heredale` → `#unknown` (not in dictionary) — should be `heredale` or `hereditare`
- ❌ `lua` → `@lu` (wrong form) — should be `sia`
- ❌ `eventas` → `#eventi` (wrong form) — should be `okazas`
- ❌ `monarkii` → `#unknown` (not in dictionary) — should be `monarĥioj`

---

## Sentence 2
**Ido Input:**
```
L'origino di la vorto republiko esas 2 Latina vorti: res publica (publika kozo, o publik afero).
```

**Apertium Output:**
```
*L'origino de #la vorto respubliko estas *2 latinaj vortoj: #unknown *publica (publika #aĵo, afero, aŭ *publik afero).
```

**Expected Esperanto:**
```
La origino de la vorto respubliko estas 2 latinaj vortoj: res publica (publika afero, aŭ publika afero).
```

### Issues Found:
- ❌ `L'origino` → `*L'origino` (contraction not handled) — should be `La origino`
- ✅ `Latina` → `latinaj` (correct!)
- ✅ `vorti` → `vortoj` (correct!)
- ❌ `res` → `#unknown` (not in dictionary)
- ❌ `publica` → `*publica` (marked as unknown)
- ❌ `kozo` → `#aĵo` (wrong/confused) — should be `afero` or `aĵo`
- ❌ `publik` → `*publik` (not declined) — should be `publika`

---

## Sentence 3
**Ido Input:**
```
Se la chefo di stato anke esas chefo di guvernerio, la lando esas prezidantala republiko (exemple en Usa, Brazilia, Arjentinia).
```

**Apertium Output:**
```
@Se #la ĉefo de ŝtato #unknown estas ĉefo de #unknown, #la lando estas *prezidantala respubliko (#unknown en #Usono, @Brazili, #unknown).
```

**Expected Esperanto:**
```
Se la ĉefo de ŝtato ankaŭ estas ĉefo de registaro, la lando estas prezidanta respubliko (ekzemple en Usono, Brazilo, Argentino).
```

### Issues Found:
- ❌ `anke` → `#unknown` (not in dictionary) — should be `ankaŭ`
- ❌ `guvernerio` → `#unknown` (not in dictionary) — should be `registaro`
- ❌ `prezidantala` → `*prezidantala` (not declined properly) — should be `prezidanta`
- ❌ `exemple` → `#unknown` (not in dictionary) — should be `ekzemple`
- ✅ `Usa` → `#Usono` (close, but with hash)
- ❌ `Brazilia` → `@Brazili` (wrong form) — should be `Brazilo`
- ❌ `Arjentinia` → `#unknown` (not in dictionary) — should be `Argentino`

---

## Sentence 4
**Ido Input:**
```
Se la chefo di guvernerio ne esas anke chefo di stato, ed selektesas da deputati de la precipua partisi (o koalisuro) en parlamento, la sistemo nominesas parlamentala republiko (exemple en Portugal, Finlando, Francia).
```

**Apertium Output:**
```
@Se #la ĉefo de #unknown ne estas *anke ĉefo de ŝtato, kaj #unknown de #unknown de #la precipaj partioj (aŭ #unknown) en parlamento, #la sistemo #unknown *parlamentala respubliko (#unknown en *Portugal, #Finnlando, #franco).
```

**Expected Esperanto:**
```
Se la ĉefo de registaro ne estas ankaŭ ĉefo de ŝtato, kaj elektiĝas de deputitoj de la precipaj partioj (aŭ koalicio) en parlamento, la sistemo nomiĝas parlamenta respubliko (ekzemple en Portugalio, Finnlando, Francio).
```

### Issues Found:
- ✅ `precipua` → `precipaj` (correct!)
- ✅ `partisi` → `partioj` (correct!)
- ❌ `anke` → `*anke` (not fully translated) — should be `ankaŭ`
- ❌ `selektesas` → `#unknown` (not in dictionary) — should be `elektiĝas`
- ❌ `deputati` → `#unknown` (not in dictionary) — should be `deputitoj`
- ❌ `koalisuro` → `#unknown` (not in dictionary) — should be `koalicio`
- ❌ `nominesas` → `#unknown` (not in dictionary) — should be `nomiĝas`
- ❌ `parlamentala` → `*parlamentala` (not declined) — should be `parlamenta`
- ❌ `Portugal` → `*Portugal` — should be `Portugalio`
- ✅ `Finlando` → `#Finnlando` (close!)
- ❌ `Francia` → `#franco` (wrong) — should be `Francio`

---

## Sentence 5
**Ido Input:**
```
La prezidanti, maxim-multa-kaze en la moderna republiki, guvernas por periodi de 4 til 6 yari.
```

**Apertium Output:**
```
#La #unknown, *maxim-multa-#unknown en #la modernaj respublikoj, direktas por periodoj de #unknown #unknown *6 jaroj.
```

**Expected Esperanto:**
```
La prezidantoj, plej-multe-kaze en la modernaj respublikoj, regas por periodoj de 4 ĝis 6 jaroj.
```

### Issues Found:
- ❌ `prezidanti` → `#unknown` (not in dictionary) — should be `prezidantoj`
- ❌ `maxim-multa-kaze` → `*maxim-multa-#unknown` — should be `plej-multe-kaze`
- ✅ `moderna` → `modernaj` (correct!)
- ✅ `republiki` → `respublikoj` (correct!)
- ❌ `guvernas` → `direktas` (wrong translation) — should be `regas`
- ✅ `periodi` → `periodoj` (correct!)
- ❌ `4` → `#unknown` (numbers not handled)
- ❌ `til` → `#unknown` (not in dictionary) — should be `ĝis`
- ✅ `6` → `*6` (recognized but marked)
- ✅ `yari` → `jaroj` (correct!)

---

## Sentence 6
**Ido Input:**
```
En kelka landi, la konstituco limitizas la quanto di inter-sequanta foyi qui ula persono povas disputar prezidantal elekti.
```

**Apertium Output:**
```
En kelkaj landoj, #la #unknown #unknown #la kvanto de inter-*sequanta fojoj #kio iu persono povas disputi *prezidantal elektoj.
```

**Expected Esperanto:**
```
En kelkaj landoj, la konstitucio limitas la kvanton de inter-sekvantaj fojoj kiujn iu persono povas disputi prezidantajn elektojn.
```

### Issues Found:
- ✅ `kelka` → `kelkaj` (correct!)
- ✅ `landi` → `landoj` (correct!)
- ❌ `konstituco` → `#unknown` (not in dictionary) — should be `konstitucio`
- ❌ `limitizas` → `#unknown` (not in dictionary) — should be `limitas`
- ✅ `quanto` → `kvanto` (correct!)
- ❌ `sequanta` → `*sequanta` (not declined) — should be `sekvantaj`
- ✅ `foyi` → `fojoj` (correct!)
- ❌ `qui` → `#kio` (wrong relative pronoun) — should be `kiujn`
- ✅ `iu` → `iu` (correct!)
- ✅ `persono` → `persono` (correct!)
- ✅ `povas` → `povas` (correct!)
- ✅ `disputar` → `disputi` (correct!)
- ❌ `prezidantal` → `*prezidantal` (not declined) — should be `prezidantajn`
- ✅ `elekti` → `elektoj` (correct!)

---

## Sentence 7
**Ido Input:**
```
Exemple en Usa e en Brazilia, prezidanti povas disputar rielekto nur unfoye sequante.
```

**Apertium Output:**
```
#unknown en #Usono kaj en @Brazili, #unknown povas disputi #unknown #unknown #unknown #unknown.
```

**Expected Esperanto:**
```
Ekzemple en Usono kaj en Brazilo, prezidantoj povas disputi reelekton nur unufoje sinsekve.
```

### Issues Found:
- ❌ `Exemple` → `#unknown` — should be `Ekzemple`
- ✅ `e` → `kaj` (correct!)
- ❌ `prezidanti` → `#unknown` — should be `prezidantoj`
- ❌ `rielekto` → `#unknown` — should be `reelekton`
- ❌ `nur` → `#unknown` — should be `nur`
- ❌ `unfoye` → `#unknown` — should be `unufoje`
- ❌ `sequante` → `#unknown` — should be `sinsekve`

---

## Sentence 8
**Ido Input:**
```
En Uruguay, la prezidanto elektesas por 5 yari e ne povas rielektesar.
```

**Apertium Output:**
```
En #unknown, #la #unknown #unknown por *5 jaroj kaj ne povas #unknown.
```

**Expected Esperanto:**
```
En Urugvajo, la prezidanto elektiĝas por 5 jaroj kaj ne povas reelektiĝi.
```

### Issues Found:
- ❌ `Uruguay` → `#unknown` — should be `Urugvajo`
- ❌ `prezidanto` → `#unknown` — should be `prezidanto`
- ❌ `elektesas` → `#unknown` — should be `elektiĝas`
- ✅ `5` → `*5` (marked but present)
- ✅ `yari` → `jaroj` (correct!)
- ✅ `e` → `kaj` (correct!)
- ✅ `ne povas` → `ne povas` (correct!)
- ❌ `rielektesar` → `#unknown` — should be `reelektiĝi`

---

## Sentence 9
**Ido Input:**
```
En Chili, lu elektesas por 4 yari e ne povas rielektesar.
```

**Apertium Output:**
```
En #Ĉilo, #li #unknown por *4 jaroj kaj ne povas #unknown.
```

**Expected Esperanto:**
```
En Ĉilio, li/ŝi elektiĝas por 4 jaroj kaj ne povas reelektiĝi.
```

### Issues Found:
- ✅ `Chili` → `#Ĉilo` (close!)
- ✅ `lu` → `#li` (close, though Esperanto would use `li/ŝi` or `ĝi`)
- ❌ `elektesas` → `#unknown` — should be `elektiĝas`
- ✅ `4` → `*4` (marked but present)
- ✅ `yari` → `jaroj` (correct!)
- ❌ `rielektesar` → `#unknown` — should be `reelektiĝi`

---

## Sentence 10
**Ido Input:**
```
En Venezuela pos modifiko en la konstituco ye la 15ma di februaro 2009, la periodo esas 6 yari e la prezidanto povas rielektesar absolute.
```

**Apertium Output:**
```
En #Venezuelo #unknown #unknown en #la #unknown je #la #dek-kvina de februaro #unknown, #la periodo estas *6 jaroj kaj #la #unknown povas #unknown @absolut.
```

**Expected Esperanto:**
```
En Venezuelo post modifo en la konstitucio je la 15-a de februaro 2009, la periodo estas 6 jaroj kaj la prezidanto povas reelektiĝi absolute.
```

### Issues Found:
- ✅ `Venezuela` → `#Venezuelo` (close!)
- ❌ `pos` → `#unknown` — should be `post`
- ❌ `modifiko` → `#unknown` — should be `modifo`
- ❌ `konstituco` → `#unknown` — should be `konstitucio`
- ✅ `ye` → `je` (correct!)
- ✅ `15ma` → `#dek-kvina` (close!)
- ✅ `februaro` → `februaro` (correct!)
- ❌ `2009` → `#unknown` (year not handled)
- ✅ `periodo` → `periodo` (correct!)
- ✅ `6` → `*6` (marked but present)
- ✅ `yari` → `jaroj` (correct!)
- ❌ `prezidanto` → `#unknown` — should be `prezidanto`
- ❌ `rielektesar` → `#unknown` — should be `reelektiĝi`
- ❌ `absolute` → `@absolut` (wrong form) — should be `absolute` or `senlime`

---

## Sentence 11
**Ido Input:**
```
Segun Aristoteles, la tri principi fundamentala di ula republiko esas: la separo di povi e lua mutuala kontrolo, l'aktiva partopreno en la politiko di omna civitani, la reprezento di omna sociala klasi en tota guvernala institucuri, sen prepondoro di ula.
```

**Apertium Output:**
```
@Segun #unknown, #la *tri principoj #unknown de iu respubliko estas: #la #unknown de #unknown kaj @lu mutuala #unknown, *l'aktiva #unknown en #la politiko de #ĉiu #unknown, #la #unknown de #ĉiu socialaj klasoj en #unknown #unknown #unknown, @sen #unknown de iu.
```

**Expected Esperanto:**
```
Laŭ Aristotelo, la tri principoj fundamentalaj de iu respubliko estas: la separo de povoj kaj ilia mutuala kontrolo, la aktiva partopreno en la politiko de ĉiuj civitanoj, la reprezento de ĉiuj socialaj klasoj en ĉiuj registaraj institucioj, sen prepondereco de iu.
```

### Issues Found:
- ❌ `Segun` → `@Segun` — should be `Laŭ`
- ❌ `Aristoteles` → `#unknown` — should be `Aristotelo`
- ✅ `tri` → `*tri` (marked but correct)
- ✅ `principi` → `principoj` (correct!)
- ❌ `fundamentala` → `#unknown` — should be `fundamentalaj`
- ✅ `iu` → `iu` (correct!)
- ✅ `respubliko` → `respubliko` (correct!)
- ❌ `separo` → `#unknown` — should be `separo`
- ❌ `povi` → `#unknown` — should be `povoj`
- ❌ `lua` → `@lu` — should be `ilia`
- ✅ `mutuala` → `mutuala` (correct!)
- ❌ `kontrolo` → `#unknown` — should be `kontrolo`
- ❌ `l'aktiva` → `*l'aktiva` — should be `la aktiva`
- ❌ `partopreno` → `#unknown` — should be `partopreno`
- ✅ `politiko` → `politiko` (correct!)
- ✅ `omna` → `#ĉiu` (close, should be `ĉiuj`)
- ❌ `civitani` → `#unknown` — should be `civitanoj`
- ❌ `reprezento` → `#unknown` — should be `reprezento`
- ✅ `sociala` → `socialaj` (correct!)
- ✅ `klasi` → `klasoj` (correct!)
- ❌ `tota` → `#unknown` — should be `ĉiuj`
- ❌ `guvernala` → `#unknown` — should be `registaraj`
- ❌ `institucuri` → `#unknown` — should be `institucioj`
- ❌ `sen` → `@sen` (marked but present)
- ❌ `prepondoro` → `#unknown` — should be `prepondereco`

---

## Sentence 12
**Ido Input:**
```
Moderna konceptajo pri republiko kom demokrata sistemo di guvernerio aparis en Francia dum Iluminismo.
```

**Apertium Output:**
```
Moderna #unknown #pri respubliko *kom demokrata sistemo de #unknown #unknown en #franco #unknown *Iluminismo.
```

**Expected Esperanto:**
```
Moderna koncepto pri respubliko kiel demokrata sistemo de registaro aperis en Francio dum Klerismo.
```

### Issues Found:
- ✅ `Moderna` → `Moderna` (correct!)
- ❌ `konceptajo` → `#unknown` — should be `koncepto`
- ✅ `pri` → `#pri` (marked but correct)
- ✅ `respubliko` → `respubliko` (correct!)
- ❌ `kom` → `*kom` — should be `kiel`
- ✅ `demokrata` → `demokrata` (correct!)
- ✅ `sistemo` → `sistemo` (correct!)
- ❌ `guvernerio` → `#unknown` — should be `registaro`
- ❌ `aparis` → `#unknown` — should be `aperis`
- ❌ `Francia` → `#franco` — should be `Francio`
- ❌ `dum` → `#unknown` — should be `dum`
- ❌ `Iluminismo` → `*Iluminismo` — should be `Klerismo` or `Iluminismo`

---

## Sentence 13
**Ido Input:**
```
Usa adoptis republiko kande ol divenis nedependanta, ye la 4ma di julio 1776.
```

**Apertium Output:**
```
#Usono #adopti respublikon kiam #ĝi #fariĝi #unknown, je #la kvare de julio #unknown.
```

**Expected Esperanto:**
```
Usono adoptis respublikon kiam ĝi fariĝis sendependa, je la 4-a de julio 1776.
```

### Issues Found:
- ✅ `Usa` → `#Usono` (close!)
- ❌ `adoptis` → `#adopti` (wrong form) — should be `adoptis`
- ✅ `republiko` → `respublikon` (correct with accusative!)
- ✅ `kande` → `kiam` (correct!)
- ✅ `ol` → `#ĝi` (close!)
- ❌ `divenis` → `#fariĝi` (wrong form) — should be `fariĝis`
- ❌ `nedependanta` → `#unknown` — should be `sendependa`
- ✅ `ye` → `je` (correct!)
- ✅ `4ma` → `kvare` (close, should be `4-a` or `kvara`)
- ✅ `julio` → `julio` (correct!)
- ❌ `1776` → `#unknown` (year not handled)

---

## Summary of Major Issues

### Categories of Problems:

#### 1. **Missing Dictionary Entries** (Most Critical)
Words not in the bilingual dictionary at all:
- `titulo` → should be `titolo`
- `prezidanto` → should be `prezidanto`
- `Roma` → should be `Romo`
- `elektesas` → should be `elektiĝas`
- `transmisar` → should be `transdoni`
- `povo` → should be `povo`
- `heredale` → should be `heredale`
- `monarkii` → should be `monarĥioj`
- `anke` → should be `ankaŭ`
- `guvernerio` → should be `registaro`
- `exemple` → should be `ekzemple`
- `Arjentinia` → should be `Argentino`
- `selektesas` → should be `elektiĝas`
- `deputati` → should be `deputitoj`
- `koalisuro` → should be `koalicio`
- `nominesas` → should be `nomiĝas`
- `prezidanti` → should be `prezidantoj`
- `til` → should be `ĝis`
- `konstituco` → should be `konstitucio`
- `limitizas` → should be `limitas`
- `rielekto` → should be `reelekton`
- `rielektesar` → should be `reelektiĝi`
- `nur` → should be `nur`
- `unfoye` → should be `unufoje`
- `sequante` → should be `sinsekve`
- `Uruguay` → should be `Urugvajo`
- `pos` → should be `post`
- `modifiko` → should be `modifo`
- `Aristoteles` → should be `Aristotelo`
- `fundamentala` → should be `fundamentalaj`
- `separo` → should be `separo`
- `povi` → should be `povoj`
- `kontrolo` → should be `kontrolo`
- `partopreno` → should be `partopreno`
- `civitani` → should be `civitanoj`
- `reprezento` → should be `reprezento`
- `tota` → should be `ĉiuj`
- `institucuri` → should be `institucioj`
- `prepondoro` → should be `prepondereco`
- `konceptajo` → should be `koncepto`
- `aparis` → should be `aperis`
- `dum` → should be `dum`
- `nedependanta` → should be `sendependa`

#### 2. **Morphological Analysis Issues**
Words marked with `*` or wrong forms:
- `guvernala` → not being declined properly
- `maxim-multa-kaze` → compound not recognized
- `dal` → preposition + article not handled
- `prezidantala` → adjective form not handled
- `parlamentala` → adjective form not handled
- `anke` → not fully translated
- Numbers: `4`, `2009`, `1776` not handled

#### 3. **Wrong Translations**
- `populo` → `#popolnombro` (should be `popolo`)
- `guvernas` → `direktas` (should be `regas`)
- `qui` → `#kio` (should be `kiujn`)
- `lua` → `@lu` (should be `sia` or `ilia`)
- `Segun` → should be `Laŭ`
- `kom` → should be `kiel`

#### 4. **Proper Nouns**
Many proper nouns not in dictionary:
- `Roma`, `Usa/Usono`, `Brazilia/Brazilo`, `Arjentinia/Argentino`
- `Portugal/Portugalio`, `Finlando/Finnlando`, `Francia/Francio`
- `Uruguay/Urugvajo`, `Chili/Ĉilio`, `Venezuela/Venezuelo`
- `Aristoteles/Aristotelo`

#### 5. **Grammatical Issues**
- Definite article handling: many `#la` marks
- Contractions: `L'origino`, `l'aktiva` not handled well
- Relative pronouns: `qui` → `#kio` (wrong case/form)
- Possessive pronouns: `lua` → `@lu` (should be `sia`/`ilia`)

#### 6. **Things That Work Well** ✅
- Basic noun plurals: `vorti` → `vortoj`, `yari` → `jaroj`
- Some adjective agreements: `Latina` → `latinaj`, `moderna` → `modernaj`
- Basic conjunctions: `e` → `kaj`, `o` → `aŭ`
- Some prepositions: `en` → `en`, `de` → `de`
- Basic verbs: `povas` → `povas`
- Some words: `persono`, `sistemo`, `periodo`, `demokrata`, `politiko`

---

## Statistics

**Total unique words in source text:** ~150 (estimated)

**Words successfully translated:** ~30-40 (20-25%)

**Words partially translated (with markers):** ~20 (13%)

**Words completely missing (#unknown):** ~90+ (60%+)

**Conclusion:** The dictionary coverage is approximately **20-25%** for this political/governmental text. The system needs:
1. Massive dictionary expansion (especially political/governmental vocabulary)
2. Better handling of verb forms (especially `-as` endings and `-iĝ-` forms)
3. Proper noun dictionary
4. Number handling
5. Compound word support
6. Better definite article handling
7. Contraction support

