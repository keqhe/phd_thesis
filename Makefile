all:
	pdflatex --shell-escape main.tex
	bibtex main 
	pdflatex --shell-escape main.tex
	pdflatex --shell-escape main.tex
abstract:
	pdflatex --shell-escape umiabstract.tex

clean:
	rm -rf *.out *.aux *.bbl *.blg *.pdf *.log  *.lot *.lof *.toc  *~ 
	rm -rf prelude/*.aux intro/*.aux vnd/*.aux perfsight/*.aux conc/*.aux prelude/*~ intro/*~ vnd/*~ perfsight/*~ conc/*~
show:
	evince main.pdf
