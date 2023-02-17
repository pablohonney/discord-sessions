from metagrams.orthographic_neighborhood import (
    find_shortest_word_chain,
    build_dijkstra_graph,
)
from metagrams.orthographic_neighborhood import VOCAB, WORD_PATH
from metagrams.orthographic_neighborhood_graph_builder import OrthographicNeighborhoodGraphBuilder


class MetagramGraph:
    def __init__(self, vocab: VOCAB):
        self._graph_builder = OrthographicNeighborhoodGraphBuilder(vocab)

    def find_word_chain(self, word1: str, word2: str) -> WORD_PATH:
        if len(word1) != len(word2):
            raise ValueError("metagrams must have the same length")

        graph = self._graph_builder.build_graph(word_length=len(word1))
        d_graph = build_dijkstra_graph(graph)

        return find_shortest_word_chain(word1, word2, d_graph)
