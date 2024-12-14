#!/bin/sh
TEXMFHOME=$(kpsewhich -var-value=TEXMFLOCAL)

path_sty=$TEXMFHOME/tex/latex/local
path_bst=$TEXMFHOME/bibtex/bst/local
path_img=$TEXMFHOME/tex/latex/local/images

cp ./paper/paper.sty $path_sty
cp ./paper/aea.bst $path_bst

cp ./slide/slide.sty $path_sty
cp ./slide/script.sty $path_sty

cp ./biblatex/biblatex-aer.tex $path_sty

# Copy the logo file
cp ./images/CBS_logo.png $path_img

texhash