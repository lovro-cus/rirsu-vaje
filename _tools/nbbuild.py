"""Pomozni modul za programsko gradnjo Jupyter notebookov (.ipynb).

Vsak notebook sestavimo iz seznama celic oblike:
    ("md", "markdown besedilo")   -> markdown celica
    ("code", "python koda")        -> code celica

Funkcija build() zgradi in zapise .ipynb datoteko.
Funkcija execute() notebook izvede z venv kernelom (nbconvert --execute)
in shrani rezultate (izhode) nazaj v isto datoteko -> primerno za zagovor.
"""
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell


def build(path, cells, kernel_name="python3"):
    """Zgradi .ipynb iz seznama (tip, vsebina) celic in ga zapise na disk."""
    nb = new_notebook()
    nb_cells = []
    for kind, src in cells:
        if kind == "md":
            nb_cells.append(new_markdown_cell(src))
        else:
            nb_cells.append(new_code_cell(src))
    nb.cells = nb_cells
    # metapodatki o kernelu, da Jupyter ve s cim izvesti
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3", "language": "python", "name": kernel_name
    }
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    return path
