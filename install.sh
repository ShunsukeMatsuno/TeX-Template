#!/bin/sh
TEXMFHOME=$(kpsewhich -var-value=TEXMFHOME)

path_sty=$TEXMFHOME/tex/latex/local
path_bst=$TEXMFHOME/bibtex/bst/local

cp ./paper/paper.sty $path_sty
cp ./slide/slide.sty $path_sty
cp ./slide/aes.bst $path_bst

texhash