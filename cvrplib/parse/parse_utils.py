from typing import List


def text2lines(text: str) -> List[str]:
    """
    Takes a text and returns a list of non-empty, stripped lines.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def infer_type(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s
