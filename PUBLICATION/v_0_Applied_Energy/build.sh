#!/bin/zsh
# Full LaTeX build: pdflatex -> bibtex -> pdflatex x2 -> clean
# bibtex is allowed to fail while the manuscript skeleton still has no citations.
set -e
cd "$(dirname "$0")"

pdflatex -synctex=1 -interaction=nonstopmode paper.tex > /dev/null 2>&1
bibtex paper > /dev/null 2>&1 || echo "NOTE: bibtex reported no citations yet (skeleton stage)."
pdflatex -synctex=1 -interaction=nonstopmode paper.tex > /dev/null 2>&1
pdflatex -synctex=1 -interaction=nonstopmode paper.tex 2>&1 | grep -E "(Output written|Overfull|Underfull)" || true

# Check for undefined refs/cites
if grep -q "undefined" paper.log 2>/dev/null; then
    echo "WARNING: undefined references/citations:"
    grep "undefined" paper.log
fi

# Clean temp files
rm -f paper.aux paper.blg paper.log paper.out paper.toc paper.lof paper.lot \
      paper.fls paper.fdb_latexmk paper.nav paper.snm paper.vrb

echo "Build complete."
