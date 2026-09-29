"""Session 3 opener: three accumulators, one number and two strings."""

scores = [4, 7, 2]
total = 0
for s in scores:
    total = total + s
print(f"total {total}")

word = "cab"
out = ""
for ch in word:
    out = out + ch + ch
print(f"out {out}")

backwards = ""
for ch in word:
    backwards = ch + backwards
print(f"backwards {backwards}")
