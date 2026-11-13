import os
import re
import unicodedata
from urllib.parse import unquote

MONTH_MAP = {
    'jan': '01', 'january': '01', '1': '01', '01': '01',
    'feb': '02', 'february': '02', '2': '02', '02': '02',
    'mar': '03', 'march': '03', '3': '03', '03': '03',
    'apr': '04', 'april': '04', '4': '04', '04': '04',
    'may': '05', '5': '05', '05': '05',
    'jun': '06', 'june': '06', '6': '06', '06': '06',
    'jul': '07', 'july': '07', '7': '07', '07': '07',
    'aug': '08', 'august': '08', '8': '08', '08': '08',
    'sep': '09', 'sept': '09', 'september': '09', '9': '09', '09': '09',
    'oct': '10', 'october': '10', '10': '10',
    'nov': '11', 'november': '11', '11': '11',
    'dec': '12', 'december': '12', '12': '12',
}


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    if not value:
        return ""
    # Replace special math symbols before ascii normalization so slugs stay recognizable
    value = str(value).replace('H∞', 'h_nfty').replace('H_ınfty', 'h_nfty').replace('H₂', 'h2')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def clean_text(text):
    if not text:
        return ''
    # Convert common LaTeX math/accents before stripping braces
    text = text.replace(r'\_\infty', '∞').replace(r'_\infty', '∞').replace('H\\_ınfty', 'H∞').replace('H_ınfty', 'H∞')
    text = text.replace('{', '').replace('}', '').replace('\\', '')
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('"', '\\"')
    return text


def format_authors(author_field):
    if not author_field:
        return ''
    authors = clean_text(author_field).split(' and ')
    formatted_authors = []
    for author in authors:
        if 'Fuentes' in author:
            formatted_authors.append(f'<strong>{author.strip()}</strong>')
        else:
            formatted_authors.append(author.strip())
    if len(formatted_authors) > 1:
        return ', '.join(formatted_authors[:-1]) + ', & ' + formatted_authors[-1]
    return ''.join(formatted_authors)


def parse_bibtex_fallback(bib_text):
    """Lightweight BibTeX parser fallback in case bibtexparser is not installed."""
    entries = []
    pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}', re.DOTALL)
    field_pattern = re.compile(r'(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|(\w+))', re.DOTALL)
    for match in pattern.finditer(bib_text):
        entry_type, entry_id, body = match.groups()
        entry = {'ENTRYTYPE': entry_type.strip(), 'ID': entry_id.strip()}
        for fmatch in field_pattern.finditer(body):
            key = fmatch.group(1).lower().strip()
            val = fmatch.group(2) if fmatch.group(2) is not None else fmatch.group(3)
            entry[key] = val.strip()
        entries.append(entry)
    return entries


def load_bib_entries(bib_file_path):
    try:
        import bibtexparser
        with open(bib_file_path, encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
            return bib_database.entries
    except ImportError:
        with open(bib_file_path, encoding='utf-8') as bibtex_file:
            return parse_bibtex_fallback(bibtex_file.read())


def normalize_doi_url(doi_raw, url_raw):
    doi = clean_text(doi_raw)
    url = unquote(clean_text(url_raw))
    if doi:
        doi = unquote(doi)
        doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi, flags=re.IGNORECASE)
        return f'https://doi.org/{doi}', doi
    if url:
        url = re.sub(r'^http://(dx\.)?doi\.org/', 'https://doi.org/', url, flags=re.IGNORECASE)
        doi_match = re.match(r'^https://doi\.org/(.+)$', url, flags=re.IGNORECASE)
        return url, (doi_match.group(1) if doi_match else '')
    return '', ''


def main():
    bib_file_path = 'files/RMFUENTES.bib'
    pub_dir = '_publications/'

    os.makedirs(pub_dir, exist_ok=True)

    if not os.path.exists(bib_file_path):
        print(f"Error: Could not find the file {bib_file_path}")
        return

    entries = load_bib_entries(bib_file_path)

    for entry in entries:
        title = clean_text(entry.get('title', 'Unknown Title'))
        year = clean_text(entry.get('year', '2023'))
        month_raw = clean_text(entry.get('month', '')).lower()
        month = MONTH_MAP.get(month_raw, '01')

        entry_type = entry.get('ENTRYTYPE', '').lower()
        journal_name = clean_text(entry.get('journal', ''))

        # Determine category and venue
        if entry_type == 'article' and 'unpublished' not in journal_name.lower():
            category = 'journals'
            venue = journal_name
        elif entry_type in ['inproceedings', 'conference', 'incollection']:
            category = 'conferences'
            venue = clean_text(entry.get('booktitle', ''))
        else:
            category = 'conferences'
            venue = journal_name or 'Unpublished manuscript / Under Review'

        # Process Authors
        authors_raw = entry.get('author', '')
        authors_formatted = format_authors(authors_raw)

        # Process URL / DOI and local PDF
        paperurl, doi_clean = normalize_doi_url(entry.get('doi', ''), entry.get('url', ''))
        pdfurl = clean_text(entry.get('pdf', ''))

        abstract = clean_text(entry.get('abstract', ''))
        excerpt = abstract[:220] + '...' if len(abstract) > 220 else abstract

        # Use YYYY-01-01 for filename stability, and YYYY-MM-01 for chronological sorting in front matter
        file_date_str = f"{year}-01-01"
        sort_date_str = f"{year}-{month}-01"

        first_author_lastname = 'unknown'
        if authors_raw:
            first_author_raw = authors_raw.split(' and ')[0].strip()
            if ',' in first_author_raw:
                first_author_lastname = first_author_raw.split(',')[0].strip()
            else:
                first_author_lastname = first_author_raw.split(' ')[-1].strip()

        author_slug = slugify(first_author_lastname)
        title_slug = slugify(title)
        if len(title_slug) > 50:
            title_slug = title_slug[:50].rstrip('-')

        file_identifier = f"{title_slug}-{author_slug}"

        # Build detailed citation with volume/number/pages/DOI when available
        volume = clean_text(entry.get('volume', ''))
        number = clean_text(entry.get('number', ''))
        pages = clean_text(entry.get('pages', '')).replace('--', '–')

        venue_details = f"<i>{venue}</i>"
        if volume and number:
            venue_details += f", {volume}({number})"
        elif volume:
            venue_details += f", {volume}"
        if pages:
            venue_details += f", {pages}"

        citation = f'{authors_formatted} ({year}). "{title}." {venue_details}.'

        lines = [
            "---",
            f'title: "{title}"',
            "collection: publications",
            f"category: {category}",
            f"permalink: /publication/{year}-{file_identifier}",
            f"excerpt: '{excerpt}'",
            f"date: {sort_date_str}",
            f"venue: '{venue}'",
        ]
        if paperurl:
            lines.append(f"paperurl: '{paperurl}'")
        if pdfurl:
            lines.append(f"pdfurl: '{pdfurl}'")
        if doi_clean:
            lines.append(f"doi: '{doi_clean}'")
        lines.append(f"citation: '{citation}'")
        lines.append("---")
        lines.append("")

        md_content = "\n".join(lines)
        file_name = f"{file_date_str}-{file_identifier}.md"
        file_path = os.path.join(pub_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Created/Updated: {file_name}")

    print(f"\nSuccessfully processed {len(entries)} publications from BibTeX!")


if __name__ == '__main__':
    main()
