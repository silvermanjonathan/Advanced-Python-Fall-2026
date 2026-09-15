"""Answer key for session 2, section 5: the print lines for the new functions."""

import sweep_tools_more

readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

print(f"smallest {sweep_tools_more.smallest_of(readings)}")
print(f"largest {sweep_tools_more.largest_of(readings)}")
print(f"spread {sweep_tools_more.spread_of(readings)}")
print(f"under {limit}: {sweep_tools_more.count_under(readings, limit)}")
print(f"between 30 and 60: {sweep_tools_more.count_between(readings, 30, 60)}")
print(f"total over {limit}: {sweep_tools_more.total_over(readings, limit)}")
print(f"first over {limit} at index {sweep_tools_more.first_over_index(readings, limit)}")
