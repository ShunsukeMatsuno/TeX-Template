#!/bin/sh
TEXMFHOME=$(kpsewhich -var-value=TEXMFLOCAL)

path_sty=$TEXMFHOME/tex/latex/local
path_bst=$TEXMFHOME/bibtex/bst/local

cp ./paper/paper.sty $path_sty
cp ./paper/aea.bst $path_bst

cp ./slide/slide.sty $path_sty
cp ./slide/script.sty $path_sty

cp ./biblatex/biblatex-aer.tex $path_sty

texhash