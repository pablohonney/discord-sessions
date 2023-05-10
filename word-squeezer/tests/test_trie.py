from word_squeezer.trie import Trie


def test_get_node_in_trie():
    trie = Trie("hell hello world".split())

    assert trie.get_node("hel").is_word is False
    assert trie.get_node("hel").is_prefix is True

    assert trie.get_node("hell").is_word is True
    assert trie.get_node("hell").is_prefix is True

    assert trie.get_node("hello").is_word is True
    assert trie.get_node("hello").is_prefix is False


def test_membership_in_trie():
    trie = Trie("hell hello world".split())

    assert "hel" not in trie
    assert "hell" in trie
    assert "hello" in trie
