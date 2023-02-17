from collections import Counter
from pprint import pprint

from metagrams.orthographic_neighborhood import (
    read_system_vocab,
)


def inspect_system_word_list():
    vocab = read_system_vocab()

    pprint(Counter(map(len, vocab)).most_common())


if __name__ == "__main__":
    inspect_system_word_list()
