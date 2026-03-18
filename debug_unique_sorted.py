from utils import unique_sorted

# Demonstrate the bug
print("Testing unique_sorted with bug:")
print(f"unique_sorted([1, 1, 1]) = {unique_sorted([1, 1, 1])}  # Expected [1]")
print(f"unique_sorted([2, 2, 2, 2]) = {unique_sorted([2, 2, 2, 2])}  # Expected [2]")
print(f"unique_sorted([1, 1, 1, 2, 3]) = {unique_sorted([1, 1, 1, 2, 3])}  # Expected [1, 2, 3]")

# Show cases that work correctly
print("\nCases that work correctly:")
print(f"unique_sorted([1, 1, 2, 2]) = {unique_sorted([1, 1, 2, 2])}  # Expected [1, 2]")
print(f"unique_sorted([1, 2, 2, 3]) = {unique_sorted([1, 2, 2, 3])}  # Expected [1, 2, 3]")
print(f"unique_sorted([1, 2, 3]) = {unique_sorted([1, 2, 3])}  # Expected [1, 2, 3]")