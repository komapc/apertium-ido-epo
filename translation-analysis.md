# Ido → Esperanto Translation Error Analysis

## Legend
- `#` = Unknown word (no translation found)
- `@` = Partially analyzed/untranslated form
- `*` = Known word (asterisk marking in apertium output)

---

## Sentence 1
**Ido:** La Europana Uniono esas politikala ed ekonomiala uniono di 27 membrostati qua lokesas en Europa.

**Esperanto (system):** #La *Europana *Uniono *esas *politikala *ed @ekonomi *uniono de *27 *membrostati #kiu *lokesas en @Europ .

**Expected Esperanto:** La Eŭropa Unio estas politika kaj ekonomia unio de 27 membroŝtatoj kiu situas en Eŭropo.

### Errors:
1. `#La` - Definite article "la" marked as unknown (should pass through)
2. `Europana` - Not converted to "Eŭropa" (adjective form)
3. `Uniono` - Not converted to "Unio" 
4. `esas` - Not translated to "estas"
5. `politikala` - Not converted to "politika"
6. `ed` - Not translated to "kaj"
7. `@ekonomi` - Word "ekonomiala" not fully analyzed/translated to "ekonomia"
8. `membrostati` - Not translated to "membroŝtatoj"
9. `#kiu` - Relative pronoun marked as unknown
10. `lokesas` - Not translated to "situas/troviĝas"
11. `@Europ` - Not fully analyzed to "Eŭropo"

---

## Sentence 2
**Ido:** L'Uniono di tri Pilastri establisiis per la Traktato di Maastricht en 1993.

**Esperanto (system):** @L '*Uniono de *tri @Pilastr *establisiis per #la *Traktato de *Maastricht en *1993.

**Expected Esperanto:** La Unio de tri Pilieroj establiĝis per la Traktato de Maastricht en 1993.

### Errors:
1. `@L` - Elided article not handled properly
2. `'*Uniono` - Apostrophe elision not processed correctly
3. `@Pilastr` - "Pilastri" not translated to "Pilieroj" (plural)
4. `establisiis` - Not translated to "establiĝis"

---

## Sentence 3
**Ido:** La decido-povo en l'Europana Uniono apartenas a diversa institucioni.

**Esperanto (system):** #La *decido-*povo en @l '*Europana *Uniono *apartenas al @divers *institucioni.

**Expected Esperanto:** La decido-povo en la Eŭropa Unio apartenas al diversaj institucioj.

### Errors:
1. `#La` - Article marked unknown
2. `decido-povo` - Compound not handled (should be "decid-povo" or "decidpovo")
3. `@l` - Elided article problem
4. `*apartenas` - Not converted to correct Esperanto form
5. `a` → `al` - Preposition correctly handled
6. `@divers` - "diversa" not fully translated to "diversaj"
7. `institucioni` - Not translated to "institucioj"

---

## Sentence 4
**Ido:** La judiciala sistemo ed internal aferi administresas da la Kortumo di Justitio di l'Europana Uniono.

**Esperanto (system):** #La @judici @sistem *ed *internal @afer *administresas de #la *Kortumo de *Justitio de @l '*Europana *Uniono.

**Expected Esperanto:** La juĝa sistemo kaj internaj aferoj administriĝas de la Kortumo de Justitio de la Eŭropa Unio.

### Errors:
1. `@judici` - "judiciala" not fully translated to "juĝa"
2. `@sistem` - "sistemo" not translated to "sistemo" (same form)
3. `ed` - Not translated to "kaj"
4. `@afer` - "aferi" not translated to "aferoj"
5. `administresas` - Not translated to "administriĝas"
6. `da` → `de` - Preposition conversion issue (should stay "de")

---

## Sentence 5
**Ido:** L'Europana Uniono havas extera relati kun altra stati en la mondo.

**Esperanto (system):** @L '*Europana *Uniono @hav *extera *relati kun @altr @stat en #la @mond .

**Expected Esperanto:** La Eŭropa Unio havas eksterajn rilatojn kun aliaj ŝtatoj en la mondo.

### Errors:
1. `@L` - Elided article issue
2. `@hav` - "havas" not fully translated to "havas"
3. `extera` → `eksterajn` - No accusative case added
4. `relati` → `rilatojn` - Not translated, no accusative
5. `@altr` - "altra" not translated to "aliaj"
6. `@stat` - "stati" not translated to "ŝtatoj"
7. `@mond` - "mondo" not fully processed

---

## Sentence 6
**Ido:** La ekonomio di l'Europana Uniono esas tre importanta por la mondo.

**Esperanto (system):** #La @ekonomi de @l '*Europana *Uniono *esas *tre *importanta por #la @mond .

**Expected Esperanto:** La ekonomio de la Eŭropa Unio estas tre grava por la mondo.

### Errors:
1. `@ekonomi` - "ekonomio" not fully processed
2. `esas` - Not translated to "estas"
3. `importanta` → `grava` - "importanta" could be "grava" or "importa" in Esperanto

---

## Sentence 7
**Ido:** L'interna merkato permisas la libera movimento di personari, servaji, kapitalo ed merkaturi.

**Esperanto (system):** @L '@intern @merkat *permisas #la @liber @moviment de *personari, *servaji, @kapital *ed *merkaturi.

**Expected Esperanto:** La interna merkato permesas la liberan movon de personoj, servoj, kapitalo kaj merkaĵoj.

### Errors:
1. `@L '@intern` - Elided article issue
2. `@merkat` - "merkato" not fully translated
3. `@liber` - "libera" not translated with accusative "liberan"
4. `@moviment` - "movimento" not translated to "movon"
5. `personari` - Not translated to "personoj"
6. `servaji` - Not translated to "servoj"
7. `@kapital` - "kapitalo" not fully processed
8. `merkaturi` - Not translated to "merkaĵoj"

---

## Sentence 8
**Ido:** La konkurenco reglamentesas da la Europana Komisiono.

**Esperanto (system):** #La *konkurenco *reglamentesas de #la *Europana @Komision .

**Expected Esperanto:** La konkurenco reguliĝas de la Eŭropa Komisiono.

### Errors:
1. `konkurenco` - Same in Esperanto (could pass through)
2. `reglamentesas` - Not translated to "reguliĝas"
3. `@Komision` - "Komisiono" not fully processed

---

## Sentence 9
**Ido:** La monetala uniono uzas l'euro quale komuna moneto.

**Esperanto (system):** #La *monetala *uniono *uzas @l '@eur @qual @komun @monet .

**Expected Esperanto:** La monera unio uzas la eŭron kiel komunan moneron.

### Errors:
1. `monetala` → `monera` - Adjective not translated
2. `uniono` → `unio` - Not converted
3. `uzas` - Same form (ok)
4. `@l '@eur` - "l'euro" elision problem, no accusative
5. `@qual` - "quale" not translated to "kiel"
6. `@komun` - "komuna" not translated with accusative
7. `@monet` - "moneto" not translated to "moneron"

---

## Sentence 10
**Ido:** La financala tutelado esas necesa por stabila ekonomio.

**Esperanto (system):** #La *financala *tutelado *esas @neces por @stabil @ekonomi .

**Expected Esperanto:** La financa protekto estas necesa por stabila ekonomio.

### Errors:
1. `financala` → `financa` - Not converted
2. `tutelado` → `protekto` - Not translated
3. `esas` → `estas` - Not translated
4. `@neces` - "necesa" not fully processed
5. `@stabil` - "stabila" not fully processed
6. `@ekonomi` - "ekonomio" not fully processed

---

## Sentence 11
**Ido:** L'energio-politiko celas redutar la dependeso de fossil karburanti.

**Esperanto (system):** @L '@energi-@politik *celas *redutar #la *dependeso de *fossil *karburanti.

**Expected Esperanto:** La energi-politiko celas redukti la dependecon de fosiliaj karburiloj.

### Errors:
1. `@L '@energi-@politik` - Elided compound word issue
2. `celas` - Same form (ok)
3. `redutar` → `redukti` - Infinitive not converted
4. `dependeso` → `dependecon` - No accusative, not translated
5. `fossil` → `fosiliaj` - No plural adjective agreement
6. `karburanti` → `karburiloj` - Not translated to plural

---

## Sentence 12
**Ido:** La substrukturo inkluzas transporto-reti e komunikado-sistemi.

**Esperanto (system):** #La *substrukturo *inkluzas @transport-@ret kaj *komunikado-@sistem .

**Expected Esperanto:** La infrastrukturo inkluzivas transport-retojn kaj komunikad-sistemojn.

### Errors:
1. `substrukturo` → `infrastrukturo` - Not translated
2. `inkluzas` → `inkluzivas` - Not fully converted
3. `@transport-@ret` - Compound "transporto-reti" not translated to "transport-retojn" (no accusative)
4. `e` → `kaj` - Correctly converted!
5. `komunikado-@sistem` - Not translated to "komunikad-sistemojn"

---

## Sentence 13
**Ido:** L'agrokultivo esas importanta sektoro en multa membri-stati.

**Esperanto (system):** @L '*agrokultivo *esas *importanta *sektoro en @mult @membr-@stat .

**Expected Esperanto:** La agrokultivo estas grava sektoro en multaj membr-ŝtatoj.

### Errors:
1. `@L` - Elision issue
2. `agrokultivo` → `agrokultivo` - Same (ok)
3. `esas` → `estas` - Not translated
4. `importanta` → `grava` - Could be "grava" or "importa"
5. `@mult` - "multa" not translated to "multaj"
6. `@membr-@stat` - Compound not translated

---

## Sentence 14
**Ido:** La protektado di l'ambiento esas prioritato por l'Europana Uniono.

**Esperanto (system):** #La *protektado de @l '*ambiento *esas *prioritato por @l '*Europana *Uniono.

**Expected Esperanto:** La protektado de la medio estas prioritato por la Eŭropa Unio.

### Errors:
1. `protektado` - Same form (ok)
2. `di` → `de` - Correctly converted
3. `@l '*ambiento` - Elision issue, "ambiento" → "medio"
4. `esas` → `estas` - Not translated
5. `prioritato` - Same form (ok)

---

## Sentence 15
**Ido:** L'eduko e cienco esas domeni ube l'Uniono investas multe.

**Esperanto (system):** @L '*eduko kaj @cienc *esas @domen *ube @l '*Uniono *investas @mult .

**Expected Esperanto:** La eduko kaj scienco estas domajnoj kie la Unio investas multe.

### Errors:
1. `@L '*eduko` - Elision issue
2. `e` → `kaj` - Correctly converted!
3. `@cienc` - "cienco" → "scienco"
4. `esas` → `estas` - Not translated
5. `@domen` - "domeni" → "domajnoj" (not translated)
6. `ube` → `kie` - Not translated
7. `investas` - Same form (ok)
8. `@mult` - "multe" not fully processed (but actually same)

---

## Sentence 16
**Ido:** La demografio di l'Europana Uniono montras diversa tendenci.

**Esperanto (system):** #La @demografi de @l '*Europana *Uniono *montras @divers *tendenci.

**Expected Esperanto:** La demografio de la Eŭropa Unio montras diversajn tendencojn.

### Errors:
1. `@demografi` - "demografio" not fully processed
2. `montras` - Same form (ok)
3. `@divers` - "diversa" not translated to "diversajn" (no accusative)
4. `tendenci` → `tendencojn` - Not translated, no accusative

---

## Sentence 17
**Ido:** En l'Uniono existas 24 oficiala lingui.

**Esperanto (system):** En @l '*Uniono *existas *24 *oficiala *lingui.

**Expected Esperanto:** En la Unio ekzistas 24 oficialaj lingvoj.

### Errors:
1. `En` - Correctly passed through
2. `@l '*Uniono` - Elision issue
3. `existas` → `ekzistas` - Not translated
4. `oficiala` → `oficialaj` - No plural agreement
5. `lingui` → `lingvoj` - Not translated

---

## Sentence 18
**Ido:** La religio esas libere selektebla en omna membrostati.

**Esperanto (system):** #La @religi *esas @liber *selektebl'en @omn *membrostati.

**Expected Esperanto:** La religio estas libere elektebla en ĉiuj membroŝtatoj.

### Errors:
1. `@religi` - "religio" not fully processed
2. `esas` → `estas` - Not translated
3. `@liber` - "libere" not fully processed (adverb)
4. `selektebla` → `elektebla` - Not translated
5. `@omn` - "omna" → "ĉiuj"
6. `membrostati` → `membroŝtatoj` - Not translated

---

## Sentence 19
**Ido:** La sanesoflego esas naciona kompetenteso ma kunlaboresas Europane.

**Esperanto (system):** #La *sanesoflego *esas *naciona *kompetenteso sed *kunlaboresas *Europane.

**Expected Esperanto:** La sanprizorgado estas nacia kompetenteco sed kunlaboras Eŭrope.

### Errors:
1. `sanesoflego` → `sanprizorgado` - Not translated
2. `esas` → `estas` - Not translated
3. `kompetenteso` → `kompetenteco` - Not fully converted
4. `ma` → `sed` - Correctly converted!
5. `kunlaboresas` → `kunlaboras` - Not fully converted
6. `Europane` → `Eŭrope` - Not translated

---

## Sentence 20
**Ido:** La kulturo e sporto esas importanta por la identeso di l'Uniono.

**Esperanto (system):** #La @kultur kaj @sport *esas *importanta por #la *identeso de @l '*Uniono.

**Expected Esperanto:** La kulturo kaj sporto estas gravaj por la identeco de la Unio.

### Errors:
1. `@kultur` - "kulturo" not fully processed
2. `e` → `kaj` - Correctly converted!
3. `@sport` - "sporto" not fully processed
4. `esas` → `estas` - Not translated
5. `importanta` → `gravaj` - Should be plural adjective
6. `identeso` → `identeco` - Not fully converted
7. `@l '*Uniono` - Elision issue

---

## Summary of Major Issues

### 1. **Definite Article (#La)**
The Ido/Esperanto article "la" is being marked as unknown (#La) instead of being passed through directly. This is a critical bug.

### 2. **Elision Not Handled (@l, @L, l', L')**
Elided forms like "l'Uniono", "l'euro" are not being properly processed. The apostrophe elision is common in both Ido and Esperanto but the system doesn't handle it.

### 3. **Core Verb "esas" → "estas"**
The most basic Ido verb "esas" (to be) is not being translated to Esperanto "estas". This is fundamental.

### 4. **Plural Endings (-i → -j)**
Ido plurals ending in -i (like "lingui", "tendenci", "stati") are not being converted to Esperanto -j forms.

### 5. **Adjective Plural Agreement**
Adjectives should agree in number and case in Esperanto but are not being converted (e.g., "diversa" → "diversaj").

### 6. **Accusative Case Missing**
Direct objects in Esperanto need the -n ending but it's not being added (e.g., "extera relati" → "eksterajn rilatojn").

### 7. **Partial Analysis (@symbol)**
Many words show @ symbol indicating they're partially analyzed but not fully translated.

### 8. **Conjunctions Sometimes Work**
Interestingly, "e" → "kaj" and "ma" → "sed" work in some cases but not consistently.

### 9. **Relative Pronoun (#kiu)**
Basic relative pronoun "kiu" (which/who) marked as unknown despite being identical in both languages.

### 10. **Common Words Missing**
Many common words aren't in the bilingual dictionary:
- existas → ekzistas
- esas → estas
- quale → kiel
- ube → kie
- omna → ĉiuj

### 11. **-ala → -a Adjective Suffix**
Ido adjectives with -ala suffix (politikala, judiciala, financala, monetala) not being converted to Esperanto -a form.

### 12. **Compound Words**
Hyphenated compounds are not handled properly, often showing partial translations.

---

## Recommendations for Fixes

1. **Fix article handling** - "la" should pass through
2. **Implement elision processing** - Handle l'/L' → la
3. **Add core vocabulary** - esas, existas, quale, ube, omna
4. **Fix plural conversion** - -i → -j for nouns
5. **Add accusative rules** - Direct objects need -n
6. **Fix adjective suffixes** - -ala → -a pattern
7. **Add plural adjective agreement**
8. **Debug @ symbol issues** - Why are so many words partially analyzed?
9. **Expand bilingual dictionary** - Missing many common words
10. **Fix compound word handling**


