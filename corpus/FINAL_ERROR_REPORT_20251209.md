# Translation Error Report - December 9, 2025

## Test Corpus: `ido-epo-test-sentences.txt`

### 1. Unknown Words (`*`)
These words are missing from the dictionary or failed analysis.

**High Frequency / Function Words:**
- `*maxim` (plej) - Superlative marker
- `*quin` (kiujn) - Relative pronoun (plural accusative)
- `*od` (aŭ) - Disjunction (appears as `@od`)
- `*por` (por) - Preposition (appears as `@por` in some contexts?)
- `*e` (kaj) - Conjunction (appears in output but often missed/misparsed)
- `*on` (oni) - Indefinite pronoun
- `*kom` (kiel) - Preposition/Adverb (appears as `#keom`)

**Verbs:**
- `*derivante` (derivate?) - Participle
- `*kreesis` (estis kreita/kreiĝis) - Passive past
- `*nomizas` (nomas)
- `*remplacigar` (anstataŭigi)

**Nouns/Adjectives:**
- `*saturdia` (sabata)
- `*facil` (facila/e) - Root used as adverb?
- `*lernebla` (lernebla) - Suffix -ebl not recognized
- `*uzebla` (uzebla) - Suffix -ebl not recognized
- `*polisemio` (polisemio)
- `*seucecoz` (sukcesa?)
- `*kajxistant` (ekzistantaj?)

**Proper Nouns:**
- `*Delegitaro`
- `*Délégation`, `*pour`, `*adoption`, etc. (French text)

### 2. Preposition/Particle Mapping Issues (`#`, `@`)
These words are being generated with debug markers, indicating probable transfer rule or dictionary issues.

- `#de` (da) - Used for agent in passive?
- `@de` (de) - Origin/possession
- `@di` (de) - Possession
- `#keom` (kom)
- `#jee` (je)
- `@ol` (ĝi)

### 3. Morphology & Syntax Errors
- `Reformita Esperanton` -> `Reformita Esperanto` (Nominative expected, got Accusative?)
- `video-konfero` -> `Video-#keonfer` (Compound word failure)
- `Ido-renkontr` (Truncated?)

### 4. Corrected Items (Verified)
- `partoprenis` -> `partoprenis` (Past tense maintained ✅)
- `diskutis` -> `diskutis` (Past tense maintained ✅)

