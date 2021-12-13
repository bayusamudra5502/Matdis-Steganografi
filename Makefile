all: makalah

makalah: src/docs/Makalah.tex
	@pdflatex -shell-escape -halt-on-error  -output-directory ./docs $<

watch:
	@npm run watch

notebook:
	@jupyter notebook --no-browser --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0

.PHONY: all watch notebook
