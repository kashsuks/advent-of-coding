def calcDistance(leftList, rightList):
    sortedLeft = sorted(leftList)
    sortedRight = sorted(rightList)
    
    maxLength = max(len(sortedLeft), len(sortedRight))
    sortedLeft += [0] * (maxLength - len(sortedLeft))
    sortedRight += [0] * (maxLength - len(sortedRight))
    
    totalDistance = sum(abs(left - right) for left, right in zip(sortedLeft, sortedRight))
    
    return totalDistance

def parseIds(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
        leftList = []
        rightList = []
        
        for line in lines:
            left, right = map(int, line.strip().split())
            leftList.append(left)
            rightList.append(right)
        
        return leftList, rightList

def solveDistance():
    leftList, rightList = parseIds('input.txt')
    totalDistance = calcDistance(leftList, rightList)
    
    return totalDistance

result = solveDistance()
print(f"Total distance between lists: {result}")
