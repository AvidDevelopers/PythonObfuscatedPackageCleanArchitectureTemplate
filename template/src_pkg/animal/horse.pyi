from .mammalian import Mammal

class Horse(Mammal):
    """
    This class if for creating horse objects
    Args:
        name (str): horse name
        weight (float): horse weight in kilograms
        speed (float): horse speed in kilometers
    """

    def __init__(self, name: str, weight: float, speed: float):
        super().__init__(name, weight)
        self.speed = speed
    def time_to_go(self, distance: float) -> float:
        """calculate the time to go with speed

        Args:
            distance (float): distance to travel in kilometers

        Returns:
            float: distance per speed in kilometers
        """
        ...
