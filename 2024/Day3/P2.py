import re
    
string = ""
with open("input.txt") as file:
    string = file.read()

res = 0
matches = re.findall(r'don\'t\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\)', string)
enabled = True

for match in matches:
    if match == 'do()':
        enabled = True
    elif match == 'don\'t()':
        enabled = False
    elif enabled:
        res += [int(a) * int(b) for a, b in [re.findall(r'\d{1,3}', match)]][0]

print(res)