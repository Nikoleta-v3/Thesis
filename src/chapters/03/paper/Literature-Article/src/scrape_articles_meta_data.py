"""
Scraping for articles' meta data script.
"""

import json

import pandas as pd
from tqdm import tqdm

import arcas
import requests


def get_raw_articles_on_search(api, arguments, start):
    parameters = api.parameters_fix(**arguments, start=start)
    url = api.create_url_search(parameters)

    request = api.make_request(url)
    root = api.get_root(request)
    raw_articles = api.parse(root)

    return raw_articles


if __name__ == "__main__":

    words = ["price of sinking", "price of stability"]
    apis = [arcas.Arxiv, arcas.Springer, arcas.Plos, arcas.Nature]
    for p in apis:
        pbar = tqdm(total=len(words) * len(apis))
        for key in words:
            api = p()
            for field in ["title", "abstract"]:
                start = 1
                switch = True
                arguments = {field: key, "records": 10}
                while switch is not False:

                    raw_articles = get_raw_articles_on_search(
                        api=api, arguments=arguments, start=start
                    )
                    try:
                        articles = []
                        for art in raw_articles:
                            articles.append(api.to_dataframe(art))
                        df = pd.concat(articles, ignore_index=True)
                        filename = "raw_data/price/result_{}_{}_{}_{}.json".format(
                            field, api.__class__.__name__, start, key
                        )
                        df.to_json(filename)
                    except (TypeError, ValueError) as e:
                        switch = False
                    start += 10
                pbar.update(1)
