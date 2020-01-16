import glob
import imp
import json
import sys
from importlib.machinery import SourceFileLoader

import pandas as pd

import arcas
import unidecode

tools = SourceFileLoader("tools", "src/tools.py").load_module()

if __name__ == "__main__":

    topic = sys.argv[1]
    path = "src/raw_data/" + topic

    for api in [
        arcas.Nature(),
        arcas.Ieee(),
        arcas.Plos(),
        arcas.Arxiv(),
        arcas.Springer(),
    ]:

        raw_articles = []
        api_name = api.__class__.__name__

        d = []
        for filename in glob.glob("{}/*_{}_*.json".format(path, api_name)):
            with open(filename) as json_data:
                d = json.load(json_data)
                raw_articles.append(d)
        if raw_articles:
            flat_list = [item for sublist in raw_articles for item in sublist]

            articles = []
            for art in flat_list:
                articles.append(api.to_dataframe(art))

            dataframe = pd.concat(articles, ignore_index=True)
            dataframe = dataframe[
                ~(dataframe["author"] == "No authors found for this document.")
            ]
            names = dataframe.author

            if api_name == "Springer":
                edited = []
                for name in names:
                    first, last = name.split(" ", 1)
                    edited.append(last + " " + first)
                names = edited

            edited_names = [tools.normalise_names(name) for name in names]
            unicoded_names = [
                unidecode.unidecode(name) for name in edited_names
            ]
            dataframe.author = unicoded_names

            api.export(dataframe, "src/data/{}_{}.json".format(topic, api_name))
