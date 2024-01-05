from string import ascii_letters, digits

literals = ascii_letters + digits + ' '


def _tokenize(regex: str):
    escaped = False
    index = 0
    while index < len(regex):
        if regex[0] == "\\":
            if not escaped:
                escaped = True
        if regex[0] in literals:
            pass


def tokenize(regex: str):
    return list(_tokenize(regex))


assert tokenize("a") == ["a"]
