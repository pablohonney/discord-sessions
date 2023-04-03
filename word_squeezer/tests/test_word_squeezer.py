from ..squeeze import (
    Trie,
    WordSqueezer,
)


def test_word_squeezer():
    trie = Trie("black white yellow groin mignon minor morin brown grey red".split())
    ws = WordSqueezer(trie)

    squeezed_words = ws.squeeze("morning")
    assert squeezed_words == "groin mignon minor morin".split()
