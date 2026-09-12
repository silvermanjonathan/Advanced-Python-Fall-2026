"""Train a word-pair model on a text file, then let it write."""

import random
from collections import defaultdict

random.seed(20261202)


def load_words(filename):
    """Return every whitespace-separated word in the file, lowercased."""
    with open(filename) as f:
        text = f.read()
    return text.lower().split()


def build_model(words):
    """Return a table mapping each word pair to the words that followed it."""
    model = defaultdict(list)
    for i in range(len(words) - 2):
        pair = (words[i], words[i + 1])
        model[pair].append(words[i + 2])
    return model


def generate(model, seed_pair, length):
    """Return a sentence of the given length, starting from seed_pair."""
    first, second = seed_pair
    out = [first, second]
    for step in range(length):
        options = model[(first, second)]
        if len(options) == 0:
            return " ".join(out)
        nxt = random.choice(options)
        out.append(nxt)
        first, second = second, nxt
    return " ".join(out)


words = load_words("corpus.txt")
model = build_model(words)

print(f"corpus words: {len(words)}")
print(f"distinct pairs: {len(model)}")
print()
print("pairs with the most different followers:")
ranked = sorted(model.items(), key=lambda kv: len(set(kv[1])), reverse=True)
for pair, followers in ranked[:5]:
    print(f"  {pair} -> {sorted(set(followers))}")
print()
print("what followed ('the', 'machine'):")
print(f"  {sorted(set(model[('the', 'machine')]))}")
print()
for i in range(4):
    print(f"{i + 1}. {generate(model, ('the', 'machine'), 22)}")
    print()
