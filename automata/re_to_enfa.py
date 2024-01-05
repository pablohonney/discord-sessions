from enfa import EpsilonNFA, NFATuple, EPSILON

from functools import reduce


def concate_two_nfas(nfa1: NFATuple, nfa2: NFATuple) -> NFATuple:
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


def concat_nfas(nfas: list[NFATuple]) -> NFATuple:
    return reduce(concate_two_nfas, nfas)


class RegexToEpsilonNFA:
    def __init__(self):
        self._state_counter = -1

    def new_q(self) -> str:
        self._state_counter += 1
        return f"q{self._state_counter}"

    def alternate_two_nfas(self, nfa1: NFATuple, nfa2: NFATuple) -> NFATuple:
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

    def alternate_nfas(self, enfas: list[NFATuple]) -> NFATuple:
        return reduce(self.alternate_two_nfas, enfas)

    def repeat_nfa(self, nfa: NFATuple) -> NFATuple:
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

    def compile(self, regex: str) -> NFATuple:
        if len(regex) in [0, 1]:
            q0 = self.new_q()
            qf = self.new_q()

            return NFATuple(
                Q={q0, qf},
                S={regex},
                T={
                    q0: {
                        regex: {qf}
                    }
                },
                q0=q0,
                F={qf}
            )

        elif regex.isalnum():
            nfas = list(map(self.compile, regex))
            return concat_nfas(nfas)
        elif "|" in regex:
            alternatives = regex.split("|")
            nfas = list(map(self.compile, alternatives))
            return self.alternate_nfas(nfas)
        elif regex[1] == "*":
            regex_star, rest_regex = regex.split('*', maxsplit=1)
            kleene_nfa = self.repeat_nfa(self.compile(regex_star))
            return concate_two_nfas(kleene_nfa, self.compile(rest_regex))
        elif regex[1] == "+":
            regex_plus, rest_regex = regex.split('+', maxsplit=1)
            rewritten_regex = regex_plus + regex_plus + "*" + rest_regex
            return self.compile(rewritten_regex)
        elif regex[1] == "?":
            regex_que, rest_regex = regex.split('?', maxsplit=1)
            rewritten_regex = f"({regex_que}|)" + rest_regex
            return self.compile(rewritten_regex)


def compile(regex: str) -> EpsilonNFA:
    return EpsilonNFA(RegexToEpsilonNFA().compile(regex))


if __name__ == "__main__":
    nfa = compile("a")
    assert nfa.accept("a")
    assert not nfa.accept("b")

    nfa = compile("abb")
    assert not nfa.accept("a")
    assert not nfa.accept("b")
    assert not nfa.accept("ab")
    assert not nfa.accept("aba")
    assert nfa.accept("abb")

    nfa = compile("a|b")
    assert nfa.accept("a")
    assert nfa.accept("b")

    nfa = compile("a|b|c")
    assert nfa.accept("a")
    assert nfa.accept("b")
    assert nfa.accept("c")

    nfa = compile("aa|b|cad")
    assert nfa.accept("aa")
    assert nfa.accept("b")
    assert nfa.accept("cad")

    nfa = compile("a*")
    assert nfa.accept("")
    assert nfa.accept("a")
    assert nfa.accept("aa")

    nfa = compile("a+")
    assert not nfa.accept("")
    assert nfa.accept("a")
    assert nfa.accept("aa")

    nfa = compile("a?")
    assert nfa.accept("")
    assert nfa.accept("a")
    assert not nfa.accept("aa")
