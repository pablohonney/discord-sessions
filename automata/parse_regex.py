from string import ascii_letters, digits

literals = ascii_letters + digits + ' '


def lit(value: str) -> dict:
    return {
        "op": "literal",
        "value": value
    }


def concat(value1: dict, value2: dict) -> dict:
    return {
        "op": "concat",
        "value1": value1,
        "value2": value2
    }


def or_(value1: dict, value2: dict) -> dict:
    return {
        "op": "or",
        "value1": value1,
        "value2": value2
    }


def star(value: dict) -> dict:
    return {
        "op": "star",
        "value": value
    }


def find_group(regex: str) -> tuple[str, str]:
    bracket_count = 0
    for i, char in enumerate(regex):
        if char == "(":
            bracket_count += 1
        if char == ")":
            bracket_count -= 1
        if bracket_count == 0:
            if not regex[i + 1:]:
                return regex[1:i], regex[i + 1:]
    raise RuntimeError


def find_char_class(regex: str) -> tuple[str, str]:
    bracket_count = 0
    for i, char in enumerate(regex):
        if char == "[":
            bracket_count += 1
        if char == "]":
            bracket_count -= 1
        if bracket_count == 0:
            if not regex[i + 1:]:
                return regex[1:i], regex[i + 1:]
    raise RuntimeError


def parse_regex(regex: str) -> dict:
    if len(regex) == 0:
        return lit("")

    if len(regex) == 1:
        return lit(regex)

    if regex[0] == "(":
        group, rest = find_group(regex)
        regex = [parse_regex(group), rest]

    if isinstance(regex[0], dict) or regex[0] in literals:
        if regex[0] in literals:
            left = lit(regex[0])
        else:
            left = regex[0]
            regex = regex[1]

        if regex[1] == "*":
            if not regex[2:]:
                return star(left)

            return concat(
                star(left),
                parse_regex(regex[2:])
            )
        if regex[1] == "|":
            return or_(
                left,
                parse_regex(regex[2:])
            )
        if regex[1] != "*":
            return concat(
                left,
                parse_regex(regex[1:])
            )


assert parse_regex("a") == {'op': 'literal', 'value': 'a'}
assert parse_regex("ab") == {
    'op': 'concat',
    'value1': {'op': 'literal', 'value': 'a'},
    'value2': {'op': 'literal', 'value': 'b'}
}
assert parse_regex("a*") == {
    'op': 'star',
    'value': {'op': 'literal', 'value': 'a'}
}
assert parse_regex("(a)") == {'op': 'literal', 'value': 'a'}
assert parse_regex("(ab)") == {
    'op': 'concat',
    'value1': {'op': 'literal', 'value': 'a'},
    'value2': {'op': 'literal', 'value': 'b'}
}
assert parse_regex("(a*)") == {
    'op': 'star',
    'value': {'op': 'literal', 'value': 'a'}
}
# print(parse_regex("(a)*"))
