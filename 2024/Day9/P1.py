
class FileBlock:
    def __init__(self, length, id):
        self.length = length
        self.id = id

    def __str__(self):
        return_str = 'Length: ' + str(self.length) + '\n'
        return_str += 'ID: ' + str(self.id) + '\n'
        return return_str

# for debugging
# def displayFileSystem():
#     for k in sorted(file_system.keys()):
#         if file_system[k].id != -1:
#             print(str(file_system[k].id) * file_system[k].length, end='')
#         else:
#             print('.' * file_system[k].length, end='')
#     print('')


with open('input.txt', 'r') as f:
    disk_map = f.read()

# file system is represented as a dictionary of FileBlock objects
# the starting location of each file is the key for the dictionary
# an empty block has an id of -1
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

# move blocks to occupy free space
# we move through file system in two directions,
# a tracks the location of the next empty space as
# we move forward through the file system
# b starts at the end and goes backward, tracking the
# files that we are moving

cell_list = sorted(file_system.keys())
# find first empty space
for c in cell_list:
    if file_system[c].id == -1:
        a = c
        break
# find the first file to move at the end of the drive
b = cell_list.pop()
while file_system[b].id == -1:
    b = cell_list.pop()

while True:
    # move files to empty blocks 
    # three cases depending on whether empty block is 
    # larger, smaller, or the same size compared to
    # the data being moved

    if file_system[a].length < file_system[b].length:
        # empty block is smaller than the file we are moving
        file_system[a].id = file_system[b].id

        # set up a new, smaller file for the data we have not moved yet
        temp_length = file_system[b].length - file_system[a].length
        file_system[b + temp_length] = \
            FileBlock(file_system[b].length - temp_length, -1)
        file_system[b].length = temp_length

        # find the next empty space at the beginning of the drive
        a += file_system[a].length
        while file_system[a].id != -1:
            a += file_system[a].length

    elif file_system[a].length == file_system[b].length:
        # empty block is the same size as the file we are moving
        file_system[a].id = file_system[b].id
        file_system[b].id = -1

        # find the next empty space at the beginning of the drive
        a += file_system[a].length
        while file_system[a].id != -1:
            a += file_system[a].length

        # find the next file to move at the end of the drive
        b = cell_list.pop()
        while file_system[b].id == -1:
            b = cell_list.pop()   

    else:
        # empty block is larger than the file we are moving
        file_system[a].id = file_system[b].id
        file_system[b].id = -1

        # make a new, smaller empty block after the data we moved
        new_cell = a + file_system[b].length
        file_system[new_cell] = \
            FileBlock(file_system[a].length - file_system[b].length, -1)
        file_system[a].length = file_system[b].length
        a = new_cell

        # find the next file to move at the end of the drive
        b = cell_list.pop()
        while file_system[b].id == -1:
            b = cell_list.pop()       

    # check to see if we are done
    if a >= b:
        break

# calculate checksum
checksum = 0
for k in sorted(file_system.keys()):
    if file_system[k].id == -1:
        break
    for n in range(k, k + file_system[k].length):
        checksum += file_system[k].id * n
        # print(file_system[k].id * n)
print(checksum)