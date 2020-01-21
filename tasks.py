import pathlib
import subprocess
import sys

import known
from invoke import task


@task
def compile(c):
    """
    Compile the LaTeX document.
    """
    c.run("latexmk  -interaction=nonstopmode  --xelatex -shell-escape main.tex")


@task
def bibliography(c):
    """
    Merges the bibliography files for each chapter to one.
    """
    c.run("cat src/chapters/01/bibliography.bib > bibliography.bib")


@task
def spellcheck(c):
    """
    Check spelling
    """

    book = list(pathlib.Path("./src/").glob("chapters/0*/main.tex"))
    exit_codes = []
    for path in book:
        latex = path.read_text()
        aspell_output = subprocess.check_output(
            ["aspell", "-t", "--list", "--lang=en_GB"], input=latex, text=True
        )
        incorrect_words = set(aspell_output.split("\n")) - {""} - known.words
        if len(incorrect_words) > 0:
            print(f"In {path} the following words are not known: ")
            for string in sorted(incorrect_words):
                print(string)
            exit_codes.append(1)
    sys.exit(max(exit_codes))
