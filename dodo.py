# from datetime import datetime
from pathlib import Path
# from doit.tools import title_with_actions
from doit.action import CmdAction

DOIT_CONFIG = {
    'verbosity': 2,
}

EVENTS_CSV_PATH = "./data/events.csv"
CAL_YEAR = 2026

def task_all_templates():
    templates = [
        "desk-landscape",
        "desk-portrait",
        "desk-portrait-gold-bg",
        "wall-landscape",
        "wall-portrait",
        "wall-portrait-gold-bg",
    ]

    def all_templates_actions():
        for i in templates:
            yield build_template_tasks(i)

    yield all_templates_actions()

def build_template_tasks(template_name):
    dist_dir = Path("dist/").joinpath(template_name)
    out_file = f"{template_name}.pdf"

    def _action():
        if not dist_dir.exists():
            dist_dir.mkdir(parents=True)

        cmd = """
    cd templates/%s && \
    lualatex -interaction=nonstopmode -halt-on-error calendar.tex && \
    cp calendar.pdf ../../dist/%s/%s
        """ % (template_name, template_name, out_file)

        return cmd

    return {
        'file_dep': [EVENTS_CSV_PATH],
        'basename': f"Build {template_name}",
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
