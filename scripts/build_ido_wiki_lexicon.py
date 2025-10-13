#!/usr/bin/env python3
"""
Build a word-frequency lexicon from the Ido Wikipedia dump.

Pipeline:
 1) Download latest pages-articles dump (iowiki)
 2) Extract plain text with WikiExtractor (templates, tables, blockquotes discarded)
 3) Remove quoted spans from extracted text
 4) Tokenize (Unicode-aware), exclude tokens with digits/URLs
 5) Count frequencies and write TSV sorted by count desc

Assumptions satisfied per user:
 - Ignore text in quotes and blockquotes
 - Ignore templates and tables
 - Use only pages namespace (the pages-articles dump is NS=0)
 - Tokenization: lowercase, NFC, keep letters and internal apostrophes/hyphens
 - Exclude numbers and URLs
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple

import bz2
import unicodedata
import requests
import mwxml  # type: ignore
import mwparserfromhell  # type: ignore


IOWIKI_LATEST_URL = (
    "https://dumps.wikimedia.org/iowiki/latest/iowiki-latest-pages-articles.xml.bz2"
)


@dataclass
class Paths:
    work_dir: Path
    dumps_dir: Path
    extract_dir: Path
    output_dir: Path


def ensure_dirs(base_dir: Path) -> Paths:
    dumps_dir = base_dir / "data" / "iowiki"
    extract_dir = base_dir / "data" / "iowiki_extracted"
    output_dir = base_dir / "outputs"
    dumps_dir.mkdir(parents=True, exist_ok=True)
    extract_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return Paths(base_dir, dumps_dir, extract_dir, output_dir)


def download_dump(url: str, dest_path: Path, timeout: int = 60) -> None:
    """Download the dump file if not present (simple streaming download)."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"Dump already present: {dest_path}")
        return
    print(f"Downloading dump: {url}")
    headers = {"User-Agent": "IdoLexiconBuilder/1.0 (github.com/komapc)"}
    with requests.get(url, stream=True, timeout=timeout, headers=headers) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
    print(f"Downloaded to: {dest_path}")


def run_wikiextractor(dump_path: Path, extract_dir: Path, processes: int = 4) -> None:
    """Run WikiExtractor to extract plain text JSON, discarding templates, tables, blockquotes."""
    if any(extract_dir.iterdir()):
        print(f"Extraction directory not empty, skipping WikiExtractor: {extract_dir}")
        return
    print("Running WikiExtractor...")
    # Using module form to avoid PATH assumptions
    cmd = [
        sys.executable,
        "-m",
        "wikiextractor.WikiExtractor",
        str(dump_path),
        "--json",
        "-o",
        str(extract_dir),
        "--no_templates",
        "--discardElements",
        "table,blockquote",
        "--processes",
        str(processes),
    ]
    subprocess.run(cmd, check=True)
    print("WikiExtractor finished.")


def remove_nested_sections(text: str, open_seq: str, close_seq: str) -> str:
    """Remove nested sections delimited by open_seq/close_seq from text."""
    out: List[str] = []
    i = 0
    depth = 0
    n = len(text)
    ol = len(open_seq)
    cl = len(close_seq)
    while i < n:
        if depth == 0 and text.startswith(open_seq, i):
            depth = 1
            i += ol
            continue
        if depth > 0:
            if text.startswith(open_seq, i):
                depth += 1
                i += ol
                continue
            if text.startswith(close_seq, i):
                depth -= 1
                i += cl
                continue
            i += 1
            continue
        # depth == 0 and not opening
        out.append(text[i])
        i += 1
    return "".join(out)


def strip_block_tags(text: str, tag: str) -> str:
    """Remove <tag>...</tag> blocks entirely (DOTALL, nested tags removed greedily)."""
    pattern = re.compile(rf"<\s*{tag}[^>]*>.*?<\s*/\s*{tag}\s*>", re.IGNORECASE | re.DOTALL)
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub("", text)
    return text


def clean_wikitext(text: str) -> str:
    """Remove templates, tables, blockquotes, then strip remaining markup to plain text."""
    # Remove HTML blockquote and table tags entirely
    text = strip_block_tags(text, "blockquote")
    text = strip_block_tags(text, "table")
    # Remove wikitext tables and templates (with nesting): {| ... |}, {{ ... }}
    text = remove_nested_sections(text, "{|", "|}")
    text = remove_nested_sections(text, "{{", "}}")
    # Strip remaining markup using mwparserfromhell
    code = mwparserfromhell.parse(text)
    plain = code.strip_code(normalize=True, collapse=True)
    return plain


def fallback_extract_dump_to_json(dump_path: Path, extract_dir: Path) -> None:
    """Fallback extractor: iterate dump with mwxml and produce JSONL article texts."""
    if any(extract_dir.iterdir()):
        print(f"Extraction directory not empty, skipping fallback extract: {extract_dir}")
        return
    print("Running fallback extractor (mwxml + mwparserfromhell)...")
    extract_dir.mkdir(parents=True, exist_ok=True)
    out_file = extract_dir / "extracted.json"
    articles = 0
    with bz2.open(dump_path, "rb") as f, open(out_file, "w", encoding="utf-8") as out:
        dump = mwxml.Dump.from_file(f)
        for page in dump:
            # Only main namespace (0)
            try:
                if getattr(page, "namespace", 0) != 0:
                    continue
            except Exception:
                continue
            latest_text: Optional[str] = None
            for rev in page:
                latest_text = getattr(rev, "text", None) or latest_text
            if not latest_text:
                continue
            cleaned = clean_wikitext(latest_text)
            if not cleaned.strip():
                continue
            obj = {
                "id": getattr(page, "id", None),
                "title": getattr(page, "title", None),
                "text": cleaned,
            }
            out.write(json.dumps(obj, ensure_ascii=False) + "\n")
            articles += 1
            if articles % 500 == 0:
                print(f"  Extracted articles: {articles:,}")
    print(f"Fallback extraction finished. Articles: {articles:,}")


QUOTE_PAIRS: List[Tuple[str, str]] = [
    ("\"", "\""),  # ASCII double quotes
    ("'", "'"),       # ASCII single quotes
    ("“", "”"),       # English curly double quotes
    ("‘", "’"),       # English curly single quotes
    ("«", "»"),       # Angle quotes
]


def remove_quoted_spans(text: str) -> str:
    """Remove text enclosed by any configured quote pairs (non-nested, greedy by pair)."""
    # We operate line-wise to avoid eating huge multi-line spans on unmatched quotes
    # while still removing multi-quote spans within a line.
    lines = text.splitlines()
    cleaned_lines: List[str] = []
    for line in lines:
        line_out = line
        for left, right in QUOTE_PAIRS:
            start = 0
            result_fragments: List[str] = []
            while True:
                i = line_out.find(left, start)
                if i == -1:
                    result_fragments.append(line_out[start:])
                    break
                j = line_out.find(right, i + len(left))
                if j == -1:
                    # No closing quote: keep remainder
                    result_fragments.append(line_out[start:])
                    break
                # Keep text before the quote, skip the quoted part
                result_fragments.append(line_out[start:i])
                start = j + len(right)
            line_out = "".join(result_fragments)
        cleaned_lines.append(line_out)
    return "\n".join(cleaned_lines)


def is_letter(ch: str) -> bool:
    # Unicode-aware letter detection
    return ch.isalpha()


def tokenize(text: str) -> Iterator[str]:
    """Yield tokens: letters only, keep internal apostrophes/hyphens, lowercase, NFC."""
    text = unicodedata.normalize("NFC", text).lower()
    token_chars: List[str] = []

    def flush_token():
        if not token_chars:
            return None
        token = "".join(token_chars)
        token_chars.clear()
        return token

    for ch in text:
        if is_letter(ch):
            token_chars.append(ch)
            continue
        if ch in {"'", "-"}:
            # Allow apostrophes/hyphens only if surrounded by letters (internal)
            if token_chars and token_chars[-1].isalpha():
                token_chars.append(ch)
                continue
        # Separator encountered
        token = flush_token()
        if token:
            yield token
    token = flush_token()
    if token:
        yield token


def is_excluded_token(token: str) -> bool:
    # Exclude tokens containing digits
    if any(c.isdigit() for c in token):
        return True
    # Exclude URL-like tokens
    if "http" in token or "www" in token or "/" in token or "." in token:
        return True
    return False


def iter_extracted_texts(extract_dir: Path) -> Iterator[str]:
    """Iterate over extracted JSON files from WikiExtractor, yielding article texts."""
    for root, _dirs, files in os.walk(extract_dir):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            fpath = Path(root) / fname
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        text = obj.get("text", "")
                        if text:
                            yield text
                    except json.JSONDecodeError:
                        continue


def build_frequency(paths: Paths, min_count: int = 1) -> Path:
    """Build word frequency TSV from extracted texts. Returns path to TSV."""
    counter: Counter[str] = Counter()
    total_articles = 0
    total_tokens = 0
    print("Processing extracted texts and counting tokens...")
    for total_articles, text in enumerate(iter_extracted_texts(paths.extract_dir), start=1):
        text = remove_quoted_spans(text)
        for tok in tokenize(text):
            if is_excluded_token(tok):
                continue
            counter[tok] += 1
            total_tokens += 1
        if total_articles % 500 == 0:
            print(f"  Articles processed: {total_articles:,} | Unique tokens: {len(counter):,} | Tokens: {total_tokens:,}")

    print(f"Done. Articles: {total_articles:,}, Unique tokens: {len(counter):,}, Tokens: {total_tokens:,}")

    out_path = paths.output_dir / "iowiki_word_frequency.tsv"
    print(f"Writing TSV to: {out_path}")
    with open(out_path, "w", encoding="utf-8") as out:
        # Sort by count desc, then token asc for determinism
        for token, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
            if count < min_count:
                continue
            out.write(f"{token}\t{count}\n")
    return out_path


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build Ido Wikipedia lexicon (word frequency)")
    parser.add_argument("--base-dir", type=str, default=str(Path(__file__).resolve().parents[1]), help="Base working directory (default: repo root)")
    parser.add_argument("--dump-url", type=str, default=IOWIKI_LATEST_URL, help="Dump URL; default latest iowiki pages-articles")
    parser.add_argument("--processes", type=int, default=4, help="Parallel processes for WikiExtractor")
    parser.add_argument("--min-count", type=int, default=1, help="Minimum frequency to include in TSV")
    args = parser.parse_args(argv)

    base_dir = Path(args.base_dir)
    paths = ensure_dirs(base_dir)

    dump_path = paths.dumps_dir / Path(args.dump_url).name
    download_dump(args.dump_url, dump_path)
    try:
        run_wikiextractor(dump_path, paths.extract_dir, processes=args.processes)
    except Exception:
        print("WikiExtractor failed, falling back to mwxml-based extractor...", file=sys.stderr)
        # Clear extraction dir if partially created by failed run
        for p in paths.extract_dir.glob("*"):
            if p.is_file():
                p.unlink()
        fallback_extract_dump_to_json(dump_path, paths.extract_dir)

    tsv_path = build_frequency(paths, min_count=args.min_count)
    print(f"Frequency file created: {tsv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



