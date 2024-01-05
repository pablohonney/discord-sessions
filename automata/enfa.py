from nfa import NFATuple, NFA

EPSILON = ""


class EpsilonNFA(NFA):
    def _extend_epsilon_links(self, states: set[str]) -> set[str]:
        while True:
            new_states = self.u_delta(states, EPSILON) | states
            if new_states == states:
                break
            else:
                states = new_states
        return states

    def extended_delta(self, state: str, text: str) -> set[str]:
        states = {state}
        states = self._extend_epsilon_links(states)
        for char in text:
            states = self.u_delta(states, char)
            states = self._extend_epsilon_links(states)
        return states


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
            },
            "q2": {
                "": {"q3"}
            }
        },
        q0="q0",
        F={"q3"}
    )

    nfa = EpsilonNFA(nfa_tuple)

    assert nfa.accept("00101") is True

    nfa_tuple = NFATuple(
        Q={"q0", "q1", "q2"},
        S={EPSILON},
        T={
            "q0": {
                EPSILON: {"q1"},
            },
            "q1": {
                EPSILON: {"q2"}
            },
            "q2": {
                EPSILON: {"q3"}
            }
        },
        q0="q0",
        F={"q3"}
    )

    nfa = EpsilonNFA(nfa_tuple)

    assert nfa.accept("") is True
