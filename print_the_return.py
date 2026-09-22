"""Session 2: a returned value can go straight into print."""


def total_of(values):
    running = 0
    for v in values:
        running = running + v
    return running


print(total_of([1, 2, 3]) * 2)
