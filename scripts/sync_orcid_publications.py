#!/usr/bin/env python3
"""
Synchronize publications from ORCID (and Crossref/DOI metadata) into files/RMFUENTES.bib,
then regenerate _publications/*.md and _data/cv.json.

Usage:
    python3 scripts/sync_orcid_publications.py
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from update_publications import clean_text, load_bib_entries, normalize_doi_url, slugify

ORCID_ID_DEFAULT = "0000-0002-1310-9780"
BIB_FILE_PATH = "files/RMFUENTES.bib"


def get_orcid_from_config(config_path="_config.yml"):
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"orcid\s*:\s*[\"']?https?://orcid\.org/([\d-]+X?)[\"']?", content, re.I)
        if match:
            return match.group(1).strip()
    return ORCID_ID_DEFAULT


def http_get_json(url, headers=None):
    req_headers = {"User-Agent": "fuentes-rm.github.io-sync/1.0 (mailto:rfuentesalbornoz@gmail.com)"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_bibtex_from_doi(doi):
    """Fetch standard BibTeX entry for a DOI via Crossref / doi.org content negotiation."""
    url = f"https://doi.org/{urllib.parse.quote(doi, safe='/')}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/x-bibtex; charset=utf-8",
            "User-Agent": "fuentes-rm.github.io-sync/1.0 (mailto:rfuentesalbornoz@gmail.com)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            bib = resp.read().decode("utf-8").strip()
            if bib.startswith("@"):
                return bib
    except Exception as exc:
        print(f"  [warn] Could not fetch BibTeX from doi.org for {doi}: {exc}")
    return None


def extract_doi_from_external_ids(ext_ids_obj):
    if not ext_ids_obj:
        return ""
    for ext in ext_ids_obj.get("external-id", []):
        if (ext.get("external-id-type") or "").lower() == "doi":
            val = (ext.get("external-id-value") or "").strip()
            val = re.sub(r"^https?://(dx\.)?doi\.org/", "", val, flags=re.I)
            return val
    return ""


def build_bibtex_from_orcid_work(work_detail, doi):
    """Fallback builder if DOI content negotiation is unavailable and ORCID has no raw bibtex."""
    citation = work_detail.get("citation") or {}
    if (citation.get("citation-type") or "").lower() == "bibtex" and citation.get("citation-value"):
        return citation["citation-value"].strip()

    title_obj = (work_detail.get("title") or {}).get("title") or {}
    title = title_obj.get("value") or "Untitled"

    pub_date = work_detail.get("publication-date") or {}
    year = ((pub_date.get("year") or {}).get("value")) or "2026"

    journal_obj = work_detail.get("journal-title") or {}
    venue = journal_obj.get("value") or ""

    work_type = (work_detail.get("type") or "").lower()
    if "conference" in work_type or "proceeding" in work_type:
        entry_type = "inproceedings"
        venue_field = f"\tbooktitle = {{{venue}}}," if venue else ""
    else:
        entry_type = "article"
        venue_field = f"\tjournal = {{{venue}}}," if venue else ""

    contributors = ((work_detail.get("contributors") or {}).get("contributor")) or []
    authors = []
    for c in contributors:
        credit_name = ((c.get("credit-name") or {}).get("value")) or ""
        if credit_name:
            authors.append(credit_name.strip())
    if not authors:
        authors = ["Fuentes, Roberto M."]
    author_str = " and ".join(authors)

    slug = slugify(title)[:20].replace("-", "_")
    cite_key = f"fuentes_{slug}_{year}"
    doi_field = f"\tdoi = {{{doi}}},\n\turl = {{https://doi.org/{doi}}},\n" if doi else ""

    lines = [
        f"@{entry_type}{{{cite_key},",
        f"\ttitle = {{{title}}},",
        f"\tauthor = {{{author_str}}},",
    ]
    if venue_field:
        lines.append(venue_field)
    lines.append(f"\tyear = {{{year}}},")
    if doi_field:
        lines.append(doi_field.rstrip("\n"))
    lines.append("}")
    return "\n".join(lines)


def sync_orcid(orcid_id):
    print(f"Checking ORCID profile: {orcid_id} ...")
    existing_entries = load_bib_entries(BIB_FILE_PATH) if os.path.exists(BIB_FILE_PATH) else []

    existing_dois = set()
    existing_title_slugs = set()
    for entry in existing_entries:
        _, doi_clean = normalize_doi_url(entry.get("doi", ""), entry.get("url", ""))
        if doi_clean:
            existing_dois.add(doi_clean.lower())
        t_slug = slugify(clean_text(entry.get("title", "")))
        if t_slug:
            existing_title_slugs.add(t_slug[:45])

    works_url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    try:
        record = http_get_json(works_url, headers={"Accept": "application/orcid+json"})
    except urllib.error.URLError as exc:
        print(f"Error connecting to ORCID API: {exc}")
        return 0

    new_bibtex_blocks = []
    groups = record.get("group", [])
    print(f"Found {len(groups)} work group(s) on ORCID.")

    for group in groups:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]
        put_code = summary.get("put-code")
        title_val = (((summary.get("title") or {}).get("title") or {}).get("value")) or ""
        t_slug = slugify(clean_text(title_val))[:45]

        pub_date = summary.get("publication-date") or {}
        pub_year_str = ((pub_date.get("year") or {}).get("value")) or ""
        try:
            if pub_year_str and int(pub_year_str) < 2021:
                continue
        except ValueError:
            pass

        doi = extract_doi_from_external_ids(group.get("external-ids")) or extract_doi_from_external_ids(
            summary.get("external-ids")
        )

        if (doi and doi.lower() in existing_dois) or (t_slug and t_slug in existing_title_slugs):
            continue

        print(f"  + New work detected on ORCID: '{title_val}' (DOI: {doi or 'none'})")
        bib_block = None
        if doi:
            bib_block = fetch_bibtex_from_doi(doi)

        if not bib_block and put_code:
            try:
                work_detail = http_get_json(
                    f"https://pub.orcid.org/v3.0/{orcid_id}/work/{put_code}",
                    headers={"Accept": "application/orcid+json"},
                )
                bib_block = build_bibtex_from_orcid_work(work_detail, doi)
            except Exception as exc:
                print(f"  [warn] Failed to fetch ORCID work {put_code}: {exc}")

        if bib_block:
            new_bibtex_blocks.append(bib_block)
            if doi:
                existing_dois.add(doi.lower())
            if t_slug:
                existing_title_slugs.add(t_slug)

    if new_bibtex_blocks:
        with open(BIB_FILE_PATH, "a", encoding="utf-8") as f:
            f.write("\n\n" + "\n\n".join(new_bibtex_blocks) + "\n")
        print(f"Added {len(new_bibtex_blocks)} new BibTeX entry/entries to {BIB_FILE_PATH}.")
    else:
        print("No new publications to add from ORCID.")

    return len(new_bibtex_blocks)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    orcid_id = sys.argv[1] if len(sys.argv) > 1 else get_orcid_from_config()
    if "--bib-only" not in sys.argv:
        sync_orcid(orcid_id)

    # Always regenerate _publications/*.md and _data/cv.json
    subprocess.run([sys.executable, "scripts/update_publications.py"], check=True)
    subprocess.run(
        [
            sys.executable,
            "scripts/cv_markdown_to_json.py",
            "--input",
            "_pages/cv.md",
            "--output",
            "_data/cv.json",
            "--config",
            "_config.yml",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
