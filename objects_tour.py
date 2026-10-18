"""Session 5 opener: values you have already used are objects."""

word = "dawn"
row = ["#", ".", "#"]
other = ["x"]
code_names = {"a": "otter"}

print(type(word))
print(type(row))
print(type(code_names))

row.append("#")
print(row)
print(other)
