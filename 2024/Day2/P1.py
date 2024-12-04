def is_safe(report):
    differences = [abs(report[i] - report[i + 1]) for i in range(len(report) - 1)]
    increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
    decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))
    valid_differences = all(1 <= diff <= 3 for diff in differences)
    return (increasing or decreasing) and valid_differences

with open('input.txt', 'r') as file:
    data = file.readlines()

reports = [list(map(int, line.split())) for line in data]
safe_count = sum(is_safe(report) for report in reports)

print(f"Number of safe reports: {safe_count}")
