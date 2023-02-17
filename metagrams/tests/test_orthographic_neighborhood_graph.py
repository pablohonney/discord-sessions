from ..orthographic_neighborhood import (
    build_orthographic_neighborhood_graph,
    read_system_vocab,
    build_dijkstra_graph,
)
from ..orthographic_neighborhood_graph_builder import OrthographicNeighborhoodGraphBuilder


def test_orthographic_neighborhood_graph():
    vocab = ["hood", "hook", "book", "boob", "black"]
    graph = build_orthographic_neighborhood_graph(vocab, word_length=4)

    assert graph == {
        "hood": ["hook"],
        "hook": ["hood", "book"],
        "book": ["hook", "boob"],
        "boob": ["book"],
    }

    graph = build_orthographic_neighborhood_graph(vocab, word_length=5)
    assert graph == {"black": []}

    graph = build_orthographic_neighborhood_graph(vocab, word_length=6)
    assert graph == {}


# smoke test
def test_build_dijkstra_graph():
    graph = OrthographicNeighborhoodGraphBuilder(read_system_vocab()).build_graph(3)

    d_graph = build_dijkstra_graph(graph)
