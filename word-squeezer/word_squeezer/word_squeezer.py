import typing as t
from pathlib import Path
import argparse

from .trie import Trie
from .utils import read_wordlist


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
                    letters[:i] + letters[i + 1 :], prefix=new_word
                )


def solve_word_squeezer(
    source_word: str, wordlist: t.List[str], target_word_length: int = None
):
    # exclude the source word itself
    wordlist = filter(lambda x: x != source_word, wordlist)

    if target_word_length:
        wordlist = filter(lambda x: len(x) >= target_word_length, wordlist)

    trie = Trie(list(wordlist))
    ws = WordSqueezer(trie)

    squeezed_words = ws.squeeze(source_word)

    for word in squeezed_words:
        print(word)


def main():
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

    solve_word_squeezer(
        args.source_word,
        read_wordlist(args.word_list_file),
        args.minimum_word_length,
    )


if __name__ == "__main__":
    main()
