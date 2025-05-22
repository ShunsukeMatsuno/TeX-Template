#!/bin/sh

# Determine the TeX Live local installation directory
TEXMFHOME=$(kpsewhich -var-value=TEXMFLOCAL)

# Define target paths for style files, BibTeX style files, and images
path_sty=$TEXMFHOME/tex/latex/local
path_bst=$TEXMFHOME/bibtex/bst/local
path_img=$TEXMFHOME/tex/latex/local/images

# Ensure the target /images directory exists
mkdir -p "$path_img"

# Copy all .sty files from the paper directory
cp ./paper/*.sty "$path_sty"

# Copy the BibTeX style file from the paper directory
cp ./paper/aea.bst "$path_bst"

# Copy all .sty files from the slide directory
cp ./slide/*.sty "$path_sty"

# Copy the biblatex configuration file
cp ./biblatex/biblatex-aer.tex "$path_sty"

# Copy the logo file to the images directory
cp ./images/CBS_logo.png "$path_img"

# Update TeX's file database to recognize the new files
texhash

# Script finished
echo "Installation complete. Copied files to $TEXMFHOME"
