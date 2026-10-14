"""Session 3: a quick look at dictionaries, before step 3 of the console."""

code_names = {"ada": "falcon", "ben": "otter", "cy": "comet"}
print(code_names["ben"])

pictures = {
    "i": ["###", ".#.", ".#.", ".#.", "###"],
    "l": ["#..", "#..", "#..", "#..", "###"],
}
print(pictures["l"])

print(code_names.get("dee", "no code name"))
