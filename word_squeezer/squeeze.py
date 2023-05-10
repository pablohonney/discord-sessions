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


class WordamentSqueezer:
    """Microsoft Wordament solver"""

    def __init__(self, trie: Trie):
        self.trie = trie

    def squeeze(self, word_grid: t.List[t.List[str]]) -> t.List[str]:
        return list(self._squeeze_raw(word_grid))

    def _squeeze_raw(self, word_grid: t.List[t.List[str]]) -> t.Iterable[str]:
        """squeeze_raw may return duplicate words"""
        path = [(0, 0)]
        yield from self._traverse_grid(word_grid, path)

        path = [(1, 0)]
        yield from self._traverse_grid(word_grid, path)

    # 1. pick next position [how, shall we use the same clockwise method?]
    # 2. look around clockwise
    # 3. if new position is not in the path, add the slot to the path
    # 4. if the path is a word in trie, yield it
    # 5. if the path is a prefix in trie, repeat the loop to loop from 1
    def _traverse_grid(
            self, word_grid: t.List[t.List[str]], path: t.List[t.Tuple[int, int]] = None
    ):
        path_head = path[-1]
        for new_head in self.walk_around(path_head[0], path_head[1]):
            # check if new_head is in the grid bounds
            if not self._is_position_in_grid(word_grid, new_head):
                continue
            # check if new_head is not already in the path
            if new_head in path:
                continue

            new_path = path + [new_head]
            path_string = self._get_path_string(word_grid, new_path)

            node = self.trie.get_node(path_string)
            if node.is_word:
                yield path_string

            if node.is_prefix:
                yield from self._traverse_grid(word_grid, new_path)

    @staticmethod
    def walk_around(i: int, j: int) -> t.List[t.Tuple[int, int]]:
        # return surrounding 2-D positions of a slot (i, j)
        # x  x  x
        # x i,j x
        # x  x  x
        deltas = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]
        return [(i + delta_i, j + delta_j) for (delta_i, delta_j) in deltas]

    def _is_position_in_grid(self, word_grid: t.List[t.List[str]], position: t.Tuple[int, int]) -> bool:
        i, j = position
        i_max = len(word_grid)
        j_max = len(word_grid[0])
        return 0 <= i < i_max and 0 <= j < j_max

    def _get_path_string(
            self, word_grid: t.List[t.List[str]], path: t.List[t.Tuple[int, int]]
    ) -> str:
        return "".join(word_grid[i][j] for (i, j) in path)


def main(source_word: str, wordlist: t.List[str], target_word_length: int = None):
    # exclude the source word itself
    wordlist = filter(lambda x: x != source_word, wordlist)

    if target_word_length:
        wordlist = filter(lambda x: len(x) >= target_word_length, wordlist)

    trie = Trie(list(wordlist))
    ws = WordSqueezer(trie)

    squeezed_words = ws.squeeze(source_word)

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
