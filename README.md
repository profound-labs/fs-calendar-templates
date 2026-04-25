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
