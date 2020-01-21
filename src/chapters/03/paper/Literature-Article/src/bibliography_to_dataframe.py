"""
Creates a dataframe with the entries from the `bibliography.tex`.
"""
import hashlib
import imp
import itertools
import sys
from importlib.machinery import SourceFileLoader

import pandas as pd

tools = SourceFileLoader("tools", "src/tools.py").load_module()

columns = [
    "abstract",
    "author",
    "category",
    "date",
    "doi",
    "journal",
    "key",
    "open_access",
    "primary_category",
    "provenance",
    "score",
    "title",
    "unique_key",
    "url",
]


def remove_symbols_from_entry(entry):
    entry = entry.replace("{", "")
    entry = entry.replace(",", "")
    entry = entry.replace("}", "")
    entry = entry.replace('"', "")
    entry = entry.replace(" = ", "=")

    return entry


def entry_to_dictionary(entry):
    split_entry = entry.split("\n")
    clean_entry = [el for el in split_entry if "=" in el]

    details = {}
    for element in clean_entry:
        key, value = element.split("=")
        details[key] = value
    return details


def dictionary_to_dataframe(raw_article):
    values = []
    for key in columns:
        try:
            if key == "provenance":
                values.append(["Manual"])
            elif key == "unique_key":
                name = raw_article["author"][0][-1]
                title = raw_article["title"]
                year = raw_article["date"]

                string = name + title + year
                hash_object = hashlib.md5(string.encode("utf-8"))

                unique_key = hash_object.hexdigest()
                values.append([unique_key])
            elif type(raw_article[key]) is not list:
                values.append([raw_article[key]])
            else:
                values.append(raw_article[key])
        except KeyError:
            values.append(["Not given"])

    data = []
    for row in itertools.product(*values):
        data.append(row)
    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    file = sys.argv[1]
    with (open(file, "r")) as textfile:
        bibliography = textfile.read()

    game_theory_section = bibliography.split("% End Game Theory")[0]
    raw_articles = game_theory_section.split("@")
    raw_articles = [art.lower() for art in raw_articles]

    clean_articles = [
        remove_symbols_from_entry(article) for article in raw_articles
    ]
    index = ["article" in article for article in clean_articles]
    result = [
        article
        for article, boolean in zip(clean_articles, index)
        if boolean == True
    ]

    articles = []
    for i, art in enumerate(result):
        articles.append(entry_to_dictionary(art))

    for article in articles:
        for k, v in list(article.items()):
            new_key = "".join(k.split())
            if new_key == "year":
                new_key = "date"
            article[new_key] = article.pop(k)

    # break up authors
    for article in articles:
        article["author"] = [
            tools.normalise_name(name)
            for name in article["author"].split(" and")
        ]

    dfs = []
    for article in articles:
        dfs.append(dictionary_to_dataframe(article))

    df = pd.concat(dfs, ignore_index=True)
    df.to_json("src/data/bibliography.json")
