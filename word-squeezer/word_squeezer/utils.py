import typing as t
from pathlib import Path


def read_wordlist(word_list_path: Path) -> t.List[str]:
    return open(word_list_path).read().split("\n")
