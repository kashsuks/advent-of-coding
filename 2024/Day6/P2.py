from collections import deque
from tqdm import tqdm

FILENAME = "input.txt"
START = "^"
OBSTACLE = "#"
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(filename):
    with open(filename, "r") as input_file:
        return [list(row) for row in input_file.read().split("\n")]


def find_start(lab):
    for i, row in enumerate(lab):
        for j, pos in enumerate(row):
            if pos == START:
                return i, j


def is_out(row, col, lab):
    return row in {-1, len(lab)} or col in {-1, len(lab[0])}


def part_one(lab, start):
    dirs = deque(DIRECTIONS)
    visited = set()
    row, col = start
    while True:
        visited.add((row, col))
        dr, dc = dirs[0]
        new_row, new_col = row + dr, col + dc
        if is_out(new_row, new_col, lab):
            return visited
        if lab[new_row][new_col] == OBSTACLE:
            dirs.rotate(-1)
            continue
        row, col = new_row, new_col


def check_loop(lab, start, obstacle):
    dirs = deque(DIRECTIONS)
    visited = set()
    row, col = start
    while (row, col, dirs[0]) not in visited:
        visited.add((row, col, dirs[0]))
        dr, dc = dirs[0]
        new_row, new_col = row + dr, col + dc
        if is_out(new_row, new_col, lab):
            return False
        if lab[new_row][new_col] == OBSTACLE or (new_row, new_col) == obstacle:
            dirs.rotate(-1)
            continue
        row, col = new_row, new_col
    return True


def part_two(lab, start, visited):
    counter = 0
    for i, row in tqdm(enumerate(lab)):
        for j, pos in enumerate(row):
            if (i, j) == start or (i, j) not in visited:
                continue
            if check_loop(lab, start, (i, j)):
                counter += 1
    return counter


def main():
    lab = parse_input(FILENAME)
    start = find_start(lab)
    visited = part_one(lab, start)
    print(part_two(lab, start, visited))


if __name__ == "__main__":
    main()
