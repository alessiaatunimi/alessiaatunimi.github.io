"""Import the single BibTeX source into Hugo data; never edit generated JSON."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote, urlsplit

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import latex_to_unicode

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'bibliography/publications.bib'
AREAS = {
    'networks': 'Temporal & multilayer networks',
    'social': 'Computational social science',
    'learning': 'Machine learning on graphs',
}


def plain(value):
    return re.sub(r'\s+', ' ', latex_to_unicode(value)).strip()


def author_names(value):
    names = []
    for author in re.split(r'\s+and\s+', value):
        parts = [plain(part) for part in author.split(',')]
        if len(parts) == 2:
            names.append(f'{parts[1]} {parts[0]}')
        elif len(parts) == 3:
            names.append(f'{parts[2]} {parts[0]}, {parts[1]}')
        else:
            names.append(plain(author))
    return ', '.join(names)


def parse(text):
    parser = BibTexParser(ignore_nonstandard_types=False)
    database = parser.parse(text, partial=False)
    # The library preserves unparsed input as comments: reject likely malformed entries.
    for comment in database.comments:
        if re.search(r'@\w+\s*[{(]', comment):
            raise ValueError('Malformed BibTeX entry; import stopped without changing output.')
    if not database.entries:
        raise ValueError('The bibliography contains no publication entries.')
    publications, seen = [], set()
    for entry in database.entries:
        key = entry['ID']
        if key in seen:
            raise ValueError(f'Duplicate citation key: {key}')
        seen.add(key)
        for required in ['title', 'author', 'year']:
            if not entry.get(required):
                raise ValueError(f'{key}: missing {required}')
        year = entry['year'].strip()
        if not re.fullmatch(r'\d{4}', year):
            raise ValueError(f'{key}: year must contain four digits')
        areas = [s.strip() for s in re.split(r'[,;]', entry.get('areas', '')) if s.strip()]
        if set(areas) - AREAS.keys():
            raise ValueError(f'{key}: areas must be networks, social, or learning')
        areas = list(dict.fromkeys(areas))
        if not areas:
            print(f'Note: {key} appears in All publications only (no areas field).')
        doi = entry.get('doi', '').strip()
        doi = re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', doi, flags=re.I)
        if doi and not re.fullmatch(r'10\.\d{4,9}/\S+', doi):
            raise ValueError(f'{key}: invalid DOI')
        link = 'https://doi.org/' + quote(doi, safe='/():;') if doi else entry.get('url', '').strip()
        if link and (urlsplit(link).scheme not in ('http', 'https') or not urlsplit(link).netloc):
            raise ValueError(f'{key}: publication URL must use http or https')
        featured = entry.get('featured', 'false').strip().lower()
        if featured not in ('true', 'false'):
            raise ValueError(f'{key}: featured must be true or false')
        title = plain(entry['title'])
        if title.isupper():
            title = title.capitalize()
        venue = plain(entry.get('journal') or entry.get('booktitle') or entry.get('school') or entry.get('publisher', ''))
        publications.append(dict(id=key, title=title, authors=author_names(entry['author']),
                                 year=int(year), venue=venue, link=link, areas=areas,
                                 featured=featured == 'true', type=entry['ENTRYTYPE'],
                                 status=plain(entry.get('status', ''))))
    return sorted(publications, key=lambda p: (-p['year'], p['title'].casefold()))


def write_if_changed(path, text):
    if path.exists() and path.read_text() == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(text)
    temporary.replace(path)


def generate():
    source = SOURCE.read_text(encoding='utf-8')
    publications = parse(source)
    output = json.dumps(publications, ensure_ascii=False, indent=2) + '\n'
    write_if_changed(ROOT / 'data/publications.json', output)
    write_if_changed(ROOT / 'data/research_areas.json', json.dumps(AREAS, indent=2) + '\n')
    write_if_changed(ROOT / 'static/files/publications.bib', source)
    print(f'Imported {len(publications)} publications from {SOURCE.name}.')


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    generate()
