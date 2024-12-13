import re
from functools import cache

# the fact that the stones are in order is not relevant to 
# solving the problem, so we can throw that piece away
@cache
def total_stones(value, turns_remaining):
    while turns_remaining > 0:
        if value == 0:
            value = 1
            turns_remaining -= 1
        elif len(str(value)) % 2 == 0:
            first_half = str(value)[:len(str(value)) // 2]
            second_half = str(value)[len(str(value)) // 2:]
            turns_remaining -= 1
            total = 0
            total += total_stones(int(first_half), turns_remaining)
            total += total_stones(int(second_half), turns_remaining)
            return total
        else:
            value = value * 2024
            turns_remaining -= 1
    return 1

        
# input = '0 1 10 99 999'
# input = '125 17'
with open('input.txt', 'r') as f:
    input = f.read()

input_list = list(map(int, re.findall(r'\d+', input)))
turns = 75
total = 0
for n in input_list:
    total += total_stones(n, turns)
print(total)