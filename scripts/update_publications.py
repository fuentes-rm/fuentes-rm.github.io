import os
import re
import bibtexparser
import unicodedata

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    if not value:
        return ""
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def clean_text(text):
    if not text:
        return ''
    # Remove bibtex curly braces and escape characters
    text = text.replace('{', '').replace('}', '').replace('\\', '')
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Escape quotes if necessary
    text = text.replace('"', '\\"')
    return text

def format_authors(author_field):
    if not author_field:
        return ''
    # Authors in bibtex are usually separated by ' and '
    authors = clean_text(author_field).split(' and ')
    formatted_authors = []
    for author in authors:
        # Highlight the author Roberto Fuentes
        if 'Fuentes' in author:
            formatted_authors.append(f'<strong>{author.strip()}</strong>')
        else:
            formatted_authors.append(author.strip())
    # Join authors up properly
    if len(formatted_authors) > 1:
        return ', '.join(formatted_authors[:-1]) + ', & ' + formatted_authors[-1]
    return ''.join(formatted_authors)

def main():
    bib_file_path = 'files/RMFUENTES.bib'
    pub_dir = '_publications/'

    # Ensure the publications directory exists
    os.makedirs(pub_dir, exist_ok=True)

    try:
        with open(bib_file_path, encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    except FileNotFoundError:
        print(f"Error: Could not find the file {bib_file_path}")
        return
    except ImportError:
        print("Error: bibtexparser module not found. Please install it using: pip install bibtexparser")
        return

    for entry in bib_database.entries:
        pub_id = entry.get('ID', 'unknown_id')
        title = clean_text(entry.get('title', 'Unknown Title'))
        year = clean_text(entry.get('year', '202X'))
        
        entry_type = entry.get('ENTRYTYPE', '').lower()
        
        # Determine category and venue
        if entry_type == 'article':
            category = 'journals'
            venue = clean_text(entry.get('journal', ''))
        elif entry_type in ['inproceedings', 'conference']:
            category = 'conferences'
            venue = clean_text(entry.get('booktitle', ''))
        elif entry_type == 'incollection':
            category = 'conferences'
            venue = clean_text(entry.get('booktitle', ''))
        else:
            category = 'manuscripts'
            venue = clean_text(entry.get('journal', 'Unpublished manuscript / Under Review'))

        # Process Authors
        authors_raw = entry.get('author', '')
        authors_formatted = format_authors(authors_raw)
        
        # Process URL / DOI
        paperurl = clean_text(entry.get('url', ''))
        if not paperurl:
            doi = clean_text(entry.get('doi', ''))
            if doi:
                # Ensure no HTTP prefix in doi if the raw value didn't have it
                if not doi.startswith('http'):
                    paperurl = f'https://doi.org/{doi}'
                else:
                    paperurl = doi
        if not paperurl:
            paperurl = '#'
            
        abstract = clean_text(entry.get('abstract', ''))
        excerpt = abstract[:200] + '...' if len(abstract) > 200 else abstract
        
        # Make a standard date
        # Some entries have a month, but defaulting to Jan 1st is typical if exact date is not crucial for display
        date_str = f"{year}-01-01"
        
        # Clean ID for the permalink and filename
        # Extract first author's last name
        first_author_lastname = 'unknown'
        if authors_raw:
            first_author_raw = authors_raw.split(' and ')[0].strip()
            # Handle forms like "Lastname, Firstname" or "Firstname Lastname"
            if ',' in first_author_raw:
                first_author_lastname = first_author_raw.split(',')[0].strip()
            else:
                first_author_lastname = first_author_raw.split(' ')[-1].strip()
        
        author_slug = slugify(first_author_lastname)
        
        # Format title up to 50 characters
        title_slug = slugify(title)
        if len(title_slug) > 50:
            # Cut at 50 chars but try not to end with a hyphen
            title_slug = title_slug[:50].rstrip('-')
        
        # Construct the new filename identifier
        # Format requested: AAAA-(50 primero caracteres del titulo)-AUTHOR
        # We prepend mm-dd (01-01) for Jekyll compatibility
        file_identifier = f"{title_slug}-{author_slug}"
        
        # Build the Markdown Content
        md_content = f"""---
title: "{title}"
collection: publications
category: {category}
permalink: /publication/{year}-{file_identifier}
excerpt: '{excerpt}'
date: {date_str}
venue: '{venue}'
paperurl: '{paperurl}'
citation: '{authors_formatted} ({year}). "{title}." <i>{venue}</i>.'
---
"""
        # Save the file
        file_name = f"{date_str}-{file_identifier}.md"
        file_path = os.path.join(pub_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Created/Updated: {file_name}")

    print(f"\\nSuccessfully processed {len(bib_database.entries)} publications from BibTeX!")

if __name__ == '__main__':
    main()
