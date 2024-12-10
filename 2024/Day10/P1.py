import numpy as np

def find_trail(t):
    # input: coordinates of current location on the map
    # output: updates global list of endpoints if we 
    # reach a space containing 9
    for s in [(-1,0), (1,0), (0,-1), (0,1)]:
        next_move = (s[0] + t[0], s[1] + t[1])
        if next_move[0] < 0 or next_move[0] >= rows \
            or next_move[1] < 0 or next_move[1] >= cols:
            continue
        if topo_map[next_move] == topo_map[t] + 1:
            if topo_map[next_move] == 9:
                endpoints.add(next_move)
            else:
                find_trail(next_move)

                     
with open('input.txt', 'r') as f:
    lines = f.read().split('\n')

rows = len(lines)
cols = len(lines[0])
trailheads = set()
topo_map = np.empty((rows, cols), dtype=int)
for i, L in enumerate(lines):
    for j, c in enumerate(L):
        topo_map[i,j] = int(c)
        if c == '0':
            trailheads.add((i,j))

total = 0
for t in trailheads:
    endpoints = set()
    find_trail(t)
    total += len(endpoints)
print(total)