"""Session 3: what a Counter can do."""

from collections import Counter

counts = Counter("banana")
print(counts)
print(counts["a"])
print(counts["z"])
print(counts.most_common(2))
print(counts.total())

counts.update("bandana")
print(counts)

first = Counter("listen")
second = Counter("silent")
print(first == second)
