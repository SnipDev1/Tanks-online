import pygame as pg


class Text:
    def __init__(self, coordinates, default_text, value, size=24, color=[255, 255, 255]):
        self.text_rect = None
        self.text = None
        self.color = color
        self.size = size
        self.default_text = default_text
        self.coordinates = coordinates
        self.font = pg.font.Font(None, size)
        self.update_value(value)

    def update_value(self, value):
        self.text = self.font.render(f"{self.default_text}{value}", True, self.color)
        self.text_rect = self.text.get_rect(center=self.coordinates)


class Surface:
    def __init__(self, coordinates: tuple, size: tuple, fill_color: tuple, alpha: int):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.size_x = size[0]
        self.size_y = size[1]
        self.surface = pg.Surface((self.size_x, self.size_y))
        self.surface.fill(fill_color)
        self.surface.set_alpha(alpha)


class Button:
    @staticmethod
    def color_under_cursor(color, darkness_value):
        new_color = []
        for i in color:
            res = i - darkness_value
            if res > 0:
                new_color.append(res)
            else:
                new_color.append(0)
        return new_color

    def is_clicked(self, event, value=None):
        if self.button_rect.collidepoint(event.pos):
            # print(f"Button clicked! {self.x_index}, {self.y_index}")
            if value is not None:
                self.value = value
            self.update_button()
            return self.value
        return None

    def update_button(self):
        if self.use_value_color:
            import materials
            self.btn_color = materials.Sprites().get_material_color_by_id(self.value)
        self.button_surface.fill(self.btn_color)
        self.button_surface.blit(self.text, self.text_rect)

    def is_under_cursor(self):
        if self.button_rect.collidepoint(pg.mouse.get_pos()):
            self.button_surface.fill(self.btn_color_under_cursor)
        else:
            self.button_surface.fill(self.btn_color)
        self.button_surface.blit(self.text, self.text_rect)

    def __init__(self, coordinates: tuple, size: tuple, btn_color: tuple, text: str, text_color: tuple, image=None, x_index=-1, y_index=-1, value=-1, use_value_color=False, darkness_value=60):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.x_index = x_index
        self.y_index = y_index
        self.value = value
        self.btn_color = btn_color
        self.use_value_color = use_value_color
        if use_value_color:
            import materials
            self.btn_color = materials.Sprites().get_material_color_by_id(self.value)
        self.btn_color_under_cursor = self.color_under_cursor(btn_color, darkness_value)

        self.button_surface = pg.Surface(size)
        self.button_surface.fill(btn_color)

        font = pg.font.Font(None, 24)

        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=(self.button_surface.get_width() / 2, self.button_surface.get_height() / 2))
        self.button_rect = pg.Rect(coordinates[0], coordinates[1], size[0], size[1])

        self.button_surface.blit(self.text, self.text_rect)


class UI:
    def __init__(self, map_path):
        import materials
        self.buttons = []
        self.map_buttons = []
        self.game_map = []
        self.map_x = 0
        self.map_y = 0
        self.res_dictionary = materials.Sprites().res_dictionary
        self.bg_image = None
        self.map_path = map_path
        self.set_images()
        self.load_map()
        self.selected_material = -1

    def load_map(self):
        loaded_map = []
        with open(self.map_path, 'r') as f:
            data = f.read().split(';')
            for row in data:
                row = row.split(',')
                row = list(map(int, row))
                loaded_map.append(row)
        self.map_y = len(loaded_map)
        self.map_x = len(loaded_map[0])
        self.game_map = loaded_map

    def set_images(self):
        import materials
        import os
        bg_image_path = materials.Sprites().get_image_path('map_editor_bg')
        self.bg_image = pg.image.load(os.path.abspath(bg_image_path))

    def start_editor(self):
        pg.init()

        screen_width = 800
        screen_height = 800
        screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption("Map Editor")

        background = pg.Surface(screen.get_size()).convert()
        bg_image = self.bg_image
        bg_image = bg_image.convert()
        screen.blit(bg_image, (0, 0))

        materials_surface = Surface((30, 37), (741, 76), (255, 0, 0), 60)
        screen.blit(materials_surface.surface, (materials_surface.x, materials_surface.y))

        space_between_mat_buttons = 0
        amount_of_mat_buttons = len(self.res_dictionary)
        print(amount_of_mat_buttons)
        button_x_size = materials_surface.surface.get_width() // amount_of_mat_buttons - space_between_mat_buttons
        button_y_size = materials_surface.surface.get_height()
        buttons_x_shift = (materials_surface.surface.get_width() - button_x_size * amount_of_mat_buttons) // 2
        for i in range(amount_of_mat_buttons):
            x_coord = materials_surface.x + button_x_size * i + buttons_x_shift
            y_coord = materials_surface.y
            button = Button((x_coord, y_coord), (button_x_size, button_y_size), (255, 255, 255), self.res_dictionary[i], (0, 0, 0), None, -1, -1, i, True, 60)
            self.buttons.append(button)


        map_surface = Surface((132, 132), (537, 537), (255, 255, 0), 0)


        screen.blit(map_surface.surface, (132, 132))
        button_x_size = map_surface.surface.get_width() // self.map_x
        button_y_size = map_surface.surface.get_height() // self.map_y
        buttons_x_shift = (map_surface.surface.get_width() - button_x_size * self.map_x) // 2
        buttons_y_shift = (map_surface.surface.get_height() - button_y_size * self.map_y) // 2
        print(button_x_size, button_y_size)
        print(buttons_x_shift)

        for row in range(len(self.game_map)):
            for column in range(len(self.game_map[row])):
                element = self.game_map[row][column]
                x_coord = buttons_x_shift + map_surface.x + button_x_size * column
                y_coord = buttons_y_shift + map_surface.y + button_y_size * row
                self.map_buttons.append(Button((x_coord, y_coord), (button_x_size, button_y_size), (255, 255, 255), "", (0, 0, 0), None, row, column, element, True, 100))

        running = True
        fill_mode = False
        bucket_mode = False
        texts = []
        fill_text = Text((80, 10), "Fill (F / G): ", fill_mode, 30)
        bucket_text = Text((440, 10), "Bucket (B / N): ", bucket_mode, 30)
        text_surface = Surface((132, 669), (537, 40), (22, 22, 22), 255)

        texts.append(fill_text)
        texts.append(bucket_text)
        while running:

            # Event handling loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        fill_mode = True
                    if event.key == pg.K_g:
                        fill_mode = False
                    if event.key == pg.K_b:
                        bucket_mode = True
                    if event.key == pg.K_n:
                        bucket_mode = False
                    if event.key == pg.K_s:
                        map_to_save = ""
                        for y in range(self.map_y):
                            if y != 0:
                                map_to_save += ";"
                            for x in range(self.map_x):
                                if x != 0:
                                    map_to_save += ", "
                                map_to_save += f"{self.map_buttons[x + y * self.map_x].value}"
                            map_to_save = map_to_save.strip()
                        with open("map.txt", "w") as f:
                            f.write(map_to_save)
                        print("Saved!")

                if event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.MOUSEMOTION and fill_mode):
                    if not fill_mode:
                        for button in self.buttons:
                            res = button.is_clicked(event)
                            if res is not None:
                                self.selected_material = res
                    if bucket_mode:
                        need_value = 0
                        for button in self.map_buttons:
                            if button.is_clicked(event) is not None:
                                need_value = button.value
                                break
                        for map_button in self.map_buttons:
                            if map_button.value == need_value:
                                map_button.value = self.selected_material
                                map_button.update_button()
                    for button in self.map_buttons:
                        button.is_clicked(event, self.selected_material)

                    # Print details of the mouse click to the console  # print(  #     f"Mouse button pressed at position: {event.pos}, Button: {event.button}")  # elif event.type == pg.MOUSEBUTTONUP:  #     # Optionally, detect mouse button release  #     print(f"Mouse button released at position: {event.pos}, Button: {event.button}")
            text_surface.surface.fill((22, 22, 22))
            for i in range(len(texts)):
                element = texts[i]
                match i:
                    case 0:
                        value = fill_mode
                    case 1:
                        value = bucket_mode
                    case _:
                        value = False

                element.update_value(str(value))
                text_surface.surface.blit(element.text, element.text_rect)
                screen.blit(text_surface.surface, (text_surface.x, text_surface.y))

            for button in self.buttons:
                button.is_under_cursor()
                screen.blit(button.button_surface, (button.x, button.y))

            for button in self.map_buttons:
                button.is_under_cursor()
                screen.blit(button.button_surface, (button.x, button.y))

            # Update display (optional, if you have visual elements)
            pg.display.flip()

        pg.quit()


UI("map.txt").start_editor()
