from collections import defaultdict
from itertools import product

from nfa import NFATuple, NFA
from dfa import DFATuple, DFA


# TODO
def dfa_to_nfa(dfa_tuple: DFATuple) -> NFATuple:
    dfa = DFA(dfa_tuple)

    dfa_delta_table = defaultdict(dict)

    return NFATuple(
        Q=set(dfa_delta_table.keys()),
        S=nfa_tuple.S,
        T=dfa_delta_table,
        q0=nfa_tuple.q0,
        F=set(q for q in dfa_delta_table.keys() if set(q.split(",")) & nfa_tuple.F),
    )


if __name__ == "__main__":
    dfa_tuple = DFATuple(
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

    nfa_tuple = dfa_to_nfa(dfa_tuple)

    nfa = NFA(nfa_tuple)
    dfa = DFA(dfa_tuple)

    for i in range(6):
        for string in product(nfa_tuple.S, repeat=i):
            string = ''.join(string)
            assert nfa.accept(string) == dfa.accept(string)
