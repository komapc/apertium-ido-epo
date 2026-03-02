---
inclusion: always
---

## No Manual Dictionary Edits

CRITICAL: **NEVER add words manually to the dictionary files (`.dix`).**

All dictionary entries must be added through official pipelines, scripts, or automated tools to ensure data integrity and provenance. 

**Required Actions:**
- Use provided scripts for adding new entries.
- Follow the established data ingestion workflow.
- Do not use `sed`, `replace`, or manual text editing to insert words into `.dix` files.
- If a word is missing, identify the correct data source (e.g., Vortaro, Wiktionary) and use the appropriate tool to update the dictionary.

**Rationale:**
- Prevents syntax errors and schema violations.
- Maintains consistency between monolingual and bilingual dictionaries.
- Ensures all changes are traceable to a reliable linguistic source.
- Avoids duplication and technical debt.
