# from datetime import datetime
from pathlib import Path
# from doit.tools import title_with_actions
from doit.action import CmdAction
from mako.template import Template

DOIT_CONFIG = {
    'verbosity': 2,
}

EVENTS_CSV_PATH = "./data/events.csv"
CAL_YEAR = 2026
ALT_YEAR = CAL_YEAR + 543

def task_all_templates():
    templates = [
        "desk-landscape",
        "desk-portrait",
        "desk-portrait-gold-bg",
        "wall-landscape",
        "wall-portrait",
        "wall-portrait-gold-bg",
    ]

    languages = [
        "english",
        # "german",
        "italian",
        # "norwegian",
        "portuguese",
        # "thai",
    ]

    def all_templates_actions():
        for language in languages:
            for template in templates:
                yield get_template_task(language=language, template_name=template, placeholders=True,  cropmarks=False, varnishmask=False)
                yield get_template_task(language=language, template_name=template, placeholders=False, cropmarks=False, varnishmask=False)
                yield get_template_task(language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=False)
                yield get_template_task(language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=True)

    yield all_templates_actions()

def get_template_task(language: str,
                      template_name: str,
                      placeholders = True,
                      cropmarks = False,
                      varnishmask = False) -> dict:
    dist_dir = Path("dist/").joinpath(language).joinpath(template_name)

    out_name = template_name
    if placeholders:
        out_name += "_placeholders"
    if cropmarks:
        out_name += "_cropmarks"
    if varnishmask:
        out_name += "_varnishmask"

    out_file = f"{out_name}.pdf"

    def _action():
        if not dist_dir.exists():
            dist_dir.mkdir(parents=True)

        tex_content = ""

        with open(f"templates/{template_name}/calendar.mako.tex", "r", encoding="utf-8") as f:
            tex_content = f.read()

        t = Template(tex_content)
        tex_content = str(t.render(
            year=CAL_YEAR,
            alt_year=ALT_YEAR,
            language=language,
            placeholders=placeholders,
            cropmarks=cropmarks,
            varnishmask=varnishmask,
        ))

        with open(f"templates/{template_name}/calendar.tex", 'w', encoding="utf-8") as f:
            f.write(tex_content)

        cmd = f"""
    cd templates/{template_name} && \
    lualatex -interaction=nonstopmode -halt-on-error calendar.tex && \
    cp calendar.pdf ../../dist/{language}/{template_name}/{out_file}
        """

        return cmd

    return {
        'file_dep': [EVENTS_CSV_PATH],
        'basename': f"Build {CAL_YEAR} {language} {template_name} placeholders:{placeholders} cropmarks:{cropmarks} varnishmask:{varnishmask}",
        'actions': [CmdAction(_action)],
        'targets': [dist_dir.joinpath(out_file)],
        'verbosity': 1,
        'clean': True,
    }

def task_calculate_year_data():
    def _action():
        from calculate_data import events_csv
        events_csv(CAL_YEAR, EVENTS_CSV_PATH)

    return {
        'actions': [_action],
        'targets': [EVENTS_CSV_PATH],
        'clean': True,
    }

# def task_jpg_to_pdf():
#     return {
#         'actions': [""" ./scripts/jpg-to-pdf.sh ./images/jpg ./images/pdf """]
#     }
