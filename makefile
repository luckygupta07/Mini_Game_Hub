LATEX = report.tex
PDF = report.pdf

all: $(PDF)
$(PDF): $(LATEX)
	pdflatex $<	
	pdflatex $<


clean:
	rm -f *.aux *.log *.out $(PDF)
.PHONY: clean
