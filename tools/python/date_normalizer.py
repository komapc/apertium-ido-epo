#!/usr/bin/env python3
"""
Library for normalizing Ido date/ordinal patterns and cleaning generated
Esperanto numeric tokens. No CLI entrypoints here; import the functions
directly or reuse inside analysis scripts.
"""

import sys
import re

MONTH_MAP_IDO_TO_EO = {
    'januaro': 'januaro',
    'februaro': 'februaro',
    'marzo': 'marto',
    'marte': 'marto',  # occasional alt
    'abril': 'aprilo',
    'aprile': 'aprilo',
    'mayo': 'majo',
    'majo': 'majo',
    'junio': 'junio',
    'julio': 'julio',
    'agosto': 'aŭgusto',
    'aguste': 'aŭgusto',
    'septembro': 'septembro',
    'oktobro': 'oktobro',
    'novembro': 'novembro',
    'decembro': 'decembro',
}

def normalize_ido_dates_line(text: str) -> str:
    s = text

    # Ordinals: 1ma..31ma → 1-a..31-a
    s = re.sub(r"\b([1-9]|[12][0-9]|3[01])ma\b", r"\1-a", s)
    # Also handle hyphenated ordinals 1-ma → 1-a
    s = re.sub(r"\b([1-9]|[12][0-9]|3[01])-ma\b", r"\1-a", s)

    # Replace ' di ' with ' de ' when preceded by a day ordinal
    s = re.sub(r"\b(\d{1,2}-?a)\s+di\b", r"\1 de", s)

    # Month mapping (case-insensitive)
    def repl_month(m: re.Match) -> str:
        src = m.group(0)
        key = src.lower()
        eo = MONTH_MAP_IDO_TO_EO.get(key, src)
        # preserve capitalization of first letter
        return eo.capitalize() if src[0].isupper() else eo

    month_re = r"\b(" + "|".join(map(re.escape, MONTH_MAP_IDO_TO_EO.keys())) + r")\b"
    s = re.sub(month_re, repl_month, s, flags=re.IGNORECASE)

    # yarcento → jarcento; 17ma yarcento → 17-a jarcento
    s = re.sub(r"\byarcento\b", "jarcento", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(\d{1,2})-?ma\s+jarcento\b", r"\1-a jarcento", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(\d{1,2})-?ma\s+yarcento\b", r"\1-a jarcento", s, flags=re.IGNORECASE)

    # 35-yara → 35-jara, yara → jara
    s = re.sub(r"\b(\d+)-yara\b", r"\1-jara", s)
    s = re.sub(r"\byara\b", "jara", s, flags=re.IGNORECASE)

    return s

def normalize_esperanto_numbers_line(text: str) -> str:
    s = text
    # Remove leading '*' before years and ordinals
    s = re.sub(r"\*(\d{3,4})\b", r"\1", s)          # *1806 → 1806
    s = re.sub(r"\*(\d{1,2}-a)\b", r"\1", s)        # *26-a → 26-a
    s = re.sub(r"\*(\d{1,3}-jara)\b", r"\1", s)     # *35-jara → 35-jara
    s = re.sub(r"\*(\d{1,2})\b", r"\1", s)          # stray *12 → 12
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

# Intentionally no __main__ to avoid CLI usage in this repository


