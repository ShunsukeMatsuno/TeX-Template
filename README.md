# StyleSheets
LaTeX original style sheets

- `paper/paper.sty`: academic paper
- `slide`: presentation slide
  - `./paper.sty`
  - `./aea.bst`: from [AEA](https://www.aeaweb.org/journals/templates)  
- `slide/script.sty`: presentation script

# Installation 
## Manually 
- Run `kpsewhich -var-value=TEXMFHOME`
  - On my Linux, it returns, `/usr/local/texlive/texmf-local/`
- Put the style sheets in `TEXMFHOME/tex/latex/local`
- Put the bst sheets in `TEXMFHOME/bibtex/bst/local`

## Using scripts
- Linux: run `install.sh` 
