all:
	pdflatex --shell-escape main.tex
	bibtex main 
	pdflatex --shell-escape main.tex
	pdflatex --shell-escape main.tex
abstract:
	pdflatex --shell-escape umiabstract.tex

clean:
	rm -rf *.out *.aux *.bbl *.blg *.pdf *.log  *.lot *.lof *.toc  *~ 
	rm -rf prelude/*.aux intro/*.aux presto/*.aux acdctcp/*.aux conc/*.aux prelude/*~ intro/*~ presto/*~ acdctcp/*~ conc/*~
show:
	evince main.pdf
