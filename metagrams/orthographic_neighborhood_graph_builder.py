import pathlib
import json

from metagrams.orthographic_neighborhood import VOCAB, ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH, \
    build_orthographic_neighborhood_graph


class OrthographicNeighborhoodGraphBuilder:
    def __init__(self, vocab: VOCAB):
        self._vocab = vocab

    def build_graph(
            self, word_length: int, no_cache: bool = False
    ) -> ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH:
        if not no_cache and self._is_cached(word_length):
            return self._load_cached_graph(word_length)

        graph = build_orthographic_neighborhood_graph(self._vocab, word_length)

        if not self._is_cached(word_length):
            self._dump_graph(graph, word_length)

        return graph

    def _load_cached_graph(self, word_length: int) -> ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH:
        cache_file = self._get_cache_file(word_length)
        if cache_file.exists():
            return json.load(cache_file.open())

    def _dump_graph(self, graph: ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH, word_length: int) -> None:
        cache_file = self._get_cache_file(word_length)
        json.dump(graph, cache_file.open(mode="w"), separators=(",", ":"))

    def _is_cached(self, word_length: int) -> bool:
        cache_file = self._get_cache_file(word_length)
        return cache_file.exists()

    def _get_cache_file(self, word_length: int) -> pathlib.Path:
        return self._get_cache_dir() / f"graph-word-size-{word_length}.json"

    def _get_cache_dir(self) -> pathlib.Path:
        path = pathlib.Path(".graphs")
        path.mkdir(exist_ok=True)
        return path
