# Corpus Translations

**Date:** December 6, 2025  
**Direction:** Ido → Esperanto  
**Corpus:** `ido-epo-test-sentences.txt`

---

## Sentence 1: Historical/Linguistic Description of Ido

### Input (Ido)
```
Ido esas konstruktita linguo derivante de Reformita Esperanto (reformita linguo konstruktita de Esperanto, facita da la originala kreinto di Esperanto) adoptita kom Esperanto reformita en Paris da la Delegitaro (Délégation pour l'adoption d'une langue auxiliaire internationale) ye la 24ma di oktobro 1907. Ido kreesis por havar poka polisemio, esas sat konciza, facile lernebla e uzebla. Ol kreesis por esar Internaciona auxiliara linguo por personi de diversa origini e esas la maxim sucesoza de la multa Esperanto-derivaji, quin on nomizas Esperantidoj.
```

### Output (Esperanto)
```
@Id estas konstruita lingvon *derivante *de Reformita Esperanton (reformita lingvon konstruas *de Esperanto, faras #de ↓ (indikante aganton) #tio #originalo #kreiint #de ↓ (indikante aganton) Esperanto) adoptas *kom Esperanto reformas *en *Paris #de ↓ (indikante aganton) #tio #Delegitaro, delegacio (*Délégation *pour *l'*adoption *d'*une *langue *auxiliaire *internationale) *ye #tio *24ma #de ↓ (indikante aganton) oktobro *1907. @Id *kreesis *por havi malmulta *polisemio, estas *sat konciza, facile *lernebla *e *uzebla. *Ol *kreesis *por esti Internacia @auxiliar lingvo *por personoj *de diversaj originoj *e estas #tio *maxim #sukcecooz *de #tio multa Esperanto-derivaĵoj, *quin *on *nomizas *Esperantidoj.
```

### Expected Translation (Reference)
```
Ido estas konstruita lingvo derivanta de Reformita Esperanto (reformita lingvo konstruita de Esperanto, farita de la originala kreinto de Esperanto) adoptita kiel Esperanto reformita en Parizo de la Delegitaro (Délégation pour l'adoption d'une langue auxiliaire internationale) je la 24-a de oktobro 1907. Ido kreiĝis por havi malmultan polisemion, estas sufiĉe konciza, facile lernebla kaj uzebla. Ĝi kreiĝis por esti Internacia helpa lingvo por personoj de diversaj originoj kaj estas la plej sukcesa de la multaj Esperanto-derivaĵoj, kiujn oni nomas Esperantidoj.
```

### Errors Identified

**Unknown words (marked with `*`):**
- `*derivante` - should be "derivanta" (present participle)
- `*kreesis` - should be "kreiĝis" (past tense)
- `*polisemio` - should be "polisemio" (polysemy)
- `*sat` - should be "sufiĉe" (quite, enough)
- `*lernebla` - should be "lernebla" (learnable)
- `*uzebla` - should be "uzebla" (usable)
- `*Ol` - should be "Ĝi" (it)
- `*maxim` - should be "plej" (most)
- `*quin` - should be "kiujn" (which, accusative)
- `*on` - should be "oni" (one, they)
- `*nomizas` - should be "nomas" (names, calls)
- `*Esperantidoj` - should be "Esperantidoj" (Esperantidos)
- `*por` (multiple) - should be "por" (for)
- `*kom` - should be "kiel" (as)
- `*en` - should be "en" (in)
- `*Paris` - should be "Parizo" (proper noun)
- `*ye` - should be "je" (on, at)
- `*1907` - year not recognized
- `*e` - should be "kaj" (and)

**Translation rule issues (marked with `#`):**
- `#de ↓ (indikante aganton)` - incorrect handling of "da" (by)
- `#tio` - incorrect handling of "la" (the)
- `#originalo #kreiint` - incorrect handling of "originala kreinto" (original creator)
- `#sukcecooz` - incorrect handling of "sucesoza" (successful)

**Proper noun issues:**
- `@Id` - should be "Ido" (proper noun, @ marker indicates handling issue)
- `@auxiliar` - should be "helpa" (auxiliary)

**Grammar issues:**
- `lingvon` - should be "lingvo" (incorrect accusative)
- `konstruas` - should be "konstruita" (past participle)
- `faras` - should be "farita" (past participle)
- `adoptas` - should be "adoptita" (past participle)
- `reformas` - should be "reformita" (past participle)
- `multa` - should be "multaj" (many, plural)

---

## Sentence 2: Discussion About Ido Community Meeting

### Input (Ido)
```
Hodie partoprenis kin Idisti la saturdiala video-konfero. Ni diskutis inter altro kelka detali dil internaciona Ido-renkontro 2025 e la nova vorti dil google-grupo Linguo. Restas la questiono kad esas bona remplacigar od adjuntar ja existanta vorti per nova vorti por la sama kozo.
```

### Output (Esperanto)
```
Hodiaŭ partoprenas *kin Idistoj #tio *saturdia *video-#konferenci. #Ne diskutas *inter #alie #iom detaloj *dil internacia @Id-#renkonti *2025 *e #tio #nova ↓ vortoj *dil *google-#grupo ↓ Lingvo. Restas #tio demandon *kad estas bona *remplacigar *od aldoni #jam #ekzistoant vortoj *per #nova ↓ vortoj *por #tio sama aĵo.
```

### Expected Translation (Reference)
```
Hodiaŭ partoprenis kvin Idistoj la sabata videokonferenco. Ni diskutis inter alie kelkajn detalojn de la internacia Ido-renkontro 2025 kaj la novajn vortojn de la google-grupo Lingvo. Restas la demando ĉu estas bona anstataŭigi aŭ aldoni jam ekzistantajn vortojn per novaj vortoj por la sama afero.
```

### Errors Identified

**Unknown words (marked with `*`):**
- `*kin` - should be "kvin" (five)
- `*saturdia` - should be "sabata" (Saturday)
- `*video` - should be "video" (video)
- `*konferenci` - should be "konferenco" (conference)
- `*inter` - should be "inter" (among, between)
- `*dil` - should be "de la" (of the)
- `*2025` - year not recognized
- `*e` - should be "kaj" (and)
- `*dil` (second occurrence) - should be "de la" (of the)
- `*google` - should be "google" (proper noun/compound)
- `*kad` - should be "ĉu" (whether, if)
- `*remplacigar` - should be "anstataŭigi" (to replace)
- `*od` - should be "aŭ" (or)
- `*per` - should be "per" (by, with)
- `*por` - should be "por" (for)

**Translation rule issues (marked with `#`):**
- `#tio` - incorrect handling of "la" (the)
- `#Ne` - should be "Ni" (We) - capitalization/analysis issue
- `#alie` - incorrect translation of "altro" (other)
- `#iom` - incorrect translation of "kelka" (some)
- `#jam` - incorrect translation of "ja" (already)
- `#ekzistoant` - incorrect form of "ekzistanta" (existing)

**Grammar issues:**
- `partoprenas` - should be "partoprenis" (wrong tense: present vs past)
- `diskutas` - should be "diskutis" (wrong tense: present vs past)
- `detaloj` - should be "detalojn" (accusative)
- `demandon` - should be "demando" (nominative, not accusative)
- `vortoj` - should be "vortojn" (accusative)
- `↓` markers - indicate word order or case issues

**Compound word issues:**
- `video-konfero` - split into `*video-#konferenci` (both parts unknown, incorrect form)
- `Ido-renkontro` - split into `@Id-#renkonti` (incorrect form)
- `google-grupo` - split into `*google-#grupo` (both parts unknown)

**Tense issues:**
- `partoprenas` (present) vs `partoprenis` (past) - Wrong tense
- `diskutas` (present) vs `diskutis` (past) - Wrong tense

---

## Summary Statistics

### Sentence 1
- **Total words:** ~85 words
- **Unknown words:** ~35 words (41%)
- **Translation rule errors:** ~10 instances (12%)
- **Grammar errors:** ~15 instances (18%)
- **Overall error rate:** ~71%

### Sentence 2
- **Total words:** ~35 words
- **Unknown words:** ~15 words (43%)
- **Translation rule errors:** ~8 instances (23%)
- **Grammar errors:** ~10 instances (29%)
- **Overall error rate:** ~95%

---

## Error Symbols Legend

- `*word` - Unknown word (morphological analysis failure)
- `@word` - Proper noun handling issue
- `#word` - Translation rule issue or incorrect analysis
- `↓` - Word order or case issue
- `(indikante aganton)` - Disambiguation hint

---

## Notes

These translations demonstrate the current state of the Ido-Esperanto translation system. The high error rate is primarily due to:

1. **Missing dictionary entries** - Many common words not in monodix
2. **Missing morphological paradigms** - Words without paradigms are skipped
3. **Translation rule issues** - Incorrect handling of function words and grammar
4. **Compound word handling** - Hyphenated compounds split incorrectly

See `ERROR_ANALYSIS.md` for detailed error breakdown and `FUNCTION_WORDS_PIPELINE_ISSUE.md` for pipeline issues.

