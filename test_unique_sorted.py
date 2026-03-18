import pytest
from utils import unique_sorted

def test_unique_sorted_bug():
    # Test cases that should expose the bug
    # The bug occurs when there are 3 or more consecutive duplicates
    
    # Case 1: Three identical elements
    assert unique_sorted([1, 1, 1]) == [1], f"Expected [1], got {unique_sorted([1, 1, 1])}"
    
    # Case 2: More than three identical elements
    assert unique_sorted([2, 2, 2, 2]) == [2], f"Expected [2], got {unique_sorted([2, 2, 2, 2])}"
    
    # Case 3: Three identical elements followed by different elements
    assert unique_sorted([1, 1, 1, 2, 3]) == [1, 2, 3], f"Expected [1, 2, 3], got {unique_sorted([1, 1, 1, 2, 3])}"
    
    # Case 4: Different elements followed by three identical elements
    assert unique_sorted([1, 2, 3, 3, 3]) == [1, 2, 3], f"Expected [1, 2, 3], got {unique_sorted([1, 2, 3, 3, 3])}"
    
    # Case 5: Multiple groups of three identical elements
    assert unique_sorted([1, 1, 1, 2, 2, 2, 3]) == [1, 2, 3], f"Expected [1, 2, 3], got {unique_sorted([1, 1, 1, 2, 2, 2, 3])}"
    
    # Case 6: Mixed case that might work correctly (to show we understand when it works)
    assert unique_sorted([1, 1, 2, 2]) == [1, 2], f"Expected [1, 2], got {unique_sorted([1, 1, 2, 2])}"
    assert unique_sorted([1, 2, 2, 3]) == [1, 2, 3], f"Expected [1, 2, 3], got {unique_sorted([1, 2, 2, 3])}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])