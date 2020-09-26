# Forest Sangha Calendar Template

Using the [wallcalendar](https://github.com/profound-labs/wallcalendar) documentclass.

## Requirements

- git annex
- [img2pdf](https://pypi.python.org/pypi/img2pdf)
- golang

## Starting a new year

Clone the template and calculate the moonday and event data in CSV for the year.

```
git clone https://github.com/profound-labs/fs-calendar-template.git ./2020_main
cd 2020_main
rm .git -rf
make calculate-data YEAR=2020
```

Edit `year` and `altYear` class options in `wall.tex` and `desk.tex`:

```
  year=2020,
  altyear=2563,
```

Test compile:

```
make wall
make desk
```

First commit:

```
git init
git annex init "2020 calendar"

git annex add images/jpg images/pdf --include-dotfiles
git commit -m "images"

git add -A
git commit -m "kickstart"
```

Crop the photos from the originals and replace the placeholders:

```
git annex unlock images/jpg/* images/pdf/*
rm images/jpg/* images/pdf/*

# Copy in the new .jpg files, then covert:
make jpg-to-pdf

git annex add images/jpg images/pdf
git add -u images/jpg images/pdf
git commit -m "cropped images"
```

Improve photos:

- Auto White Balance
- Desaturate manually Lightn. / Lumin. / Avg.

## PDF Colors

Don't use `[cmyk]` option on `xcolor` package. Declare text colors either in gray or cmyk (for color).

Images should be Grayscale colorspace.

PDF should embed Fogra29 profile.

Kenny uses Photoshop to convert the calendar to Black + Pantone 1245 C.

## Converting photos to grayscalse

*GIMP*

Use the Channel Mixer:

https://www.gimp.org/tutorials/Color2BW/#channelmixer

Then adjust Brightness and Contrast.

## Cropping and resizing photos for landscape layout

Three-side bleed is best if the images allow it.

Lock the aspect ratio of the selection tool in the image editor, then you can
forget the numbers, and resize the selection area to the crop that is best.

Calendar sizes:

Trimmed paper size: 6.75in x 10.5in = 171.45mm x 266.7mm

Photo width: 171.45mm + 2*3mm bleed = 177.45mm

Photo height: 150mm + 3mm, covering wire and top bleed

Photo height: 140mm, when two side bleed

Calendar height, including events: 85mm + 3mm bleed = 88mm

Quote, four lines, 14/18pt = 72pt + 6mm spacing = 25.4mm + 6mm = 31.4mm

Vertical sizes:

|               | p | c |       |
|---------------|---|---|-------|
| top bleed     | + |   | 3mm   |
| wire punch    | + |   | 10mm  |
| photo         | + |   | 130mm |
| quote         |   |   |       |
| cal headings  |   | + |       |
| day headings  |   | + | 5mm   |
| calendar grid |   | + |       |
| events        |   | + |       |
| bottom margin |   | + | 10mm  |

Most years have one or two months with three uposathas and the notes text allow
for three lines.

Notes for three uposathas: x

### Image Properties

- Cropped to ratio
- Resized to 300dpi
- Grayscale
- Compression 90%

### Ratios

Full-page ratio: 1.5555 = 2400px x 3733px

Three-side bleed resolution: 1.1598 = 2087px x 1800px

Three-side bleed resolution: 1.3342 = 2400px x 1800px

(? desk) Two-side bleed resolution: 1.2675 = 2028px x 1600px

Two-side bleed wall resolution: 1.47875 = 2366px x 1600px

(Image is 177.450mm x 120.000mm)

Desk resolution: 1.3369 = 1605px x 1200px

(Image is 123mm x 92mm)

123/92 = 1.33695652174

Photo width: 171.45mm + 2*3mm bleed = 177.45mm

Photo height: 150mm + 3mm = 153mm

Photo height, less: 130mm + 3mm = 133mm

Three-side bleed ratio: 177.45 / 153 = 1.1598

Three-side bleed ratio: 177.45 / 133 = 1.3342

Two-side bleed ratio: 177.45 / 140 = 1.2675

177.45 mm = 6.9862 in
153 mm = 6.0236 in
140 mm = 5.5118 in
133 mm = 5.2362 in

6.9862 * 300 = 2095.86 

6.0236 * 300 = 1807.08

5.5118 * 300 = 1653.54

5.2362 * 300 = 1570.86

---

*Three-side bleed*

For a three-side bleed, the images have to fill a space *177.45mm wide and
229.7mm tall*, this already includes 3mm bleed left and right, and 3mm on top.

The pixel size can be different from photo to photo, but the ratio of the sizes
should be the same. When you divide the height with the width, *the ratio should
be about 1.2944*.

This means you can crop smaller, but the aspect ratio of the crop should be the
same.

In the ideal case where they all have sufficient size to crop from, aiming at
300dpi for the cropped images, it translates to (height x width): *2712 x 2095
pixels*.

Checking the ratio: 2712 / 2095 = 1.2945.

*Two-side bleed*

For a two-side bleed, it is good to leave about 10mm empty space at the top, and
there is no top bleed, so that is an area *177.45mm wide and 216.7mm tall*.

The ratio of that is 1.2211. At 300dpi, in pixels (height x width):
*2559 x 2095*.

*Portrait, Two Side: Two-side bleed*

Photo is full height, on the left or right side.

The photo width is 2/3 of paper width.

Photo has bleed cut on top and bottom, plus one of left or right.

(NOTE this is for bleed on left or right side only)

(FIXME: 220? not 266?) Width: 220 * (2/3) = 146.66 + 3 = 149.66

Height: 171 + 6 = 177

Ratio: 177 / 150 = 1.18

In pixels for 300dpi: 2090 x 1771 px

177mm = 6.9685 inch 
6.9685 * 300 = 2090.55

150mm = 5.9055 inch
5.9055 * 300 = 1771.65

*Portrait, One Side, Large Calendar, Two-side bleed*

The photo width is 2/3 of paper width.

The photo height extends 1cm below the half-height line.

Width: 171 * (2/3) + 3 = 117.0

Height: (266/2) + 10 + 3 = 146

Ratio: 146 / 117 = 1.24

117mm = 4.6062 inch
4.6062 * 300 = 1381.86

146mm = 5.7480 inch
5.7480 * 300 = 1724.4

In pixels for 300dpi: 1400 x 1736 px

500*1.24
620.

### Editing

- open JPG
- Add Alpha Channel
- check if Color > Levels will improve contrast
- Desaturate, use the one with better contrast
- look at the desaturation with zoomed out image
- test is Color > Brightness and Contrast can improve the image
- Select All, then Image > Guides > Guides from Selection
- create selection with fixed size ratio
- Select > Save to Channel
- save as .xcf

Export:

- crop to selection
- scale image
- change color mode to Grayscale
- Export as JPG
- export with max 95% compression, no need for 98% and such
