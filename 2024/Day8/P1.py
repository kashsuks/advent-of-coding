from itertools import combinations

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

antinodes = set()
for k in antennas.keys():
    for a1, a2 in combinations(antennas[k], 2):
        # find difference in position between antennas
        delta_row = a2[0] - a1[0]
        delta_col = a2[1] - a1[1]

        # each pair generates two antinodes
        antinode_row = a1[0] - delta_row
        antinode_col = a1[1] - delta_col
        if 0 <= antinode_row < rows and 0 <= antinode_col < cols:
            antinodes.add((antinode_row, antinode_col))

        antinode_row = a2[0] + delta_row
        antinode_col = a2[1] + delta_col
        if 0 <= antinode_row < rows and 0 <= antinode_col < cols:
            antinodes.add((antinode_row, antinode_col))
print(len(antinodes))