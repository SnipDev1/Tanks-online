def load_image(image_path):
    import os
    import pygame as pg
    return pg.image.load(os.path.abspath(image_path))


def nearest_value(list_of_values: list, target_value: float, get_index=False):
    closest_value = min(list_of_values, key=lambda x: abs(x - target_value))
    if get_index:
        return list_of_values.index(closest_value)
    return closest_value


def find_object_index_in_list(what_is_looking_for, list_where_to_search):
    try:
        return list_where_to_search.index(what_is_looking_for)
    except ValueError:
        print("DICK")
        print(what_is_looking_for, list_where_to_search)
        return -1  # или другое значение по умолчанию


def load_image_sequence(sequence):
    images = []
    for i in range(len(sequence)):
        path = sequence[i]
        images.append(load_image(path))
    return images



def get_emitter_offset(tank_center_x, tank_center_y, gun_length, gun_angle_degrees):
    import math
    angle_rad = math.radians(-gun_angle_degrees - 90)

    offset_x = gun_length * math.cos(angle_rad)
    offset_y = gun_length * math.sin(angle_rad)

    emitter_x = tank_center_x + offset_x
    emitter_y = tank_center_y + offset_y

    return [emitter_x, emitter_y]


def parse_folder():
    import os
    folder_path = r"sprites\smoke_pipe"  # Replace with the actual path to your folder
    items_in_folder = os.listdir(folder_path)
    file_list = []
    items_in_folder = sorted(items_in_folder, key=len)
    for i in range(len(items_in_folder)):
        items_in_folder[i] = folder_path + "\\" + items_in_folder[i]
    stringify_output = str(items_in_folder)
    stringify_output = stringify_output.replace("'", '"')
    print(stringify_output)
    return items_in_folder


parse_folder()
