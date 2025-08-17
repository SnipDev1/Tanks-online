import json


def set_map():
    width = 8
    height = 8
    tiles = []

    for y in range(height):
        for x in range(width):
            tiles.append({
                'x': x,
                'y': y,
                'material_id': 0,
                'layer': 0
            })

    map_data = {
        'width': width,
        'height': height,
        'tiles': tiles
    }

    with open("map.json", "w") as f:
        json.dump(map_data, f, indent=2)
    print("Map generated: map.json")


def convert_old_map(old_path, new_path):
    with open(old_path, 'r') as f:
        data = f.read().split(';')

    tiles = []
    for y, row in enumerate(data):
        cols = row.split(',')
        for x, val in enumerate(cols):
            if val.strip():
                tiles.append({
                    'x': x,
                    'y': y,
                    'material_id': int(val.strip()),
                    'layer': 0
                })

    width = len(cols)
    height = len(data)
    map_data = {
        'width': width,
        'height': height,
        'tiles': tiles
    }

    with open(new_path, 'w') as f:
        json.dump(map_data, f, indent=2)
    print(f"Converted {old_path} to {new_path}")

# Выберите что нужно сделать:
set_map()  # Создать новую карту
# convert_old_map("map.txt", "map.json")  # Конвертировать старую карту
