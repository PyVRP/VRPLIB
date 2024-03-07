import pytest
from numpy.testing import assert_equal

from vrplib.parse.parse_utils import text2lines


@pytest.mark.parametrize(("text", "expected"), [("", []), ("\n", [])])
def test_empty_lines(text: str, expected: list[str]):
    assert_equal(text2lines(text), expected)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("# test comment", []),
        ("# other comment", []),
        ("123\n#comment", ["123"]),
        ("#\n#", []),
        # Lines are stripped before they're inspected for comments, so this
        # should also be OK:
        (" # comment after whitespace", []),
    ],
)
def test_comments(text: str, expected: list[str]):
    assert_equal(text2lines(text), expected)
