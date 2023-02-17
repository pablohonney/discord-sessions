from ..orthographic_neighborhood import (
    read_system_vocab,
    build_dijkstra_graph,
    find_shortest_word_chain,
)
from ..orthographic_neighborhood_graph_builder import OrthographicNeighborhoodGraphBuilder

from .test_orthographic_neighborhood import dumb_graph


def test_find_shortest_word_chain__find_path(dumb_graph):
    d_graph = build_dijkstra_graph(dumb_graph)
    assert find_shortest_word_chain("hood", "boob", d_graph) == ["hood", "hook", "book", "boob"]


def test_find_shortest_word_chain__finds_path_to_itself(dumb_graph):
    d_graph = build_dijkstra_graph(dumb_graph)
    assert find_shortest_word_chain("hood", "hood", d_graph) == ["hood"]  # path to itself


def test_find_shortest_word_chain__find_no_path(dumb_graph):
    d_graph = build_dijkstra_graph(dumb_graph)
    assert find_shortest_word_chain("hood", "bush", d_graph) == []


def test_find_shortest_word_chain__real_example():
    graph = OrthographicNeighborhoodGraphBuilder(read_system_vocab()).build_graph(3)
    d_graph = build_dijkstra_graph(graph)

    path = find_shortest_word_chain("dog", "cat", d_graph)
    assert path == ['dog', 'cog', 'cag', 'cat']


def test_find_shortest_word_chain__finds_the_path_both_ways():
    graph = OrthographicNeighborhoodGraphBuilder(read_system_vocab()).build_graph(3)
    d_graph = build_dijkstra_graph(graph)

    assert find_shortest_word_chain("dog", "cat", d_graph) == find_shortest_word_chain("cat", "dog", d_graph)[::-1]
