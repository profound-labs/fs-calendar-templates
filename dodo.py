import re
from typing import Optional
from datetime import datetime
from pathlib import Path
from doit.action import CmdAction
from mako.template import Template
import pymupdf
from pymupdf.utils import get_pixmap
from PIL import Image

CAL_YEARS = [2026, 2027]

DOIT_CONFIG = {
    'default_tasks': [
        'Template *',
    ],
    'verbosity': 2,
}

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
        "german",
        "italian",
        "norwegian",
        "portuguese",
        "thai",
    ]

    def all_images_actions():
        year = CAL_YEARS[0]
        language = "english"

        # Produce the empty content area example for each template.
        for template in templates:
            if template == "wall-landscape":
                continue
            yield get_image_task(year=year, language=language, template_name=template, placeholders=False,  cropmarks=False, varnishmask=False)

        # Produce all examples for the wall-landscape template.
        template = "wall-landscape"
        yield get_image_task(year=year, language=language, template_name=template, placeholders=True,  cropmarks=False, varnishmask=False)
        yield get_image_task(year=year, language=language, template_name=template, placeholders=True,  cropmarks=True,  varnishmask=False)
        yield get_image_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=False, varnishmask=False)
        yield get_image_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=False)
        yield get_image_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=True)

    def all_templates_actions():
        for year in CAL_YEARS:
            for language in languages:
                for template in templates:
                    yield get_template_task(year=year, language=language, template_name=template, placeholders=True,  cropmarks=False, varnishmask=False)
                    yield get_template_task(year=year, language=language, template_name=template, placeholders=True,  cropmarks=True,  varnishmask=False)
                    yield get_template_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=False, varnishmask=False)
                    yield get_template_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=False)
                    yield get_template_task(year=year, language=language, template_name=template, placeholders=False, cropmarks=True,  varnishmask=True)

    yield all_templates_actions()
    yield all_images_actions()

def get_template_path(year: int,
                      language: str,
                      template_name: str,
                      placeholders = True,
                      cropmarks = False,
                      varnishmask = False) -> Path:
    dist_dir = Path("gh-pages/templates").joinpath(str(year)).joinpath(language).joinpath(template_name)

    out_name = template_name
    if placeholders:
        out_name += "_placeholders"
    if cropmarks:
        out_name += "_cropmarks"
    if varnishmask:
        out_name += "_varnishmask"

    out_file = f"{out_name}.pdf"

    return dist_dir.joinpath(out_file)

def get_template_task(year: int,
                      language: str,
                      template_name: str,
                      placeholders = True,
                      cropmarks = False,
                      varnishmask = False) -> dict:
    events_csv_path = f"data/years/events-{year}.csv"

    template_path = get_template_path(year=year,
                                      language=language,
                                      template_name=template_name,
                                      placeholders=placeholders,
                                      cropmarks=cropmarks,
                                      varnishmask=varnishmask)
    template_dir = template_path.parent

    def _action():
        if not template_dir.exists():
            template_dir.mkdir(parents=True)

        tex_content = ""

        with open(f"templates/{template_name}/calendar.mako.tex", "r", encoding="utf-8") as f:
            tex_content = f.read()

        t = Template(tex_content)
        tex_content = str(t.render(
            year=year,
            alt_year=year + 543,
            language=language,
            placeholders=placeholders,
            cropmarks=cropmarks,
            varnishmask=varnishmask,
        ))

        with open(f"templates/{template_name}/calendar.tex", 'w', encoding="utf-8") as f:
            f.write(tex_content)

        cmd = f"""
    cd "templates/{template_name}" && \
    lualatex -interaction=nonstopmode -halt-on-error calendar.tex && \
    cp calendar.pdf "../../{template_path}"
        """

        return cmd

    return {
        'file_dep': [events_csv_path],
        'basename': f"Template {year} {language} {template_name} placeholders:{placeholders} cropmarks:{cropmarks} varnishmask:{varnishmask}",
        'actions': [CmdAction(_action)],
        'targets': [template_path],
        'verbosity': 1,
        'clean': True,
    }

def get_image_task(year: int,
                   language: str,
                   template_name: str,
                   placeholders = True,
                   cropmarks = False,
                   varnishmask = False) -> dict:

    template_path = get_template_path(year=year,
                                      language=language,
                                      template_name=template_name,
                                      placeholders=placeholders,
                                      cropmarks=cropmarks,
                                      varnishmask=varnishmask)

    out_png_page_path = Path("gh-pages/assets/images/").joinpath(template_path.stem+"-p9.png")

    def _action():
        # The gold bg pages get too dark with the multiply effect.
        if template_name.endswith("gold-bg"):
            color_multiply_factor = None
        else:
            color_multiply_factor = 1.5

        pdf_page_to_png(template_path, 9, out_png_page_path, color_multiply_factor)

    return {
        'file_dep': [template_path],
        'basename': f"Image {year} {language} {template_name} placeholders:{placeholders} cropmarks:{cropmarks} varnishmask:{varnishmask}",
        'actions': [_action],
        'targets': [out_png_page_path],
        'verbosity': 1,
        'clean': True,
    }

def get_year_data_task(year: int):
    from calculate_data import events_csv

    events_csv_path = f"data/years/events-{year}.csv"

    def _action():
        events_csv(year, events_csv_path)

    return {
        'basename': f"Events {year}",
        'actions': [_action],
        'targets': [events_csv_path],
        'clean': True,
    }

def task_calculate_all_years_data():
    for year in CAL_YEARS:
        yield get_year_data_task(year)

def task_copy_fonts():
    dist_dir = Path("gh-pages/templates/")

    def _action():
        if not dist_dir.exists():
            dist_dir.mkdir(parents=True)
        cmd = f""" cp -r ./fonts/ "{dist_dir}" """
        return cmd

    return {
        'actions': [CmdAction(_action)]
    }

def task_update_html_info():
    def _action():
        html_content = ""

        with open("gh-pages/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        last_updated = datetime.now().isoformat()[0:10]
        calendar_years = ", ".join([str(i) for i in CAL_YEARS])

        html_content = re.sub(r'<em id="info-last-updated">\d{4}-\d{2}-\d{2}</em>', f"""<em id="info-last-updated">{last_updated}</em>""", html_content)
        html_content = re.sub(r'<em id="info-calendar-years">[0-9, ]+</em>', f"""<em id="info-calendar-years">{calendar_years}</em>""", html_content)

        with open("gh-pages/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    return {
        'actions': [_action]
    }


def pdf_page_to_png(pdf_path: Path,
                    page_number: int,
                    output_path: Path,
                    color_multiply_factor: Optional[float] = None):
    try:
        doc = pymupdf.open(pdf_path)
    except FileNotFoundError:
        raise Exception(f"Error: File '{pdf_path}' not found.")
    except Exception as e:
        raise Exception(f"Error opening PDF file: {str(e)}")

    # Check if the PDF has enough pages
    if doc.page_count < page_number:
        doc.close()
        raise Exception(f"Error: PDF file '{pdf_path}' has less than {page_number} pages.")

    # Get the page and convert it to a pixmap with 600 DPI
    page = doc[page_number-1]

    pix = get_pixmap(page=page, dpi=600)

    # Convert pixmap to Pillow Image
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()

    # Resize the image to 900px wide
    img = img.resize((900, int(img.height * 900 / img.width)))

    # Strengthen colors
    if color_multiply_factor is not None:
        result_img = multiply_effect(img, color_multiply_factor)
    else:
        result_img = img

    # Save the resized image
    try:
        result_img.save(output_path, "PNG")
    except Exception as e:
        raise Exception(f"Error saving PNG file: {str(e)}")

def multiply_effect(rgb_img: Image.Image, factor: float) -> Image.Image:
    width, height = rgb_img.size

    # Create a new image for the result
    result_img = Image.new('RGB', (width, height))

    # Iterate through each pixel and apply the multiply effect
    for x in range(width):
        for y in range(height):
            px = rgb_img.getpixel((x, y))
            if not isinstance(px, tuple):
                raise Exception("Can't get the pixel value")

            r, g, b = px

            # Invert colors (treat white as 0)
            inv_r, inv_g, inv_b = 255 - r, 255 - g, 255 - b

            # Apply multiplication
            mult_r = int(min(inv_r * factor, 255))
            mult_g = int(min(inv_g * factor, 255))
            mult_b = int(min(inv_b * factor, 255))

            # Invert colors back
            res_r, res_g, res_b = 255 - mult_r, 255 - mult_g, 255 - mult_b

            result_img.putpixel((x, y), (res_r, res_g, res_b))

    return result_img
