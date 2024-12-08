from itertools import combinations
from math import gcd

with open('input.txt', 'r') as f:
    lines = f.read().split()

rows = len(lines)
cols = len(lines[0])
antennas = {}
for i, L in enumerate(lines):
    for j, c in enumerate(lines[i]):
        if c != '.':
            if c in antennas.keys():
                antennas[c].add((i,j))
            else:
                antennas[c] = {(i,j)}

# problem is to find all integer values on line
# connecting two antennas
antinodes = set()
for k in antennas.keys():
    for a1, a2 in combinations(antennas[k], 2):
        # find difference in position between antennas
        delta_row = a2[0] - a1[0]
        delta_col = a2[1] - a1[1]
        # see if there is a point with integer coordinates
        # lying between these antennas
        divisor = gcd(delta_row, delta_col)
        delta_row = delta_row / divisor
        delta_col = delta_col / divisor

        # find all points with integer coordinates lying on
        # the line connecting the two antennas
        n = 0
        while 0 <= a1[0] + n * delta_row < rows and 0 <= a1[1] + n * delta_col < cols:
            antinodes.add((a1[0] + n * delta_row, a1[1] + n * delta_col))
            n += 1
        n = -1
        while 0 <= a1[0] + n * delta_row < rows and 0 <= a1[1] + n * delta_col < cols:
            antinodes.add((a1[0] + n * delta_row, a1[1] + n * delta_col))
            n -= 1
print(len(antinodes))