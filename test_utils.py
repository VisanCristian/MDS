import pytest
from utils import clamp, merge_sorted, parse_pair

def test_clamp():
    # Inside range
    assert clamp(5, 0, 10) == 5
    # Outside below
    assert clamp(-5, 0, 10) == 0
    # Outside above
    assert clamp(15, 0, 10) == 10
    # Exactly on boundaries
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10
    # lo == hi
    assert clamp(5, 5, 5) == 5
    assert clamp(3, 5, 5) == 5  # below -> returns lo (5)
    assert clamp(7, 5, 5) == 5  # above -> returns hi (5)

def test_merge_sorted():
    # Normal case
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    # One list empty
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted([1, 2, 3], []) == [1, 2, 3]
    # Both empty
    assert merge_sorted([], []) == []
    # Duplicates across them
    assert merge_sorted([1, 2, 2, 3], [2, 4]) == [1, 2, 2, 2, 3, 4]

def test_parse_pair():
    # Valid inputs
    assert parse_pair("3:4") == (3, 4)
    assert parse_pair("0:0") == (0, 0)
    assert parse_pair("-1:5") == (-1, 5)
    assert parse_pair("10:-3") == (10, -3)
    # Invalid inputs: not exactly one colon
    with pytest.raises(ValueError):
        parse_pair("3")
    with pytest.raises(ValueError):
        parse_pair("3:4:5")
    with pytest.raises(ValueError):
        parse_pair("")
    # Invalid inputs: non-integer parts
    with pytest.raises(ValueError):
        parse_pair("a:b")
    with pytest.raises(ValueError):
        parse_pair("3:a")
    with pytest.raises(ValueError):
        parse_pair("a:3")