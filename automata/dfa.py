from typing import NamedTuple


class DFATuple(NamedTuple):
    Q: set[str]
    S: set[str]
    T: dict[str, dict[str, str]]
    q0: str
    F: set[str]


class DFA:
    def __init__(self, dfa_tuple: DFATuple):
        self.dfa_tuple = dfa_tuple

    def delta(self, state: str, char: str) -> str:
        return self.dfa_tuple.T[state][char]

    def extended_delta(self, state: str, text: str) -> str:
        for char in text:
            state = self.delta(state, char)
        return state

    def accept(self, text: str) -> bool:
        return self.extended_delta(self.dfa_tuple.q0, text) in self.dfa_tuple.F


if __name__ == "__main__":
    dfa_tuple = DFATuple(
        Q={"q0", "q1"},
        S={"0", "1"},
        T={
            "q0": {
                "0": "q0",
                "1": "q1",
            },
            "q1": {
                "0": "q1",
                "1": "q0",
            }
        },
        q0="q0",
        F={"q1"}
    )

    nfa = DFA(dfa_tuple)

    assert nfa.accept("0010") is True
    assert nfa.accept("00101") is False
