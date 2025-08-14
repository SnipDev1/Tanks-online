import pygame as pg

import game_objects
import materials
import utils


class Game:
    def __init__(self):
        self.tank_image = None
        self.box_image = None
        self.enemy_image = None
        self.floor_image = None
        self.objects_to_update = []
        self.update_order = []
        self.active_objects = []
        self.anim_sequences = []
        self.game_map = []
        self.tanks = []
        self.tank = None
        self.res_dictionary = materials.Sprites().res_dictionary
        print(self.res_dictionary)
        self.load_map()


    def spawn_object_by_number(self, number, screen, position):
        obj = None
        match number:
            case 2:
                obj = game_objects.Box((400, 400), 0, 'Box', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2, obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                obj.explosion_anim.coordinates = obj.coordinates

                self.active_objects.append(obj.game_object_class)
                self.objects_to_update.append(obj)
            case 4:
                obj = game_objects.Floor((400, 400), 0, 'floor', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2, obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                self.objects_to_update.append(obj)
            case 6:
                obj = game_objects.LightTank([100, 100], 0, 'LT', screen, self)
                obj.coordinates = [obj.sprite_size[0] * position[0] + obj.sprite_size[0] / 2, obj.sprite_size[1] * position[1] + obj.sprite_size[1] / 2]
                self.active_objects.append(obj.game_object_class)
                self.tanks.append(obj)
                self.tank = obj
                self.objects_to_update.append(obj)







    def initialize_map(self, screen):
        for row in range(len(self.game_map)):
            for column in range(len(self.game_map[row])):
                element = self.game_map[row][column]
                self.spawn_object_by_number(element, screen, [column, row])

                # x_coord = buttons_x_shift + map_surface.x + button_x_size * column
                # y_coord = buttons_y_shift + map_surface.y + button_y_size * row
                # self.map_buttons.append(Button((x_coord, y_coord), (button_x_size, button_y_size), (255, 255, 255), "", (0, 0, 0), None, row, column, element, True, 100))

    def load_map(self):
        loaded_map = []
        with open("map.txt", 'r') as f:
            data = f.read().split(';')
            for row in data:
                row = row.split(',')
                row = list(map(int, row))
                loaded_map.append(row)
        self.game_map = loaded_map

    def parse_images(self):
        import materials
        textures_paths = materials.Sprites().texture_dictionary

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
        # test_obj = game_objects.Box((300, 300), 0, 'Box1', screen, self)
        # # explosion = game_objects.Explosion("explosion_2",(500, 500), 0, 'expl', screen, self)
        # another_test_obj = game_objects.Box((400, 400), 0, 'Box2', screen, self)
        # tank = game_objects.LightTank([100, 100], 0, 'LT', screen, self)


        self.initialize_map(screen)
        # projectile = game_objects.ProjectileEmitter(100, 100, [500, 500], 90, screen)
        # projectile.shoot()
        tank = self.tank
        while running:
            dt = clock.tick(144) / 1000
            # print(clock.get_fps())
            # Event handling loop
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
                print(anim.name)
                anim.sprite_sequencer()

            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    Game().start_game()