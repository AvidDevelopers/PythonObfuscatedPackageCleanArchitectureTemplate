class Mammal:
    def __init__(self, name: "str", weight: float) -> None:
        self.name = name
        self.weight = weight

    def talk(self) -> None:
        print(f"Hi, my name is {self.name}")
