from enfa import EpsilonNFA, NFATuple, EPSILON

from functools import reduce


def concat(nfa1: NFATuple, nfa2: NFATuple) -> NFATuple:
    return NFATuple(
        Q=nfa1.Q | nfa2.Q,
        S=nfa1.S | nfa2.S,
        T={
            **nfa1.T,
            **nfa2.T,
            **{f: {
                EPSILON: {nfa2.q0}
            } for f in nfa1.F},
        },
        q0=nfa1.q0,
        F=nfa2.F
    )


class RegexToEpsilonNFA:
    def __init__(self):
        self._state_counter = -1

    def new_q(self) -> str:
        self._state_counter += 1
        return f"q{self._state_counter}"

    def alternate(self, nfa1: NFATuple, nfa2: NFATuple) -> NFATuple:
        q0 = self.new_q()
        qf = self.new_q()

        return NFATuple(
            Q=nfa1.Q | nfa2.Q | {q0, qf},
            S=nfa1.S | nfa2.S | {EPSILON},
            T={
                **nfa1.T,
                **nfa2.T,
                q0: {
                    EPSILON: {nfa1.q0, nfa2.q0}
                },
                **{f: {
                    EPSILON: {qf}
                } for f in nfa1.F | nfa2.F},
            },
            q0=q0,
            F={qf}
        )

    def repeat(self, nfa: NFATuple) -> NFATuple:
        q0 = self.new_q()
        qf = self.new_q()

        return NFATuple(
            Q=nfa.Q | {q0, qf},
            S=nfa.S | {EPSILON},
            T={
                **nfa.T,
                # connect new q0 to old q0
                # connect new q0 to new qf, accept empty string
                q0: {
                    EPSILON: {nfa.q0, qf}
                },
                # connect old F states to the new qf and old q0
                **{f: {
                    EPSILON: {qf, nfa.q0}
                } for f in nfa.F},
            },
            q0=q0,
            F={qf}
        )

    def create_literal(self, value: str) -> NFATuple:
        assert len(value) == 1

        q0 = self.new_q()
        qf = self.new_q()

        return NFATuple(
            Q={q0, qf},
            S={value},
            T={
                q0: {
                    value: {qf}
                }
            },
            q0=q0,
            F={qf}
        )

    def compile(self, regex: dict) -> NFATuple:
        if regex["op"] == "literal":
            return self.create_literal(regex["value"])
        if regex["op"] == "concat":
            return concat(
                self.compile(regex["value1"]),
                self.compile(regex["value2"])
            )
        if regex["op"] == "or":
            return self.alternate(
                self.compile(regex["value1"]),
                self.compile(regex["value2"])
            )
        if regex["op"] == "star":
            return self.repeat(self.compile(regex["value"]))


def compile(regex: dict) -> EpsilonNFA:
    return EpsilonNFA(RegexToEpsilonNFA().compile(regex))


if __name__ == "__main__":
    # ab
    nfa = compile({
        'op': 'concat',
        'value1': {'op': 'literal', 'value': 'a'},
        'value2': {'op': 'literal', 'value': 'b'}
    })
    assert not nfa.accept("a")
    assert not nfa.accept("b")
    assert nfa.accept("ab")

    # (ab)*
    nfa = compile({
        "op": "star",
        "value": {
            'op': 'concat',
            'value1': {'op': 'literal', 'value': 'a'},
            'value2': {'op': 'literal', 'value': 'b'}
        }
    })
    assert not nfa.accept("a")
    assert not nfa.accept("b")
    assert not nfa.accept("aba")
    assert nfa.accept("ab")
    assert nfa.accept("abab")

    # a|b
    nfa = compile({
        'op': 'or',
        'value1': {'op': 'literal', 'value': 'a'},
        'value2': {'op': 'literal', 'value': 'b'}
    })
    assert nfa.accept("a")
    assert nfa.accept("b")
    assert not nfa.accept("ab")

    # a(b|c)*d
    nfa = compile({
        'op': 'concat',
        'value1': {
            'op': 'concat',
            'value1': {'op': 'literal', 'value': 'a'},
            'value2': {
                "op": "star",
                "value": {
                    'op': 'or',
                    'value1': {'op': 'literal', 'value': 'b'},
                    'value2': {'op': 'literal', 'value': 'c'}
                }
            }
        },
        'value2': {'op': 'literal', 'value': 'd'}
    })
    assert nfa.accept("ad")
    assert nfa.accept("abd")
    assert nfa.accept("abbd")
    assert nfa.accept("acd")
    assert nfa.accept("accd")
    assert nfa.accept("abcbbbcccbd")


    # nfa = compile("a")
    # assert nfa.accept("a")
    # assert not nfa.accept("b")
    #
    # nfa = compile("abb")
    # assert not nfa.accept("a")
    # assert not nfa.accept("b")
    # assert not nfa.accept("ab")
    # assert not nfa.accept("aba")
    # assert nfa.accept("abb")
    #
    # nfa = compile("a|b")
    # assert nfa.accept("a")
    # assert nfa.accept("b")
    #
    # nfa = compile("a|b|c")
    # assert nfa.accept("a")
    # assert nfa.accept("b")
    # assert nfa.accept("c")
    #
    # nfa = compile("aa|b|cad")
    # assert nfa.accept("aa")
    # assert nfa.accept("b")
    # assert nfa.accept("cad")
    #
    # nfa = compile("a*")
    # assert nfa.accept("")
    # assert nfa.accept("a")
    # assert nfa.accept("aa")
    #
    # nfa = compile("a+")
    # assert not nfa.accept("")
    # assert nfa.accept("a")
    # assert nfa.accept("aa")
    #
    # nfa = compile("a?")
    # assert nfa.accept("")
    # assert nfa.accept("a")
    # assert not nfa.accept("aa")