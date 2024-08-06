#!/bin/sh
TEXMFHOME=$(kpsewhich -var-value=TEXMFHOME)

path_sty=$TEXMFHOME/tex/latex/local
path_bst=$TEXMFHOME/bibtex/bst/local

cp ./paper/paper.sty $path_sty
cp ./paper/aes.bst $path_bst
cp ./slide/slide.sty $path_sty
cp ./slide/script.sty $path_sty


texhash