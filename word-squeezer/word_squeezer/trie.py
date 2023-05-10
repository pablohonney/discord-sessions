import typing as t
from dataclasses import dataclass, field


class Trie:
    """Prefix tree object for efficient word lookup, avoiding exhaustive brute-force character permutations"""

    @dataclass
    class Node:
        is_word: bool = False
        subtrie: dict = field(default_factory=dict)

        @property
        def is_prefix(self) -> bool:
            return bool(self.subtrie)

    # avoid edge-case checks by using a sentinel node
    _sentinel_node = Node()

    def __init__(self, words: t.List[str]):
        self._root = self.Node()

        for word in words:
            self.add(word)

    def add(self, word: str) -> None:
        node = self._root
        for letter in word:
            node = node.subtrie.setdefault(letter, self.Node())
        node.is_word = True

    def __contains__(self, word: str) -> bool:
        return self.get_node(word).is_word

    def is_prefix(self, word: str) -> bool:
        return self.get_node(word).is_prefix

    def get_node(self, word: str) -> Node:
        node = self._root
        for letter in word:
            if letter not in node.subtrie:
                return self._sentinel_node
            node = node.subtrie[letter]
        return node
