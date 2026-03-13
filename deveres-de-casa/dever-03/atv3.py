"""Recursive palindrome checker for arrays.

This module provides a recursive function to verify if an array
(list) is a palindrome or not.
"""

def is_palindrome(arr, start=0, end=None):
    """
    Check if an array is a palindrome using recursion.

    A palindrome is a sequence that reads the same forward and backward.

    Args:
        arr: The list to check.
        start: The starting index for comparison (default: 0).
        end: The ending index for comparison (default: len(arr) - 1).

    Returns:
        True if the array is a palindrome, False otherwise.
    """
    if end is None:
        end = len(arr) - 1

    # Base case: if start >= end, we've checked all pairs
    if start >= end:
        return True

    # If current pair doesn't match, it's not a palindrome
    if arr[start] != arr[end]:
        return False

    # Recursive case: check the inner elements
    return is_palindrome(arr, start + 1, end - 1)


if __name__ == "__main__":
    # Test cases
    test_cases = [
        [1, 2, 3, 2, 1],
        ['a', 'b', 'c', 'b', 'a'],
        [1, 2, 3, 4],
        [],
        [1],
        ['r', 'a', 'd', 'a', 'r'],
        [0,1,2,3,2,1,0],
        ['a','b','b','a'],
        ['a','b','c','f','b','a']
    ]

    for test in test_cases:
        result = is_palindrome(test)
        print(f"{test} -> {'Palindrome' if result else 'Not a palindrome'}")
