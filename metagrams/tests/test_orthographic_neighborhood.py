from ..orthographic_neighborhood import (
    check_metagram,
    build_orthographic_neighborhood_graph,
    is_word_chain,
    find_word_chain,
    read_system_vocab,
    ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH
)
from ..orthographic_neighborhood_graph_builder import OrthographicNeighborhoodGraphBuilder

import pytest


@pytest.fixture
def dumb_graph() -> ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH:
    vocab = ["hood", "hook", "book", "boob"]
    graph = build_orthographic_neighborhood_graph(vocab, 4)

    return graph


def test_check_metagram():
    with pytest.raises(ValueError):
        check_metagram("book", "shaker")

    assert check_metagram("hood", "hook")
    assert not check_metagram("hood", "book")
    assert not check_metagram("hood", "hood")


def test_words_form_word_chain(dumb_graph):
    assert is_word_chain("hood", "boob", dumb_graph)
    assert not is_word_chain("hood", "nuke", dumb_graph)


def test_find_word_chain(dumb_graph):
    assert find_word_chain("hood", "boob", dumb_graph) == ["hood", "hook", "book", "boob"]


def test_find_word_chain_on_system_vocab():
    graph = OrthographicNeighborhoodGraphBuilder(read_system_vocab()).build_graph(3)

    # this is abysmal
    print(find_word_chain("cat", "dog", graph))
