from .mammalian import Mammal


class Horse(Mammal):
    """
    This class if for creating horse objects
    :param name: The horse's name
    """

    def __init__(self, name: str, weight: float, speed: float):
        super().__init__(name, weight)
        self.speed = speed

    def time_to_go(self, distance: float) -> float:

        return distance / self.speed

    def __repr__(self) -> str:
        return f"{__class__.__name__}(name={self.name}, weight={self.weight}, speed={self.speed})"
