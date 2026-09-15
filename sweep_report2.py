"""Summarize tower readings using our own sweep_tools module."""

import sweep_tools

readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

print(f"total {sweep_tools.total_of(readings)}")
print(f"average {sweep_tools.average_of(readings)}")
print(f"over {limit}: {sweep_tools.count_over(readings, limit)}")
print(f"first best at {sweep_tools.best_index(readings)}")
print(f"last best at {sweep_tools.last_best_index(readings)}")

