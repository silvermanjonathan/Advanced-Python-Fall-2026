"""Session 5: a class for a virtual pet, and two pets made from it."""


class Pet:
    """A virtual pet that keeps its own name, hunger, and happiness."""

    def __init__(self, name):
        self.name = name
        self.hunger = 5
        self.happiness = 5

    def feed(self):
        """Make this pet 1 less hungry."""
        self.hunger = self.hunger - 1

    def play(self):
        """Make this pet 1 happier."""
        self.happiness = self.happiness + 1

    def report(self):
        """Return one line about this pet."""
        return f"{self.name}: hunger {self.hunger}, happiness {self.happiness}"


# make two pets from the one class
rocky = Pet("Rocky")
luna = Pet("Luna")

rocky.feed()
rocky.feed()
luna.play()

print(rocky.report())
print(luna.report())
print(type(rocky))
