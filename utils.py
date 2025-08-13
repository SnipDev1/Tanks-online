
def load_image(image_path):
    import os
    import pygame as pg
    return pg.image.load(os.path.abspath(image_path))
