# StyleSheets
LaTeX original style sheets

- `paper/paper.sty`: academic paper
- `slide`: presentation slide
  - `./paper.sty`
  - `./aea.bst`: from [AEA](https://www.aeaweb.org/journals/templates)  
- `slide/script.sty`: presentation script

# Installation 
## Manually 
- Run `kpsewhich -var-value=TEXMFLOCAL` (or alternatively use user-specific directory) 
  - On Linux, it will typically return, `/usr/local/texlive/texmf-local/`
  - On Windows, it will typically return `C:/texlive/texmf-local`
- Put the style sheets in `TEXMFHOME/tex/latex/local`
- Put the bst sheets in `TEXMFHOME/bibtex/bst/local`

## Using scripts
On Windows, run this on `git bash`.
```bash
git clone https://github.com/ShunsukeMatsuno/TeX-Template
cd Tex-Template
sh ./install.sh
```
