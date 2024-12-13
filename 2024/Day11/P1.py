
# input = '0 1 10 99 999'
# input = '125 17'
with open('input.txt', 'r') as f:
    input = f.read()
stones = list(map(int, input.split(' ')))

for n in range(25):
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(str(s)) % 2 == 0:
            s_string = str(s)
            new_stones.append(int(s_string[:len(s_string)//2]))
            new_stones.append(int(s_string[len(s_string)//2:]))
        else:
            new_stones.append(s * 2024)
    stones = new_stones
print(len(stones))