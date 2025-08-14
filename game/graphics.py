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
        self.active_objects = []
        self.objects_to_update = []
        self.anim_sequences = []

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
        test_obj = game_objects.Box((300, 300), 0, 'Box1', screen, self)
        # explosion = game_objects.Explosion("explosion_2",(500, 500), 0, 'expl', screen, self)
        another_test_obj = game_objects.Box((400, 400), 0, 'Box2', screen, self)
        self.active_objects = [test_obj.game_object_class, another_test_obj.game_object_class]
        tank = game_objects.LightTank([100, 100], 0, 'LT', screen, self)
        self.objects_to_update = [tank, test_obj, another_test_obj]
        # projectile = game_objects.ProjectileEmitter(100, 100, [500, 500], 90, screen)
        # projectile.shoot()
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

            # Обновляем только активные объекты
            tank.update_tank(dt)

            for obj in self.objects_to_update:
                if obj.isAlive:  # Обновляем только живые объекты
                    obj.update_object()

            # Обновляем анимации
            for anim in self.anim_sequences[:]:
                # print(self.anim_sequences)
                anim.sprite_sequencer()

            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    Game().start_game()
