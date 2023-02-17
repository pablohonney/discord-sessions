import typing as t
from collections import deque
import sys

from dijkstar import Graph as DijkstarGraph, find_path, NoPathError

VOCAB = t.List[str]
ORTHOGRAPHIC_NEIGHBORHOOD = t.List[str]
ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH = t.Dict[str, ORTHOGRAPHIC_NEIGHBORHOOD]
WORD_PATH = t.List[str]


def check_metagram(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        raise ValueError("metagrams must have the same length")

    # count bool true for 1, when true is not equal pair of letters
    replace_distance = sum(l1 != l2 for l1, l2 in zip(word1, word2))
    return replace_distance == 1


def find_orthographic_neighborhood(
        word: str, vocab: t.List[str]
) -> ORTHOGRAPHIC_NEIGHBORHOOD:
    return list(filter(lambda candidate: check_metagram(word, candidate), vocab))


# TODO too slow, dump computed results for later fast loading, flag?
def build_orthographic_neighborhood_graph(
        vocab: VOCAB, word_length: int
) -> ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH:
    vocab = list(
        filter(lambda w: len(w) == word_length, vocab)
    )  # TODO can be optimized?

    orthographic_neighborhood_graph = {
        w: find_orthographic_neighborhood(w, vocab) for w in vocab
    }
    return orthographic_neighborhood_graph


# use breadth-first-search
def is_word_chain(
        word1: str, word2: str, graph: ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH
) -> bool:
    q = deque([word1])
    seen = set()

    while q:
        w = q.popleft()
        if w == word2:
            return True

        seen.add(w)
        for neighbor in graph.get(w, []):
            if neighbor not in seen:
                q.append(neighbor)
    return False


# use depth-first-search to keep track of the path
def find_word_chain(
        word1: str, word2: str, graph: ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH
) -> WORD_PATH:
    return _find_word_chain(word1, word2, graph, set())


def _find_word_chain(
        word1: str, word2: str, graph: ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH, seen: set
) -> WORD_PATH:
    seen.add(word1)
    for neighbor in graph.get(word1, []):
        if neighbor in seen:
            continue

        if neighbor == word2:
            return [word1, word2]

        path = _find_word_chain(neighbor, word2, graph, seen)
        if path:
            return [word1] + path

    return []


def read_system_vocab() -> VOCAB:
    if sys.platform == "darwin":
        word_list_path = "/usr/share/dict/words"
    else:
        raise FileNotFoundError(f"Could not find system word list for {sys.platform}")

    return open(word_list_path).read().split("\n")


def build_dijkstra_graph(graph: ORTHOGRAPHIC_NEIGHBORHOOD_GRAPH) -> DijkstarGraph:
    d_graph = DijkstarGraph()
    for word, neighbors in graph.items():
        for neighbor in neighbors:
            d_graph.add_edge(
                word, neighbor, 1
            )

    return d_graph


# use Dijkstra's shortest path approach
def find_shortest_word_chain(
        word1: str, word2: str, graph: DijkstarGraph
) -> WORD_PATH:
    if len(word1) != len(word2):
        raise ValueError("metagrams must have the same length")

    try:
        return find_path(graph, word1, word2).nodes
    except NoPathError:
        return []
