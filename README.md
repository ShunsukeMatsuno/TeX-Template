# StyleSheets
LaTeX original style sheets

- `paper/paper.sty`: academic paper
- `slide`: presentation slide
  - `./paper.sty`
- `slide/script.sty`: presentation script

# Installation 
Prerequisite: TeX Live 2025
## Manually 
- Run `kpsewhich -var-value=TEXMFLOCAL` (or alternatively use user-specific directory) 
  - On Linux, it will typically return, `/usr/local/texlive/texmf-local/`
  - On Windows, it will typically return `C:/texlive/texmf-local`
- Put the style sheets in `TEXMFHOME/tex/latex/local`
- Put the bst sheets in `TEXMFHOME/bibtex/bst/local`

## Using scripts
On Linux or Windows with `git bash`.
```bash
cd ~/Downloads    # optional
git clone https://github.com/ShunsukeMatsuno/TeX-Template
cd Tex-Template
sh ./install.sh
```
After successful installation you can remove the cloned repo.

Note WSL2 won't work unless you install texlive on wsl.
