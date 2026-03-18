from hypothesis import given, assume, strategies as st
from hypothesis import settings, HealthCheck
from utils import clamp, merge_sorted

# Test for clamp
@given(st.integers(), st.integers(), st.integers())
def test_clamp_in_bounds(x, lo, hi):
    assume(lo <= hi)
    result = clamp(x, lo, hi)
    assert lo <= result <= hi

@given(st.integers(), st.integers(), st.integers())
def test_clamp_idempotence(x, lo, hi):
    assume(lo <= hi)
    once = clamp(x, lo, hi)
    twice = clamp(once, lo, hi)
    assert twice == once

@given(st.integers(), st.integers(), st.integers())
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_clamp_no_op_when_in_range(x, lo, hi):
    assume(lo <= hi)
    assume(lo <= x <= hi)
    assert clamp(x, lo, hi) == x

# Test for merge_sorted
sorted_lists = st.lists(st.integers()).map(sorted)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_is_sorted(a, b):
    result = merge_sorted(a, b)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(sorted_lists, sorted_lists)
def test_merge_sorted_length(a, b):
    result = merge_sorted(a, b)
    assert len(result) == len(a) + len(b)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_permutation(a, b):
    result = merge_sorted(a, b)
    assert sorted(result) == sorted(a + b)