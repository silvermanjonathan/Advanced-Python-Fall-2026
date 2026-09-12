"""Summarize tower readings using our own sweep_tools module."""

import sweep_tools

readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

print(f"total {sweep_tools.total_of(readings)}")
print(f"average {sweep_tools.average_of(readings)}")
print(f"over {limit}: {sweep_tools.count_over(readings, limit)}")
print(f"first best at {sweep_tools.best_index(readings)}")
print(f"last best at {sweep_tools.last_best_index(readings)}")

print("--- checks ---")
print(f"total_of([1, 2, 3]) expected 6 got {sweep_tools.total_of([1, 2, 3])}")
print(f"total_of([]) expected 0 got {sweep_tools.total_of([])}")
print(f"count_over([5, 5, 5], 5) expected 0 got {sweep_tools.count_over([5, 5, 5], 5)}")
print(f"best_index([9, 9]) expected 0 got {sweep_tools.best_index([9, 9])}")
print(f"last_best_index([9, 9]) expected 1 got {sweep_tools.last_best_index([9, 9])}")
