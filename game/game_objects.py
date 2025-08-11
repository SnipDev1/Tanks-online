class GameObject:
    def __init__(self, health: float, is_able_to_collide: bool, coordinates: tuple, name: str, tag: str):
        self.name = name
        self.tag = tag
        self.health = health
        self.is_able_to_collide = is_able_to_collide
        self.coordinates = coordinates


class Player(GameObject):
    pass


class Enemy(GameObject):
    pass


class Box(GameObject):
    pass


