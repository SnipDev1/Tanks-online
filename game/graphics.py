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
        test_obj = game_objects.Box((300, 300), 0, 'Box1', screen)
        another_test_obj = game_objects.Box((400, 400), 0, 'Box2', screen)
        objects_to_collide = [test_obj.obj_rect, another_test_obj.obj_rect]
        tank = game_objects.LightTank([100, 100], 0, 'LT', screen, objects_to_collide)

        while running:
            dt = clock.tick(clock.get_fps()) / 1000
            # Event handling loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
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
            tank.update_inputs(dt)
            screen.blit(background, (0, 0))
            tank.update_object()
            test_obj.update_object()
            another_test_obj.update_object()
            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    Game().start_game()
