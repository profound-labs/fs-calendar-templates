# Forest Sangha Calendar Templates

Using the [wallcalendar](https://github.com/profound-labs/wallcalendar) documentclass.

Visit the project page:

<https://profound-labs.github.io/fs-calendar-templates/>

Build all years and languages defined in `dodo.py`:

```
poetry run doit
```

After an update, edit `gh-pages/index.html`

``` html
<p>Last updated: <em id="info-last-updated">2026-04-25</em></p>
<p>Calendar years included: <em id="info-calendar-years">2026, 2027, 2028, 2029, 2030</em></p>
```

The list of years corresponds to `CAL_YEARS` in `dodo.py`.

Build a given year and language:

```
poetry run doit clean "Template 2027 norwegian *"; poetry run doit run "Template 2027 norwegian *";
```

The PDFs are written to `gh-pages/` folder.

## Starting a new year

```
git clone ../fs-calendar-templates/ 2027_main
cd 2027_main
rm .git -rf
git init

poetry env use python3.14
poetry install
poetry shell
```

Remove extra folders from the `./templates` and `./images` folders.

```
rm templates/desk-* templates/wall-portrait/ templates/wall-portrait-gold-bg/ -r
rm images/jpg_desk_* images/jpg_wall_portrait/ -r
```

Remove from `calendar.mako.tex` template:

```
% if placeholders:
\wireHoles
% else:
\emptyPhotosAndQuotes
% endif
```

Render the PDF for the given year. This also re-generates the year data CSV for that year.

```
doit run "Template 2027 portuguese wall-landscape placeholders:False cropmarks:False varnishmask:False"
```

PDF is in `gh-pages/`. If needs a clean folder, use `doit clean ...`

First commit.

```
git add -A .
git commit -m first
```

Landscape photos should be cropped to `1600 x 2366 px`.
