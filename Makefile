all: makalah

makalah: src/docs/Makalah.tex
	@pdflatex -halt-on-error  -output-directory ./docs $<

watch:
	@npm run watch

.PHONY: all watch
