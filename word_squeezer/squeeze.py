import typing as t
from dataclasses import dataclass, field
from pathlib import Path
import argparse


def read_system_vocab(word_list_path: Path) -> t.List[str]:
    return open(word_list_path).read().split("\n")


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


class WordSqueezer:
    def __init__(self, trie: Trie):
        self.trie = trie

    def squeeze(self, word: str) -> t.List[str]:
        """squeeze returns unique and sorted words"""
        return sorted(set(self._squeeze_raw(word)))

    def _squeeze_raw(self, word: str) -> t.Iterable[str]:
        """squeeze_raw may return duplicate words"""
        yield from self._permute_and_check(word)

    def _permute_and_check(self, letters: str, prefix: str = "") -> t.Iterable[str]:
        # incrementally produce prefixes from character permutations.
        for i, letter in enumerate(letters):
            new_word = prefix + letter

            node = self.trie.get_node(new_word)
            if node.is_word:
                yield new_word

            # check for prospective words starting with the prefix in the prefix tree.
            # if there are no matches with the current prefix we can avoid exhaustive brute-force permutations.
            if node.is_prefix:
                yield from self._permute_and_check(
                    letters[:i] + letters[i + 1:], prefix=new_word
                )


def main(source_word: str, wordlist: t.List[str], target_word_length: int = None):
    # exclude the source word itself
    wordlist = filter(lambda x: x != source_word, wordlist)

    if target_word_length:
        wordlist = filter(lambda x: len(x) >= target_word_length, wordlist)

    tr = Trie(wordlist)
    sq = WordSqueezer(tr)

    squeezed_words = sq.squeeze(source_word)

    for word in squeezed_words:
        print(word)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Word squeezer finds words from the source word's characters"
    )
    parser.add_argument("source_word", type=str, help="Source word")
    parser.add_argument(
        "-f", "--word-list-file", type=Path, required=True, help="Wordlist file path"
    )
    parser.add_argument(
        "-l",
        "--minimum-word-length",
        type=int,
        required=False,
        help="Minimum length of target words",
    )
    args = parser.parse_args()

    main(
        args.source_word,
        read_system_vocab(args.word_list_file),
        args.minimum_word_length,
    )
