import re

def solve():
    with open("input.txt", "r") as file:
        data = file.read()

    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, data)

    total = 0
    for match in matches:
        x, y = int(match[0]), int(match[1])
        total += x * y

    print(total)

solve()
