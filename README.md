# Alessia Galdeman · Hugo website

An English academic website preserving the charcoal, sage, serif typography, and circular homepage motif. Requires Hugo 0.136.2+ and Python 3.9+. A small progressive-enhancement script provides publication filtering; every paper remains readable without JavaScript.

## First-time setup

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Preview and build

```sh
.venv/bin/python scripts/site.py serve --port 1314
# Open http://localhost:1314
.venv/bin/python scripts/site.py build
# Deployable output is in public/
```

The preview command watches the BibTeX file as well as Hugo content. Saving the bibliography regenerates the publication data and triggers Hugo live reload. Invalid bibliography edits show an error in the terminal and retain the last valid publication list. Stop the preview with Ctrl+C.

Use `scripts/site.py build` instead of plain `hugo` to ensure the bibliography is imported before every build. The GitHub Pages workflow runs the importer automatically, so editing and pushing the `.bib` file updates the deployed publication list.

## Add or edit publications

**Only edit `bibliography/publications.bib`.** The current file is imported from `references-3.bib`, with research areas and featured selections added. Publication dates, authors, venues, and links use that bibliography rather than the older CV.

```bibtex
@article{unique-citation-key,
  title = {Your paper title},
  author = {Galdeman, Alessia and Collaborator, First Name},
  year = {2027},
  journal = {Journal name},
  doi = {10.1234/example},
  areas = {networks; learning},
  featured = {false}
}
```

- `title`, `author`, and a four-digit `year` are required. Keys must be unique.
- Use `journal` or `booktitle` for the venue. `school` and `publisher` are fallbacks.
- `doi` is preferred for the paper link; `url` is used if no DOI is present. No link is displayed if both are absent.
- Optional `areas` accepts `networks`, `social`, and `learning`, separated by semicolons or commas. Papers can appear in multiple filters. Missing areas keeps a paper in **All publications** and prints a reminder during import; it never silently disappears.
- `networks`: Temporal & multilayer networks.
- `social`: Computational social science.
- `learning`: Machine learning on graphs.
- Set `featured = {true}` to show a paper in the homepage selection.
- Optional `status = {Under review}` labels an unpublished manuscript; use `@unpublished` and the submission year.
- Records are sorted newest first, then alphabetically by title.
- Replacing the file with a fresh export also replaces custom `areas`/`featured` fields. Retain those fields to preserve categorization and homepage selections.

BibTeX parsing uses the pinned [bibtexparser library](https://bibtexparser.readthedocs.io/en/v1.4.0/tutorial.html), including standard string macros, nested braces, and LaTeX accents. Imports validate duplicate keys, required metadata, categories, and URL schemes before writing any output.

`data/publications.json`, `data/research_areas.json`, and `static/files/publications.bib` are generated; do not edit them. They are committed so ordinary Hugo previews can still show the last imported bibliography. The public BibTeX download contains exactly the source bibliography, including its custom fields: do not add private notes to this public source.

Run checks with `.venv/bin/python -m unittest discover -s tests`.

## Other updates

- Homepage introduction: `content/_index.md`.
- Biography: `content/about.md`.
- Research themes and collaboration summary: `content/research.md`.
- Courses: `content/teaching.md`.
- Email, LinkedIn, Bluesky, Scholar and Scopus profile URLs: `hugo.toml`.
- Visual styling: `static/css/site.css`; templates: `layouts/`.
- Filter behaviour: `static/js/publications.js`. Links such as `/publications/?area=networks` select a filter; browser Back/Forward restores previous selections.

## GitHub Pages

The workflow installs the pinned Python dependencies, runs importer tests, imports the bibliography, builds Hugo, and deploys on a push to `main` or `master`. In **Settings → Pages**, select **GitHub Actions** as the source. No push or deployment has been performed during local development. Legacy root HTML/CSS/assets remain as a reference; Hugo publishes only `public/`. Do not open the legacy root `index.html` to preview the new site.

## Content notes

The biography and teaching content were adapted from the CV dated 18 September 2026. Personal administrative details, detailed talks, supervision counts, and course hours are omitted. Contact and academic profile URLs were supplied by the owner.

The supplied bibliography has 17 papers and one doctoral thesis. Research-area assignments are editorial and editable through `areas`. The FORESEEN formal-methods paper is included in All publications without being forced into an unrelated research theme. Old handwritten publication records, including the three under-review manuscripts absent from the supplied bibliography, are preserved in `archive/` and no longer published. Add those manuscripts to the BibTeX source if you want them displayed again.

Original homepage design: Luther by [StyleShout](https://www.styleshout.com/), credited in the site footer. License: `readme.txt`. Fonts use Google Fonts with local fallbacks.
