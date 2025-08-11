def set_map():
    string_to_write = ""
    x_size = 32
    y_size = 64
    for y in range(y_size):
        if y != 0:
            string_to_write += ";"
        for x in range(x_size):
            if x != 0:
                string_to_write += ", "
            string_to_write += "0"
        string_to_write = string_to_write.strip()



    print(string_to_write)

    with open("map.txt", "w") as f:
        f.write(string_to_write)


def load_map():
    loaded_map = []
    with open("map.txt", 'r') as f:
        data = f.read().split(';')
        for row in data:
            row = row.split(',')

            row = list(map(int, row))
            loaded_map.append(row)
    y = len(loaded_map)
    x = len(loaded_map[0])
set_map()


