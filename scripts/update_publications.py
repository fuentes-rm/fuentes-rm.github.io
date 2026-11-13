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
    value = str(value).replace('H∞', 'h_nfty').replace('H_ınfty', 'h_nfty').replace('H₂', 'h2')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def clean_text(text):
    if not text:
        return ''
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
    """Brace-balanced BibTeX parser that handles both multi-line and single-line BibTeX entries."""
    entries = []
    pos = 0
    n = len(bib_text)
    header_re = re.compile(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', re.DOTALL)
    field_re = re.compile(r'(\w+)\s*=\s*', re.DOTALL)

    while pos < n:
        m = header_re.search(bib_text, pos)
        if not m:
            break
        entry_type, entry_id = m.group(1).strip(), m.group(2).strip()
        # Find matching closing brace for the @entry{ ... }
        idx = m.end()
        depth = 1
        while idx < n and depth > 0:
            if bib_text[idx] == '{':
                depth += 1
            elif bib_text[idx] == '}':
                depth -= 1
            idx += 1
        body = bib_text[m.end():idx - 1]
        pos = idx

        entry = {'ENTRYTYPE': entry_type, 'ID': entry_id}
        fpos = 0
        bn = len(body)
        while fpos < bn:
            fm = field_re.search(body, fpos)
            if not fm:
                break
            key = fm.group(1).lower().strip()
            vstart = fm.end()
            while vstart < bn and body[vstart].isspace():
                vstart += 1
            if vstart >= bn:
                break
            if body[vstart] == '{':
                vdepth = 1
                vidx = vstart + 1
                while vidx < bn and vdepth > 0:
                    if body[vidx] == '{':
                        vdepth += 1
                    elif body[vidx] == '}':
                        vdepth -= 1
                    vidx += 1
                val = body[vstart + 1:vidx - 1].strip()
                fpos = vidx
            elif body[vstart] == '"':
                vidx = vstart + 1
                while vidx < bn and body[vidx] != '"':
                    if body[vidx] == '\\':
                        vidx += 1
                    vidx += 1
                val = body[vstart + 1:vidx].strip()
                fpos = vidx + 1
            else:
                vidx = vstart
                while vidx < bn and body[vidx] not in ',\n\r}':
                    vidx += 1
                val = body[vstart:vidx].strip()
                fpos = vidx
            entry[key] = val
        entries.append(entry)
    return entries


def load_bib_entries(bib_file_path):
    try:
        import bibtexparser
        if hasattr(bibtexparser, 'load'):
            with open(bib_file_path, encoding='utf-8') as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                return bib_database.entries
    except (ImportError, AttributeError, Exception):
        pass
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


def infer_topic(title, venue):
    text = f"{title} {venue}".lower()
    if any(k in text for k in ['sampled-data', 'dlmi', 'packet']):
        return 'sampled-data'
    if any(k in text for k in ['gain-schedul', 'lpv', 'd-stability', 'metaheuristic', 'lqr']):
        return 'gain-scheduling'
    if any(k in text for k in ['solar', 'photovoltaic', 'mppt', 'agrifood', 'greenhouse']):
        return 'solar-energy'
    return 'control-applications'


def build_clean_bibtex(entry, entry_type, title, venue, year, doi_clean):
    cite_id = entry.get('ID', f"fuentes_{year}")
    authors_raw = clean_text(entry.get('author', '')).replace('\\"', '"')
    clean_title = title.replace('\\"', '"')
    clean_venue = venue.replace('\\"', '"')
    lines = [f"@{entry_type}{{{cite_id},"]
    lines.append(f"  author = {{{authors_raw}}},")
    lines.append(f"  title = {{{clean_title}}},")
    if entry_type == 'article':
        lines.append(f"  journal = {{{clean_venue}}},")
    else:
        lines.append(f"  booktitle = {{{clean_venue}}},")
    if entry.get('volume'):
        lines.append(f"  volume = {{{clean_text(entry.get('volume'))}}},")
    if entry.get('number'):
        lines.append(f"  number = {{{clean_text(entry.get('number'))}}},")
    if entry.get('pages'):
        lines.append(f"  pages = {{{clean_text(entry.get('pages'))}}},")
    lines.append(f"  year = {{{year}}},")
    if doi_clean:
        lines.append(f"  doi = {{{doi_clean}}}")
    lines.append("}")
    return "\n".join(lines)


def yaml_single_quote(val):
    return "'" + str(val).replace("'", "''") + "'"


def main():
    bib_file_path = 'files/RMFUENTES.bib'
    pub_dir = '_publications/'

    os.makedirs(pub_dir, exist_ok=True)

    if not os.path.exists(bib_file_path):
        print(f"Error: Could not find the file {bib_file_path}")
        return

    entries = load_bib_entries(bib_file_path)
    generated_files = set()

    for entry in entries:
        title = clean_text(entry.get('title', 'Unknown Title'))
        year = clean_text(entry.get('year', '2023'))
        month_raw = clean_text(entry.get('month', '')).lower()
        month = MONTH_MAP.get(month_raw, '01')

        entry_type = entry.get('ENTRYTYPE', '').lower()
        journal_name = clean_text(entry.get('journal', ''))

        if entry_type == 'article' and 'unpublished' not in journal_name.lower():
            category = 'journals'
            venue = journal_name
        elif entry_type in ['inproceedings', 'conference', 'incollection']:
            category = 'conferences'
            venue = clean_text(entry.get('booktitle', ''))
        else:
            category = 'conferences'
            venue = journal_name or 'Unpublished manuscript / Under Review'

        authors_raw = entry.get('author', '')
        authors_formatted = format_authors(authors_raw)
        authors_list = [a.strip().replace('\\"', '"') for a in clean_text(authors_raw).split(' and ') if a.strip()]

        paperurl, doi_clean = normalize_doi_url(entry.get('doi', ''), entry.get('url', ''))
        pdfurl = clean_text(entry.get('pdf', ''))

        abstract = clean_text(entry.get('abstract', '')).replace('\\"', '"')
        excerpt = abstract[:220] + '...' if len(abstract) > 220 else abstract

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
        topic = infer_topic(title, venue)
        bibtex_str = build_clean_bibtex(entry, entry_type, title, venue, year, doi_clean)

        lines = [
            "---",
            f'title: "{title}"',
            "collection: publications",
            f"category: {category}",
            f"topic: {topic}",
            f"permalink: /publication/{year}-{file_identifier}",
            f"excerpt: {yaml_single_quote(excerpt)}",
            f"abstract: {yaml_single_quote(abstract)}",
            f"date: {sort_date_str}",
            f"venue: {yaml_single_quote(venue)}",
        ]
        if paperurl:
            lines.append(f"paperurl: {yaml_single_quote(paperurl)}")
        if pdfurl:
            lines.append(f"pdfurl: {yaml_single_quote(pdfurl)}")
        if doi_clean:
            lines.append(f"doi: {yaml_single_quote(doi_clean)}")
        if authors_list:
            lines.append("authors:")
            for auth in authors_list:
                lines.append(f"  - {yaml_single_quote(auth)}")
        lines.append(f"citation: {yaml_single_quote(citation)}")
        lines.append("bibtex: |")
        for bline in bibtex_str.splitlines():
            lines.append(f"  {bline}")
        lines.append("---")
        lines.append("")
        if abstract:
            lines.append("## Abstract")
            lines.append("")
            lines.append(abstract)
            lines.append("")

        md_content = "\n".join(lines)
        file_name = f"{file_date_str}-{file_identifier}.md"
        file_path = os.path.join(pub_dir, file_name)
        generated_files.add(file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Created/Updated: {file_name}")

    for existing_file in os.listdir(pub_dir):
        if existing_file.endswith('.md') and existing_file not in generated_files:
            os.remove(os.path.join(pub_dir, existing_file))
            print(f"Removed stale publication file: {existing_file}")

    print(f"\nSuccessfully processed {len(entries)} publications from BibTeX!")


if __name__ == '__main__':
    main()
