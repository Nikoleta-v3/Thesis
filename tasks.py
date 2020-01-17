from invoke import task

@task
def compile(c):
    """
    Compile the LaTeX document.
    """
    c.run("latexmk  -interaction=nonstopmode  --xelatex -shell-escape main.tex")

@task
def get_bibliography(c):
    """
    Merges the bibliography files for each chapter to one.
    """
    c.run("cat src/chapters/01/bibliography.bib >> bibliography.bib")
