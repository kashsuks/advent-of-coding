
class FileBlock:
    def __init__(self, length, id):
        self.length = length
        self.id = id

    def __str__(self):
        return_str = 'Length: ' + str(self.length) + '\n'
        return_str += 'ID: ' + str(self.id) + '\n'
        return return_str


def displayFileSystem():
    for k in sorted(file_system.keys()):
        if file_system[k].id != -1:
            print(str(file_system[k].id) * file_system[k].length, end='')
        else:
            print('.' * file_system[k].length, end='')
    print('')

with open('input.txt', 'r') as f:
    disk_map = f.read()

# file system is a dictionary of FileBlock objects
# the value of the starting cell is the key
# a file block id of -1 indicates an empty block
file_system = {}
id = 0
current_cell = 0
empty_space = False
for m in disk_map:
    n = int(m)
    if not empty_space:
        if n != 0:
            file_system[current_cell] = FileBlock(n, id)
        id += 1
        empty_space = True
    else:
        if n != 0:
            file_system[current_cell] = FileBlock(n, -1)
        empty_space = False
    current_cell += n

# because of 0 inputs, we can have two contiguous, separate blocks
# of empty space that should be a single block
# go through the file system and fix this
cell_list = sorted(file_system.keys())
n = 0
while n < len(cell_list):
    if file_system[cell_list[n]].id != -1:
        n += 1
        continue
    k = 1
    while n + k < len(cell_list) and file_system[cell_list[n+k]].id == -1:
        file_system[cell_list[n]].length += file_system[cell_list[n+k]].length
        del file_system[cell_list[n+k]]
        k += 1
    n += k

# move blocks to occupy free space
cell_list = sorted(file_system.keys())
for b in cell_list[::-1]:
    # find next nonempty block at end of file to move
    if file_system[b].id == -1:
        continue

    # find first empty block at beginning of file with enough length
    for a in sorted(file_system.keys()):
        if a >= b:
            break
        if file_system[a].id == -1 \
            and file_system[a].length >= file_system[b].length:
            file_system[a].id = file_system[b].id
            file_system[b].id = -1

            # if the file we moved did not completely fill the empty
            # space, we create a new file block for whatever space is
            # left over
            if file_system[a].length > file_system[b].length:
                new_start = a + file_system[b].length
                new_length = file_system[a].length - file_system[b].length
                file_system[a].length = file_system[b].length
                file_system[new_start] = FileBlock(new_length, -1)
            break

# calculate checksum
checksum = 0
for k in sorted(file_system.keys()):
    if file_system[k].id == -1:
        continue
    for n in range(k, k + file_system[k].length):
        checksum += file_system[k].id * n
print(checksum)