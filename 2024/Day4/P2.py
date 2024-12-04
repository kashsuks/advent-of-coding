def main(word_search: list[str]) -> int:
    # Now need to look for 3x3 squares of the form [MAS] diagonally in both diagonals (direction agnostic). Two examples:
    # Important observation: 'A' must be in the center. We can use that as a search key to identify potential squares
    total = 0
    i = 1
    while i < len(word_search) - 1:
        j = 1
        while j < len(word_search[i]) - 1:
            if word_search[i][j] == "A":
                # get relevant cells
                top_left = word_search[i - 1][j - 1]
                top_right = word_search[i - 1][j + 1]
                bottom_left = word_search[i + 1][j - 1]
                bottom_right = word_search[i + 1][j + 1]

                if (top_left == "S" and bottom_right == "M") or (
                    top_left == "M" and bottom_right == "S"
                ):
                    if (top_right == "S" and bottom_left == "M") or (
                        top_right == "M" and bottom_left == "S"
                    ):
                        total += 1
            j += 1
        i += 1

    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        word_search = f.read().splitlines()

    print(f"'X-MAS' count: {main(word_search)}")