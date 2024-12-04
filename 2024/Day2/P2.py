def is_safe(report):
    differences = [abs(report[i] - report[i + 1]) for i in range(len(report) - 1)]
    increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
    decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))
    valid_differences = all(1 <= diff <= 3 for diff in differences)
    return (increasing or decreasing) and valid_differences

def is_safe_with_dampener(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_safe(modified_report):
            return True
    return False

with open('input.txt', 'r') as file:
    data = file.readlines()

reports = [list(map(int, line.split())) for line in data]
safe_count = sum(is_safe_with_dampener(report) for report in reports)

print(f"Number of safe reports with Problem Dampener: {safe_count}")
