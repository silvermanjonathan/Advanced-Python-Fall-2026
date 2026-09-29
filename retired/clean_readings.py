"""Read a messy file, keep what is usable, and say what was thrown away.

The file is deliberately dirty. Real files always are.
"""

MESSY = """41
58
  33
58
twelve
12

77,
58
-9
60
29
77 
"""


def write_messy(filename):
    """Create the dirty input file this lesson reads."""
    handle = open(filename, "w")
    handle.write(MESSY)
    handle.close()


def read_lines(filename):
    """Return every line in the file, or an empty list if it is missing."""
    try:
        handle = open(filename, "r")
    except FileNotFoundError:
        print(f"no file called {filename}, so there is nothing to read")
        return []
    lines = handle.readlines()
    handle.close()
    return lines


def clean(lines):
    """Return the numbers we could read, plus the lines we could not."""
    good = []
    rejected = []
    for raw in lines:
        text = raw.strip()
        text = text.replace(",", "")

        if text == "":
            rejected.append((raw, "blank"))
        else:
            try:
                value = int(text)
            except ValueError:
                rejected.append((raw, "not a number"))
            else:
                if value < 0:
                    rejected.append((raw, "negative"))
                else:
                    good.append(value)
    return good, rejected


def write_report(filename, good, rejected):
    """Write a short report next to the data."""
    handle = open(filename, "w")

    handle.write(f"kept {len(good)} readings\n")
    handle.write(f"rejected {len(rejected)} lines\n")
    total = 0

    for v in good:
        total = total + v

    handle.write(f"total {total}\n")
    handle.write(f"average {total / len(good)}\n")
    handle.close()


write_messy("readings_raw.txt")

lines = read_lines("readings_raw.txt")
print(f"lines in the file: {len(lines)}")

good, rejected = clean(lines)
print(f"kept: {good}")
print(f"kept {len(good)}, rejected {len(rejected)}")
print("rejected lines and why:")
for raw, reason in rejected:
    print(f"  {raw!r} -> {reason}")

write_report("readings_report.txt", good, rejected)
print()
print("readings_report.txt now says:")
print(open("readings_report.txt").read())

print("and when the file is not there:")
read_lines("no_such_file.txt")
