import collections
import itertools

from scipy import stats

import networkx as nx


def normalise_name(name):
    """
    Normalise name to: Forename Surname
    """
    elements = name.split()

    new = elements[0].title() + " "
    new += elements[-1].title()

    return new


def write_to_file(filename, metric, in_assets=True):
    """
    Saves metric value in filename. The metric's value is then read in
    automatically to `main.tex`.

    If `in_assets` is True the file in save under the assets folder.
    """
    if in_assets is True:
        file = open("../../assets/{}".format(filename), "w")  # pragma: no cover
    else:
        file = open(filename, "w")
    file.write("{}".format(metric))
    file.close()


def test_kruskal(distributions, alpha=0.05):
    """
    Performs a Kruskal–Wallis test. Returns the p-value and tests the hypothesis
    with a (1 - alpha) confidence.
    """
    _, p = stats.kruskal(*distributions)

    if p < alpha:
        print(p, "The null hypothesis can be rejected.")
    else:
        print(p, "The null hypothesis cannot be rejected.")
    return p


def test_mannwhitneyu(distributions, alternative="two-sided", alpha=0.05):
    """
    Performs a Mann Whitney U test. Returns the p-value and tests the hypothesis
    with a (1 - alpha) confidence.
    """
    _, p = stats.mannwhitneyu(*distributions, alternative=alternative)

    if p < alpha:
        print(p, "The null hypothesis can be rejected.")
    else:
        print(p, "The null hypothesis cannot be rejected.")
    return p


def generate_co_authorship_graph(data):
    """
    Returns a `networkx` graph where the nodes are authors and the edges
    collaborations.
    """
    data.author = data.author.str.lower()

    pairs = []
    for _, d in data.groupby("unique_key"):
        pairs += tuple(
            sorted(list(itertools.combinations(d["author"].unique(), 2)))
        )
        co_authors = collections.Counter(pairs)

    authors_num_papers = (
        data.groupby(["author", "unique_key"])
        .size()
        .reset_index()
        .groupby("author")
        .count()
    )
    authors_num_papers = authors_num_papers.drop(0, axis=1)

    graph = nx.Graph()
    for name, w in zip(data.author, authors_num_papers["unique_key"].values):
        graph.add_node(name)
    for pair in co_authors.items():
        graph.add_edge(*pair[0])

    return graph
