import glob
import pathlib
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher

import bibtexparser
import known
from bibtexparser.bibdatabase import BibDatabase
from invoke import task


@task
def compile(c):
    """
    Compile the LaTeX document.
    """
    c.run("latexmk  -interaction=nonstopmode  --xelatex -shell-escape main.tex")


@task
def spellcheck(c):
    """
    Check spelling
    """

    book = list(pathlib.Path("./src/").glob("chapters/0*/main.tex"))
    exit_codes = [0]
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


@task
def bibliography(c):
    """
    Merges the bibliography files for each chapter to one and cleans the entries.
    """
    filenames = glob.glob("src/chapters/*/bibliography.bib")

    with open("bibliography.bib", "w") as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    with open("bibliography.bib") as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(
            common_strings=True
        ).parse_file(bibtex_file)

    titles = [entry["title"].lower() for entry in bib_database.entries]
    keys = [entry["ID"].capitalize() for entry in bib_database.entries]

    bib_database.entries.reverse()
    entries = bib_database.entries

    # for entry in entries:
    #     entry["ID"] = entry["ID"].capitalize()

    unique_titles = set(titles)

    # Drop duplicates on title and keep track of their keys
    to_keep = []
    for title in unique_titles:
        for entry in entries:
            if title == entry["title"].lower():
                to_keep.append(entry)
                break

    keys_to_keep = [entry["ID"].capitalize() for entry in to_keep]
    dropped_keys = list(set(keys) - set(keys_to_keep))
    duplicate_keys = [k for k, v in Counter(keys_to_keep).items() if v > 1]

    # Check the number of papers assigned to the remaining keys
    keys_to_check = []
    for key in duplicate_keys:
        unique_titles = set(
            [
                entry["title"].lower()
                for entry in bib_database.entries
                if entry["ID"] == key
            ]
        )
        if len(unique_titles):
            keys_to_check.append(key)

    # Create a list of citations to export.
    # Export:
    # - if the key is unique
    # - if key has duplicates with the same title export one entry
    # - if key has duplicates with similar titles (ratio > 0.7) export one entry
    # - if key has duplicates with different titles export all entries with altered key

    citations_to_export = []
    for key in set(keys_to_keep):
        if key in keys_to_check:
            unique_titles = set(
                [
                    entry["title"].lower()
                    for entry in bib_database.entries
                    if entry["ID"].capitalize() == key
                ]
            )
            if SequenceMatcher(None, *unique_titles).ratio() > 0.7:
                for entry in bib_database.entries:
                    if key == entry["ID"].capitalize():
                        citations_to_export.append(entry)
                        break
            else:
                dropped_keys.append(key)
                for i, title in enumerate(unique_titles):
                    for entry in bib_database.entries:
                        if entry["title"].lower() == title:
                            entry["ID"] = entry["ID"] + f"{i}"
                            citations_to_export.append(entry)
        else:
            for entry in bib_database.entries:
                if key == entry["ID"].capitalize():
                    citations_to_export.append(entry)
                    break

    # Export the new bibliography and a list of dropped keys
    db = BibDatabase()
    db.entries = citations_to_export

    with open("bibliography.bib", "w") as bibtex_file:
        bibtexparser.dump(db, bibtex_file)
    with open("dropped_keys.txt", "w") as outfile:
        for key in dropped_keys:
            outfile.write(f"{key}\n")

@task
def doctest(c):
    """
    Check spelling
    """

    book = list(pathlib.Path("./src/").glob("chapters/0*/main.tex"))
    for path in book:
        chapter = chapter = str(path).split('chapters/')[-1][:2]
        print(f'Testing chapter {chapter}')
        c.run(f"python -m doctest -v {path}")
