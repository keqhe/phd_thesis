##
PAPERNAME = C3
#TOFOLDER = "/mnt/c/Users/wenfe/Desktop"
TOFOLDER = /mnt/hgfs/SharedFolder/

TARGETS = paper
TEXFILES = $(wildcard *.tex) $(wildcard sections/*.tex)
PDFS = $(addsuffix .pdf,$(TARGETS))
FIGFILES = $(wildcard ./figs/*.pdf) $(wildcard ./figs/*.tex) $(wildcard ./figs/*.eps)

all: $(PDFS)

%.pdf: %.tex %.bib %.blg %.toc $(FIGFILES) $(TEXFILES)
	pdflatex $*.tex
	bibtex $*
	pdflatex $*.tex
	pdflatex $*.tex
#	mv $*.pdf $(PAPERNAME).pdf
#	pdflatex "\def\draft{1} \input{$*.tex}"
#	bibtex $*
#	pdflatex "\def\draft{1} \input{$*.tex}"
#	pdflatex "\def\draft{1} \input{$*.tex}"
#	mv $*.pdf $(PAPERNAME)_draft.pdf
#	@echo "================================================"
#	@echo "two output files: $(PAPERNAME).pdf and $(PAPERNAME)_draft.pdf"
#	@echo "$(PAPERNAME).pdf: submission version."
#	@echo "$(PAPERNAME)_draft.pdf: draft version."
#	@echo "================================================"

draft: 
	pdflatex "\def\draft{1} \input{$*.tex}"
	bibtex $*
	pdflatex "\def\draft{1} \input{$*.tex}"
	pdflatex "\def\draft{1} \input{$*.tex}"
	mv $*.pdf $(PAPERNAME)_draft.pdf

submit:
	pdflatex $*.tex
	bibtex $*
	pdflatex $*.tex
	pdflatex $*.tex
	mv $*.pdf $(PAPERNAME).pdf


%.blg: %.bib 
	pdflatex $*.tex
	bibtex $*
	pdflatex $*.tex

%.toc: %.tex
	pdflatex $*.tex

clean:
	/bin/rm -f $(PDFS) $(PAPERNAME).pdf $(PAPERNAME)_draft.pdf  *.dvi *.aux *.ps *~ *.log *.out *.lot *.lof *.toc *.blg *.bbl url.sty figs/*~ figs/raw_figs/*~ sections/*~

FORCE:

evince:
	pdflatex $(TARGETS).tex
	evince $(PDFS) &

acro:
	pdflatex $(TARGETS).tex
	acroread $(PDFS) &

osx:
	pdflatex $(TARGETS).tex
	open $(PDFS)

windows:
	pdflatex $(TARGETS).tex
	explorer.exe $(PDFS) &

home: osx

check:
	pdflatex $(TARGETS).tex | grep -i -e "undefined" -e "multiply"

copy:
	cp $(TARGETS).pdf $(TOFOLDER)/$(PAPERNAME).pdf
#	cp $(PAPERNAME)_draft.pdf $(TOFOLDER)/



commit:
	git commit -a
	git push

tar:
	tar cvf paper.tar *.tex Makefile *.bib *.sty figs/

echo:
	@ echo $(FIGFILES)
