def find_all_subsequences(s: str) -> list[str]:
    result = []

    def helper(index: int, current: str) -> None:
        # We've processed all characters in the string
        if index == len(s):
            if current:  # Only add non-empty subsequences
                result.append(current)
            return

        # Choice 1: Include s[index] in the subsequence
        helper(index + 1, current + s[index])

        # Choice 2: Exclude s[index] from the subsequence
        helper(index + 1, current)

    helper(0, "")
    return result


if __name__ == "__main__":
    test_string = "claude"
    subsequences = find_all_subsequences(test_string)

    print(f"String: '{test_string}'")
    print(f"Total subsequences: {len(subsequences)}")
    print(f"Subsequences: {subsequences}")

