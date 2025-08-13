def load_image(image_path):
    import os
    import pygame as pg
    return pg.image.load(os.path.abspath(image_path))


def nearest_value(list_of_values: list, target_value: float, get_index=False):
    closest_value = min(list_of_values, key=lambda x: abs(x - target_value))
    if get_index:
        return list_of_values.index(closest_value)
    return closest_value
