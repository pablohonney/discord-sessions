import argparse

from metagrams.metagram_graph import MetagramGraph
from metagrams.orthographic_neighborhood import read_system_vocab


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("word1")
    parser.add_argument("word2")
    return parser.parse_args()


def main():
    args = get_args()

    vocab = read_system_vocab()
    path = MetagramGraph(vocab).find_word_chain(args.word1, args.word2)
    print(path)


if __name__ == "__main__":
    main()
