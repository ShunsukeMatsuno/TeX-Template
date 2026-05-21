# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a LaTeX template repository providing custom style sheets and templates for academic papers, presentations, and documents. It includes:

- **paper/**: Academic paper templates with custom styling
- **slide/**: Beamer presentation templates 
- **letter/**: Letter templates
- **fonts/**: Font configuration utilities
- **biblatex/**: Bibliography styling configurations

## Common Commands

### Installation
```bash
# Install templates to TeX Live system
sh ./install.sh
```

### Document Compilation
```bash
# Compile LaTeX documents (use LuaLaTeX for unicode-math support)
lualatex document.tex

# Use latexmk for automated compilation with dependencies
latexmk -lualatex document.tex

# For documents with bibliography
latexmk -lualatex -bibtex document.tex
```

### Font Management
```bash
# Generate font fallback configurations
cd fonts/
python generate-fallbacks.py
```

## Architecture

### Style Sheet Structure
- **paper.sty**: Main academic paper styling with Unicode math support, custom fonts (Libertinus), and flexible spacing options
- **slide.sty**: Beamer presentation styling using metropolis theme with custom color scheme
- **script.sty**: Presentation script styling
- **paper_biblatex.sty**: BibLaTeX variant for bibliography management

### Font Configuration
The templates use LuaLaTeX with unicode-math package for advanced typography:
- Main text: Libertinus Serif
- Math: Libertinus Math with fallbacks (texgyrepagella-math, NewCMMath)
- Slides: Libertinus Sans

### Installation System
The `install.sh` script copies style files to the TeX Live local directory structure:
- `.sty` files → `$TEXMFLOCAL/tex/latex/local/`
- `.bst` files → `$TEXMFLOCAL/bibtex/bst/local/`
- Images → `$TEXMFLOCAL/tex/latex/local/images/`

### Template Usage Patterns
- Paper templates support spacing options: `\usepackage[onehalf]{paper}` or `\usepackage[double]{paper}`
- Slide templates include custom color macros and CBS branding
- All templates are designed for LuaLaTeX compilation with full Unicode support

## Prerequisites
- TeX Live 2025 or later
- LuaLaTeX engine
- latexmk for build automation
- Python 3.6+ (for font utilities)
- otfinfo command (lcdf-typetools package)