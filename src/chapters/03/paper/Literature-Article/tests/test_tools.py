import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
import pandas as pd

import pytest

tools = SourceFileLoader("tools", "src/tools.py").load_module()


def test_normalise_name():
    name = "Richard Dick grayson"

    assert tools.normalise_name(name) == "Richard Grayson"


def test_write_to_file():
    count, filename = 100, "number_of_authors.txt"
    tools.write_to_file(filename, count, in_assets=False)

    assert os.path.exists(filename)
    assert int(Path(filename).read_text()) == 100

    os.remove(filename)


def test_test_kruskal():
    x = [1, 3, 5, 7, 9]
    y = [2, 4, 6, 8, 10]
    expected_pvalue = 0.6015081344405895

    assert np.isclose(tools.test_kruskal([x, y]), expected_pvalue)


def test_test_kruskal_two():
    np.random.seed(1)
    x = 5 * np.random.randn(100) + 50
    y = 5 * np.random.randn(100) + 51

    expected_pvalue = 0.017204680222781703

    assert np.isclose(tools.test_kruskal([x, y]), expected_pvalue)


def test_test_mannwhitneyu():
    x = [1, 3, 5, 7, 9]
    y = [2, 4, 6, 8, 10]
    expected_pvalue = 0.6761033140231469

    assert np.isclose(tools.test_mannwhitneyu([x, y]), expected_pvalue)


def test_test_mannwhitneyu_two():
    np.random.seed(1)
    x = 5 * np.random.randn(100) + 50
    y = 5 * np.random.randn(100) + 51

    expected_pvalue = 0.017261846917598123

    assert np.isclose(tools.test_mannwhitneyu([x, y]), expected_pvalue)


def test_generate_co_authorship_graph():
    data = pd.read_json("tests/test_data.json")

    graph = tools.generate_co_authorship_graph(data)

    assert list(graph.nodes) == ["jean grey", "scott summers", "charles xavier"]
    assert len(graph.nodes) == 3
    assert ("jean grey", "scott summers") in graph.edges
    assert ("scott summers", "charles xavier") in graph.edges
    assert (("jean grey", "charles xavier") in graph.edges) is False
    assert len(graph.edges) == 2
