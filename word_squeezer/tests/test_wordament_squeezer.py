import pytest

from ..squeeze import (
    Trie,
    WordamentSqueezer,
)


@pytest.fixture
def trie():
    return Trie("black white yellow groin mignon minor morin brown grey red".split())


def test_wordament_squeezer_1_row(trie):
    ws = WordamentSqueezer(trie)

    word_grid = [
        ['r', 'e', 'd'],
    ]

    squeezed_words = ws.squeeze(word_grid)
    assert squeezed_words == ["red"]


def test_wordament_squeezer_2_rows(trie):
    ws = WordamentSqueezer(trie)

    word_grid = [
        ['r', 'e', 'd'],
        ['g', 'o', 'y'],
    ]

    squeezed_words = ws.squeeze(word_grid)
    assert squeezed_words == ["red", "grey"]


def test_walk_around():
    surroundings = list(WordamentSqueezer.walk_around(1, 1))
    assert surroundings == [(1, 2), (2, 1), (1, 0), (0, 1), (2, 0), (0, 2), (2, 2), (0, 0)]
