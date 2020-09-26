LATEX=lualatex
LATEX_OPTS=-interaction=nonstopmode -halt-on-error

none:
	@echo "huh?"

wall:
	make -B wall-landscape-one-side

desk:
	make -B desk-landscape-one-side

wall-portrait-one-side:
	cd wall-portrait-one-side && $(LATEX) $(LATEX_OPTS) wall.tex

desk-portrait-one-side:
	cd desk-portrait-one-side && $(LATEX) $(LATEX_OPTS) desk.tex

wall-landscape-one-side:
	cd wall-landscape-one-side && $(LATEX) $(LATEX_OPTS) wall.tex

desk-landscape-one-side:
	cd desk-landscape-one-side && $(LATEX) $(LATEX_OPTS) desk.tex

desk-stand:
	cd desk-portrait-one-side && $(LATEX) $(LATEX_OPTS) desk-stand.tex

wall-portrait-two-side:
	cd wall-portrait-two-side && $(LATEX) $(LATEX_OPTS) wall.tex

wall-portrait-largecal-one-side:
	cd wall-portrait-largecal-one-side && $(LATEX) $(LATEX_OPTS) wall.tex

calculate-data:
	@go run ./template-helpers/calculate-data.go $(YEAR)

jpg-to-pdf:
	./template-helpers/jpg-to-pdf.sh ./images/jpg ./images/pdf
