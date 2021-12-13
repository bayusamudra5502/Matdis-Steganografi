all: makalah

makalah: src/docs/Makalah.tex
	@pdflatex -halt-on-error  -output-directory ./docs $<

watch:
	@npm run watch

notebook:
	@jupyter notebook --no-browser

.PHONY: all watch notebook
