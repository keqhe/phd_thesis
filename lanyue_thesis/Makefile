MAIN      = dissertation
SRCS      = *.tex */*.tex
TARG      = $(MAIN).pdf

all: $(MAIN).tex $(MAIN).bbl
	pdflatex $(MAIN)
	bibtex -min-crossrefs=1000 $(MAIN)
	bash redo-bib.csh main
	pdflatex $(MAIN)
	fish change-lof.sh
	pdflatex $(MAIN)

bib: $(MAIN).bbl bib.tex

$(MAIN).bbl: $(MAIN).aux
	export BIBINPUTS=/u/l/l/ll/private/my-thesis/bibs
	bibtex -min-crossrefs=1000 $(MAIN)

$(MAIN).aux: $(MAIN).tex
	export BIBINPUTS=/u/l/l/ll/private/my-thesis/bibs
	pdflatex $(MAIN)	

clean:
	rm -rf *.aux *.log *.bbl *.toc *.lof *.pdf *.xml
