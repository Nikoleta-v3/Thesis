from invoke import task

@task
def compile(c):
    """
    Compile the LaTeX document.
    """
    c.run("latexmk  -interaction=nonstopmode  --xelatex -shell-escape main.tex")