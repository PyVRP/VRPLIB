def text2lines(text: str) -> list[str]:
    """
    Takes a string and returns a list of non-empty, stripped lines. Also
    removes any comment lines from the given string.
    """
    return [
        stripped
        for line in text.splitlines()
        if (stripped := line.strip()) and not stripped.startswith("#")
    ]


def infer_type(s: str) -> int | float | str:
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s
