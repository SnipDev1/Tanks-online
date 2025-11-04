import pygame as pg
import json

import game_objects
import materials
import utils


class Game:
    def __init__(self):
        self.objects_to_update = []
        self.update_order = []
        self.active_objects = []
        self.anim_sequences = []
        self.objects_to_render = []
        self.game_map = []
        self.tanks = []
        self.tank = None
        self.res_dictionary = materials.Sprites().res_dictionary
        self.load_map()
        self.render_index_counter = 0

    def del_object_from_render(self, render_index):
        self.objects_to_render = [t for t in self.objects_to_render if t[0] != render_index]

    def add_object_to_render(self, game_object, render_layer):
        self.render_index_counter += 1
        self.objects_to_render.append((self.render_index_counter, render_layer, game_object))
        return self.render_index_counter

    def spawn_object_by_number(self, material_id, screen, position, layer=0):
        obj = None
        match material_id:
            case 2:
                obj = game_objects.Box((400, 400), 0, 'Box', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2,
                                   obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                obj.explosion_anim.coordinates = obj.coordinates
                self.active_objects.append(obj.game_object_class)
                self.objects_to_update.append(obj)
            case 4:
                obj = game_objects.Floor((400, 400), 0, 'floor', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2,
                                   obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                self.objects_to_update.append(obj)
            case 6:
                obj = game_objects.LightTank([100, 100], 0, 'LT', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2,
                                   obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                self.active_objects.append(obj.game_object_class)
                self.tanks.append(obj)
                self.tank = obj
                self.objects_to_update.append(obj)
            case 7:
                obj = game_objects.Bush([100, 100], 0, 'LT', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2,
                                   obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                # self.active_objects.append(obj.game_object_class)
                self.objects_to_update.append(obj)

    def initialize_map(self, screen):
        for row in range(len(self.game_map)):
            for column in range(len(self.game_map[row])):
                cell = self.game_map[row][column]
                for layer_data in cell['layers']:
                    self.spawn_object_by_number(
                        layer_data['material_id'],
                        screen,
                        [column, row],
                        layer_data.get('layer', 0)
                    )

    def load_map(self):
        try:
            with open("map.json", 'r') as f:
                data = json.load(f)

            self.game_map = []
            width = data['width']
            height = data['height']

            for y in range(height):
                row = []
                for x in range(width):
                    tiles = [t for t in data['tiles'] if t['x'] == x and t['y'] == y]
                    row.append({'layers': tiles})
                self.game_map.append(row)

        except (FileNotFoundError, json.JSONDecodeError):
            self.game_map = []
            for y in range(8):
                row = []
                for x in range(8):
                    row.append({'layers': [{'material_id': 4, 'layer': 0}]})
                self.game_map.append(row)
            print("Created default map")

    def parse_images(self):
        import materials
        textures_paths = materials.Sprites().texture_dictionary

    def update_screen(self):
        sorted_objs = sorted(self.objects_to_render, key=lambda x: x[1])
        for i in sorted_objs:
            game_object = i[2]
            game_object.render_object()

    def start_game(self):
        pg.init()
        pg.display.set_caption("Tanks Online")
        screen_width = 800
        screen_height = 800
        clock = pg.time.Clock()

        sprites = materials.Sprites()
        screen = pg.display.set_mode((screen_width, screen_height))
        background = pg.Surface(screen.get_size()).convert()
        bg_sprite = utils.load_image(sprites.get_image_path("test_bg"))
        bg_sprite = pg.transform.scale(bg_sprite, (screen.get_width(), screen.get_height()))
        background.blit(bg_sprite, (0, 0))

        running = True
        self.initialize_map(screen)
        tank = self.tank
        while running:
            dt = clock.tick(300) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        tank.projectile_emitter.shoot()
                    if event.key == pg.K_w:
                        tank.change_moving_state(True, True)
                    elif event.key == pg.K_s:
                        tank.change_moving_state(True, False)
                    if event.key == pg.K_d:
                        tank.change_rotation_state(True, True)
                    elif event.key == pg.K_a:
                        tank.change_rotation_state(True, False)
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        tank.change_moving_state(False, True)
                    elif event.key == pg.K_s:
                        tank.change_moving_state(False, False)
                    if event.key == pg.K_d:
                        tank.change_rotation_state(False, True)
                    elif event.key == pg.K_a:
                        tank.change_rotation_state(False, False)

            screen.blit(background, (0, 0))

            for obj in self.objects_to_update:
                if obj.isAlive:
                    obj.update_object()

            for tank in self.tanks:
                tank.update_tank(dt)

            for anim in self.anim_sequences[:]:
                anim.sprite_sequencer()

            self.update_screen()
            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    Game().start_game()