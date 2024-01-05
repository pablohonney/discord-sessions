from functools import reduce
from typing import NamedTuple


class NFATuple(NamedTuple):
    Q: set[str]
    S: set[str]
    T: dict[str, dict[str, set[str]]]
    q0: str
    F: set[str]


class NFA:
    def __init__(self, nfa_tuple: NFATuple):
        self.nfa_tuple = nfa_tuple

    def delta(self, state: str, char: str) -> set[str]:
        try:
            return self.nfa_tuple.T[state][char]
        except KeyError:
            return set()

    def u_delta(self, states: set[str], char: str) -> set[str]:
        return reduce(lambda ss, acc: acc | ss, (self.delta(state, char) for state in states), set())

    def extended_delta(self, state: str, text: str) -> set[str]:
        states = {state}
        for char in text:
            states = self.u_delta(states, char)
        return states

    def accept(self, text: str) -> bool:
        return len(self.extended_delta(self.nfa_tuple.q0, text) & self.nfa_tuple.F) != 0


if __name__ == "__main__":
    nfa_tuple = NFATuple(
        Q={"q0", "q1", "q2"},
        S={"0", "1"},
        T={
            "q0": {
                "0": {"q0", "q1"},
                "1": {"q0"}
            },
            "q1": {
                "1": {"q2"}
            }
        },
        q0="q0",
        F={"q2"}
    )

    nfa = NFA(nfa_tuple)

    assert nfa.accept("00101") is True
