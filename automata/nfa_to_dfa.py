from collections import defaultdict
from itertools import product

from nfa import NFATuple, NFA
from dfa import DFATuple, DFA


def powerset_to_state(states: set[str]) -> str:
    return ','.join(sorted(states))


def state_to_powerset(s: str) -> set[str]:
    return set(s.split(","))


# powerset construction
def nfa_to_dfa(nfa_tuple: NFATuple) -> DFATuple:
    nfa = NFA(nfa_tuple)

    dfa_delta_table = defaultdict(dict)

    powerset_queue = [{nfa_tuple.q0}]

    while powerset_queue:
        powerset = powerset_queue.pop()
        for char in nfa_tuple.S:
            new_powerset = nfa.u_delta(powerset, char)

            powerset_as_state = powerset_to_state(powerset)
            new_powerset_as_state = powerset_to_state(new_powerset)

            dfa_delta_table[powerset_as_state][char] = new_powerset_as_state
            if new_powerset_as_state not in dfa_delta_table:
                powerset_queue.append(new_powerset)

    return DFATuple(
        Q=set(dfa_delta_table.keys()),
        S=nfa_tuple.S,
        T=dfa_delta_table,
        q0=nfa_tuple.q0,
        F=set(q for q in dfa_delta_table.keys() if state_to_powerset(q) & nfa_tuple.F),
    )


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

    dfa_tuple = nfa_to_dfa(nfa_tuple)

    nfa = NFA(nfa_tuple)
    dfa = DFA(dfa_tuple)

    for i in range(6):
        for string in product(nfa_tuple.S, repeat=i):
            string = ''.join(string)
            assert nfa.accept(string) == dfa.accept(string)
