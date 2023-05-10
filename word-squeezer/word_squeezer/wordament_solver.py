import typing as t
from pathlib import Path
import argparse
import textwrap

from .trie import Trie
from .utils import read_wordlist

WordGrid = t.List[t.List[str]]


class WordamentSolver:
    """Microsoft Wordament solver"""

    def __init__(self, trie: Trie):
        self.trie = trie

    def squeeze(self, word_grid: WordGrid) -> t.List[str]:
        return list(self._squeeze_raw(word_grid))

    def _squeeze_raw(self, word_grid: WordGrid) -> t.Iterable[str]:
        for start_head in self._get_start_heads(word_grid):
            yield from self._traverse_grid(word_grid, [start_head])

    def _traverse_grid(
        self, word_grid: WordGrid, path: t.List[t.Tuple[int, int]] = None
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

    def _is_position_in_grid(
        self, word_grid: WordGrid, position: t.Tuple[int, int]
    ) -> bool:
        i, j = position
        i_max = len(word_grid)
        j_max = len(word_grid[0])
        return 0 <= i < i_max and 0 <= j < j_max

    def _get_path_string(
        self, word_grid: WordGrid, path: t.List[t.Tuple[int, int]]
    ) -> str:
        return "".join(word_grid[i][j] for (i, j) in path)

    def _get_start_heads(self, word_grid: WordGrid) -> t.Iterable[t.Tuple[int, int]]:
        i_max = len(word_grid)
        j_max = len(word_grid[0])

        for i in range(i_max):
            for j in range(j_max):
                yield i, j


def solve_wordament(
    word_grid: WordGrid, wordlist: t.List[str], target_word_length: int = None
):
    if target_word_length:
        wordlist = filter(lambda x: len(x) >= target_word_length, wordlist)

    trie = Trie(list(wordlist))
    ws = WordamentSolver(trie)

    squeezed_words = ws.squeeze(word_grid)

    for word in squeezed_words:
        print(word)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
    Wordament is an online word puzzle from Microsoft, where users need to find words from a word grid.
    The words need to be continuous in the grid, including diagonal, without jumps."
    
    example:
        l r t l
        f a a n
        g c s t
        l e e l"""
        ),
    )

    parser.add_argument(
        "word_grid",
        type=str,
        help="Word grid, input example: 'l r t l|f a a n|g c s t|l e e l'",
    )
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

    def parse_word_grid(s: str) -> WordGrid:
        lines = s.split("|")
        return [line.split() for line in lines]

    solve_wordament(
        parse_word_grid(args.word_grid),
        read_wordlist(args.word_list_file),
        args.minimum_word_length,
    )


if __name__ == "__main__":
    main()
