from collections import defaultdict
from collections.abc import Iterable
import itertools as it

def main(lines: list[str]) -> int:
    line_iter = iter(lines)

    rules: defaultdict[str, set[str]] = defaultdict(set)
    # Compile a set of rules until the first blank line
    for line in line_iter:
        if not line.strip():
            break
        first_page, second_page = line.strip().split("|")
        rules[first_page].add(second_page)

    total = 0
    # For every update in the remaining part of the input
    for line in line_iter:
        update = line.strip().split(",")

        # If any page has a rule forcing a previous page to go after it
        # (i.e. it's not in the correct order)
        if any(
            previous_page in rules[page]
            for previous_page, page in it.combinations(update, r=2)
        ):
            # Put update in order by the rules
            # NOTE This relies on the fact that each update has a unique
            # correct order. Each page in the update has a rule saying
            # it must go before every other page in the update. This
            # means we can sort by how many of those rules there are.
            update = sorted(
                update,
                key=lambda page: len(set(rules[page]) & set(update)),
                reverse=True,
            )
            # Add value of middle page
            total += int(update[len(update) // 2])

    return total


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_lines = file.readlines()

    result_part2 = main(input_lines)
    print(f"Part 2: {result_part2}")