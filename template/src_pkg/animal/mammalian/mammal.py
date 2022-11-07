class Mammal:
    """
    This class is for creating Mammal objects
    Args:
        name (str): horse name
        weight (float): horse weight in kilograms
    """

    def __init__(self, name: str, weight: float) -> None:
        self.name = name
        self.weight = weight

    def talk(self) -> None:
        """
        This method is for introducing Mammal objects
        """
        print(f"{self.name} is a {self.weight} mammal")
