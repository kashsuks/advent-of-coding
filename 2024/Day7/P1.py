from collections import namedtuple
from pathlib import Path
from operator import add, mul

def concat(x, y): return int(str(x) + str(y))

text = Path('input.txt').read_text('utf-8')

def process(operators: list[callable]) -> int:
    data = [
        (int(data[0][:-1]), list(map(int, data[1:])))
        for data in [line.split() for line in text.splitlines()]]

    result = 0
    operator_count = len(operators)

    for target, values in data:
        value_count = len(values)

        for p in range(operator_count ** (value_count - 1)):
            value = values[0]

            for j in range(1, value_count):
                p, r = divmod(p, operator_count)
                value = operators[r](value, values[j])

            if value == target:
                result += target
                break

    return result

print("Part 1:", process(operators=[add, mul]))