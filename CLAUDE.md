# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Forest Sangha calendar templates — generates printable wall and desk calendars as PDFs using LuaLaTeX and the `wallcalendar` document class. Calendars include Buddhist lunar observance days (uposathas), moon phases, and Vassa dates computed by the `splendidmoons` Python library.

## Build System

Uses **doit** (Python task runner) for all build orchestration. The Python environment is managed with **Poetry** (local venv in `.venv/`).

```bash
# Install dependencies
poetry install

# Build all templates for all years/languages (default task)
doit

# Build a specific year/language/template (glob patterns supported)
doit run "Template 2027 norwegian *"

# Clean and rebuild a specific combination
doit clean "Template 2027 norwegian *"; doit run "Template 2027 norwegian *"

# Generate event CSV data for a year
doit run "Events 2026"

# Compile SCSS for the gh-pages site
npm run sass
```

Output PDFs go to `gh-pages/templates/{year}/{language}/{template}/`.

## Architecture

### Data Pipeline

1. `calculate_data.py` generates per-year CSV files (`data/years/events-{year}.csv`) containing moon phases, uposathas, and annual events from `data/annual-events.csv`
2. `dodo.py` renders Mako templates (`templates/{name}/calendar.mako.tex`) into `.tex` files, then compiles with `lualatex`
3. Each template task produces variants: with/without placeholders, cropmarks, varnish mask

### Template Structure

Six templates in `templates/`: `desk-landscape`, `desk-portrait`, `desk-portrait-gold-bg`, `wall-landscape`, `wall-portrait`, `wall-portrait-gold-bg`. Each contains:
- `calendar.mako.tex` — Mako template that receives `year`, `alt_year`, `language`, `placeholders`, `cropmarks`, `varnishmask`
- `wall-local.sty` — template-specific LaTeX style
- Symlinks to shared files (`wallcalendar.cls`, Lua scripts, `i18n/`)

### Shared LaTeX Files (root)

- `wallcalendar.cls` — main document class
- `wallcalendar-*.lua` — Lua scripts for CSV parsing, date calculations, helper functions
- `calendar-shared.tex` — shared macros input by all templates
- `text-{language}.tex` — per-language text content (quotes, translations)
- `translation-keys.tex` / `address-macros.tex` — i18n key definitions
- `i18n/wallcalendar-{language}.tex` — locale-specific day/month names

### Key Configuration in dodo.py

- `CAL_YEARS` — list of years to generate (e.g., `[2026, 2027]`)
- `languages` — list of supported languages
- `templates` — list of template names

### Dependencies

- **Python**: splendidmoons (lunar calendar), doit, mako, pillow, pymupdf
- **System**: lualatex (TeX Live), fonts in `fonts/`
- **Node**: sass, @picocss/pico (for gh-pages site only)
