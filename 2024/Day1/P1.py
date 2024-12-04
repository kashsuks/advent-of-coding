def calcDistance(leftArr, rightArr):
    sortedL = sorted(leftArr)
    sortedR = sorted(rightArr)
    
    maxLen = max(len(sortedL), len(sortedR))
    sortedL += [0] * (maxLen - len(sortedL))
    sortedR += [0] * (maxLen - len(sortedR))
    
    total = sum(abs(left - right) for left, right in zip(sortedL, sortedR))
    
    return total

def parseID(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
        leftArr = []
        rightArr = []
        
        for line in lines:
            left, right = map(int, line.strip().split())
            leftArr.append(left)
            rightArr.append(right)
        
        return leftArr, rightArr

def solveDistance():
    leftArr, rightArr = parseID('input.txt')
    total = calcDistance(leftArr, rightArr)
    
    return total

result = solveDistance()
print(f"Total distance between lists: {result}")