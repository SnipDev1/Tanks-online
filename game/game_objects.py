import json
import math
import time

import pygame as pg

import materials
import utils


class Decals:
    def __init__(self, decals_coef=0.2, sprites=materials.Sprites(), decals_name="breaking_stages", object=None, rotation=0):
        self.decals_coef = decals_coef
        self.sprites = sprites
        self.stages = []
        self.breaking_decals = []
        self.object = object
        self.rotation = rotation
        self.default_object = object.copy()

    def load_decals(self, health):
        paths = self.sprites.get_image_path('breaking_stages')
        self.stages.append(health)
        self.breaking_decals = utils.load_image_sequence(paths)
        step = (health - health * self.decals_coef) // len(self.breaking_decals)
        for i in range(len(self.breaking_decals)):
            self.stages.append(step * (i + 1))
        self.stages.reverse()  # print(self.stages)

    def delete_decals(self):
        obj_sprite = self.default_object
        obj_sprite = pg.transform.scale(obj_sprite, self.object.get_size())
        obj_sprite = pg.transform.rotate(obj_sprite, self.rotation)
        obj_pos = [self.object.get_rect().x, self.object.get_rect().y]
        self.object.blit(obj_sprite, obj_pos)

    def check_decal(self, health):
        self.delete_decals()
        try:
            index = utils.nearest_value(self.stages, health, True)
        except ValueError:
            return
        try:
            decal = self.breaking_decals[index]
        except IndexError:
            return
        decal = pg.transform.scale(decal, self.object.get_size())
        decal = pg.transform.rotate(decal, self.rotation)
        decal_pos = [self.object.get_rect().x, self.object.get_rect().y]
        self.object.blit(decal, decal_pos)


class GameObject:
    @staticmethod
    def get_texture_path(name):
        texture_path = materials.Sprites().get_image_path(name)
        return texture_path

    @staticmethod
    def read_json(json_name, object_name):
        with open(json_name, "r") as f:
            data = f.read()
        json_string = json.loads(data)
        return json_string[object_name]

    def __init__(self, health=100.0, is_able_to_collide=True, coordinates=[0, 0], name='blank', tag='blank', sprite_size=[100, 100], screen=None, texture_path=None, rotation=0,
                 collision_size=[100, 100], has_texture=True, game_class=None, destructible=False, has_animation=False, frame_duration=0, explosion_anim=None, parent_object=None, is_anim_cycled=False,
                 emitter_offset=0, render_layer=0):
        self.name = name
        self.game_object_class = self
        self.screen = screen
        self.rotation = rotation
        self.sprite_size = sprite_size
        self.collision_size = [self.sprite_size[0] * 0.9, self.sprite_size[1] * 0.9]
        self.tag = tag
        self.health = health
        self.start_health = health
        self.parent_object = parent_object
        self.is_able_to_collide = is_able_to_collide
        self.destructible = destructible
        self.coordinates = coordinates
        self.texture_path = texture_path
        self.sprites = materials.Sprites()
        self.emitter_offset = emitter_offset
        self.game_class = game_class
        self.is_cycled = is_anim_cycled

        self.obj_sprite = utils.load_image(self.sprites.get_image_path('box'))
        self.render_layer = render_layer

        if has_texture and not has_animation:
            self.obj_sprite = utils.load_image(self.sprites.get_image_path(self.name))

        self.isAlive = True


        self.obj_rect = self.obj_sprite.get_rect()
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]
        self.decals = Decals(sprites=self.sprites, object=self.obj_sprite, rotation=self.rotation)
        if is_able_to_collide and destructible:
            self.decals.load_decals(self.start_health)

        self.explosion_anim = explosion_anim
        if has_animation:
            self.animation = Animation(anim_name=self.name, sprites=self.sprites, game_object=self, frame_duration=frame_duration, is_anim_cycled=is_anim_cycled, render_layer=render_layer)

        if not has_animation:
            self.my_render_index = self.game_class.add_object_to_render(self, self.render_layer)

    def decrease_health(self, amount_to_decrease):
        # Убираем принты для оптимизации
        self.health -= amount_to_decrease
        self.decals.check_decal(self.health)
        if self.health <= 0:
            self.isAlive = False
            if self.explosion_anim is not None:
                self.game_class.anim_sequences.append(self.explosion_anim.animation)
            self.destroy()

    def destroy(self):
        object_index = utils.find_object_index_in_list(self, self.game_class.active_objects)
        if len(self.game_class.active_objects) != 0 and object_index != -1:
            self.game_class.active_objects.pop(object_index)
        # print(f"{self.tag} is destroyed")
        self.game_class.del_object_from_render(self.my_render_index)

    def update_object(self):
        if not self.isAlive:
            return
        if self.parent_object is not None:
            # print(self.tag)
            self.coordinates[0] = self.parent_object.coordinates[0]
            self.coordinates[1] = self.parent_object.coordinates[1]
            self.rotation = self.parent_object.rotation
            self.coordinates = utils.get_emitter_offset(self.coordinates[0], self.coordinates[1], self.emitter_offset, self.rotation)
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]
        self.obj_rect.size = self.collision_size

    def render_object(self):
        obj_sprite = pg.transform.scale(self.obj_sprite, self.sprite_size)
        copy_obj = pg.transform.rotate(obj_sprite, self.rotation)
        self.screen.blit(copy_obj, (self.coordinates[0] - int(copy_obj.get_width() / 2), self.coordinates[1] - int(copy_obj.get_height() / 2)))


class Animation:
    def __init__(self, anim_name="explosion", sprites=materials.Sprites(), coordinates=[100, 100], screen=None, rotation=0, size=[100, 100], frame_duration=0.05, game_object=None,
                 is_anim_cycled=False, is_anim_active=True, render_layer=6):
        self.name = anim_name
        self.sprites = sprites
        self.coordinates = coordinates
        self.screen = screen
        self.rotation = rotation
        self.size = size
        self.frame_duration = frame_duration
        self.game_object = game_object
        self.render_layer = render_layer
        self.sprites_set = utils.load_image_sequence(self.sprites.get_anim_sequence(anim_name))
        self.game_object.obj_sprite = self.sprites_set[0]
        self.game_class = self.game_object.game_class
        self.original_sprite = self.game_object.obj_sprite.copy()
        self.last_frame_time = time.time()
        self.current_frame = 0
        self.is_anim_cycled = is_anim_cycled
        self.is_anim_ended = False
        self.is_anim_active = is_anim_active  # if self.name == "light_tank":  #     print(self.sprites_set)
        # if is_anim_active:
        self.my_index = None


    def sprite_sequencer(self):
        if self.is_anim_ended:
            return
        if not self.is_anim_active:
            return
        if self.my_index is None:
            # print(f"{self.game_object.tag} active")
            self.my_index = self.game_class.add_object_to_render(self.game_object, self.render_layer)
        # Убираем принты для оптимизации
        if time.time() - self.last_frame_time >= self.frame_duration:
            # if self.name == "light_tank":
            #     print(self.current_frame)

            # if self.game_object.parent_object is not None:
            #     self.game_object.obj_sprite.x = self.game_object.parent_object.coordinates[0]
            #     self.game_object.obj_sprite.y = self.game_object.parent_object.coordinates[1]
            self.game_object.obj_sprite = self.sprites_set[self.current_frame]
            self.last_frame_time = time.time()
            self.current_frame += 1
            if self.is_anim_cycled:
                if self.current_frame == len(self.sprites_set):
                    self.current_frame = 0

            elif not self.is_anim_cycled and self.current_frame >= len(self.sprites_set):
                self.game_object.obj_sprite = self.original_sprite
                self.is_anim_ended = True
                self.delete_anim_from_sequencer()
                # self.game_object.destroy()

        self.game_object.update_object()

    def delete_anim_from_sequencer(self):
        object_index = utils.find_object_index_in_list(self, self.game_class.anim_sequences)
        self.game_class.anim_sequences.pop(object_index)
        self.game_class.del_object_from_render(self.my_index)




class ProjectileEmitter(GameObject):
    def __init__(self, projectile_damage, projectile_speed, emitter_coordinates, emitter_rotation, screen, game_class, rectangles_to_exclude):
        self.projectile_damage = projectile_damage
        self.projectile_speed = projectile_speed
        self.rectangles_to_exclude = rectangles_to_exclude
        self.bullets = []
        self.active_objects = game_class.active_objects
        super().__init__(screen=screen, has_texture=False, coordinates=emitter_coordinates, rotation=emitter_rotation, health=99999999, is_able_to_collide=False, collision_size=[0, 0],
                         sprite_size=[0, 0], game_class=game_class)
        self.rectangles_to_exclude.append(self.obj_rect)

    def shoot(self):
        # print("bulletasasdasd " + str(self.game_class))
        new_bullet = Projectile(self.projectile_damage, self.projectile_speed, self.coordinates, self.rotation, self.screen, self.game_class, self.rectangles_to_exclude)
        explosion = AnimEmitter(name="explosion_2", coordinates=self.coordinates, rotation=self.rotation, tag="shot_expl", screen=self.screen, game_class=self.game_class, sprite_size=[40, 40],
                                parent_object=self)
        explosion.coordinates = self.coordinates
        explosion.rotation = self.rotation
        self.game_class.anim_sequences.append(explosion.animation)
        self.bullets.append(new_bullet)

    def move_projectiles(self, dt):
        # Используем копию списка для безопасного удаления
        for bullet in self.bullets[:]:
            if bullet.met_obstacle:
                self.bullets.remove(bullet)
                continue
            bullet.move_forward(dt)
        self.update_projectiles()

    def update_projectiles(self):
        for bullet in self.bullets:
            self.game_object_class.update_object()


class Active(GameObject):
    def __init__(self, health, is_able_to_collide, coordinates, name, tag, sprite_size, screen, texture_path, rotation, game_class, render_layer):
        # print(game_class)
        super().__init__(health=health, is_able_to_collide=is_able_to_collide, coordinates=coordinates, name=name, tag=tag, sprite_size=sprite_size, screen=screen, texture_path=texture_path,
                         rotation=rotation, game_class=game_class, render_layer=render_layer)
        # self.game_class = game_class
        self.active_objects = game_class.active_objects
        self.collision_list = []

    def update_collisions(self, rect_to_exclude=None):
        self.collision_list = []
        for active_object in self.active_objects:
            if active_object != self:
                self.collision_list.append(active_object.obj_rect)
        if rect_to_exclude is not None:
            for rect in rect_to_exclude:
                if rect in self.collision_list:
                    self.collision_list.remove(rect)


class Projectile(Active):
    def __init__(self, projectile_damage, projectile_speed, emitter_coordinates, emitter_rotation, screen, game_class, rect_to_exclude):
        self.name = 'bullet'
        self.tag = self.name
        self.projectile_damage = projectile_damage
        self.projectile_speed = projectile_speed
        self.game_class = game_class
        self.active_objects = game_class.active_objects
        self.collision_list = []
        self.update_collisions(rect_to_exclude)
        self.is_able_to_collide = True
        self.met_obstacle = False
        self.screen = screen
        self.screen_rect = screen.get_rect() if screen else None
        self.start_time = time.time()
        self.rect_to_exclude = rect_to_exclude
        self.lifetime = 3.0  # 3 секунды жизни пули
        self.explosion = AnimEmitter(name="explosion_2", coordinates=emitter_coordinates, rotation=0, tag="expl", screen=screen, game_class=self.game_class)
        material = self.read_json("materials.json", self.name)

        health = material['health']
        sprite_size = material['size']
        collision_size = material['collision_size']
        render_layer = 3
        # print(self.collision_list)
        # texture_path = self.get_texture_path(self.name)
        # super().__init__(screen=screen, name=self.name, health=health, coordinates=emitter_coordinates, rotation=emitter_rotation, is_able_to_collide=True, sprite_size=sprite_size, game_class=game_class)
        super().__init__(health, self.is_able_to_collide, emitter_coordinates, self.name, self.tag, sprite_size, screen, "", emitter_rotation, game_class, render_layer)

    def move_forward(self, dt):
        if self.met_obstacle:
            return

        if time.time() - self.start_time > self.lifetime:
            self.met_obstacle = True
            return

        if self.screen_rect and not self.screen_rect.collidepoint(self.coordinates):
            self.met_obstacle = True
            self.on_collision()
            return
        self.update_collisions(self.rect_to_exclude)
        rad_rotation = math.radians(self.rotation)
        sin = math.sin(rad_rotation)
        cos = math.cos(rad_rotation)
        coordinates_before = self.coordinates.copy()
        self.coordinates = [self.coordinates[0] - self.projectile_speed * sin * dt, self.coordinates[1] - self.projectile_speed * cos * dt]
        self.game_object_class.update_object()

        collided_with = self.obj_rect.collidelistall(self.collision_list)
        if len(self.obj_rect.collidelistall(self.collision_list)) != 0:
            self.coordinates = coordinates_before
            self.met_obstacle = True
            self.on_collision(collided_with)
            self.game_object_class.update_object()

    def on_collision(self, collided_with=None):
        if collided_with is not None:
            self.explosion.coordinates = self.coordinates
            self.game_class.anim_sequences.append(self.explosion.animation)
            for i in collided_with:
                self.active_objects[i].decrease_health(self.projectile_damage)
        self.destroy()


class Tank(Active):
    def __init__(self, health: float, is_able_to_collide: bool, coordinates: list, name: str, tag: str, shot_damage: float, shot_speed: float, reload_time: float, ammo_capacity: int, speed: float,
                 screen, sprite_size, texture_path, rotation, rotation_speed, game_class, frame_duration, render_layer):
        # print(game_class)
        super().__init__(health, is_able_to_collide, coordinates, name, tag, sprite_size, screen, texture_path, rotation, game_class, render_layer)
        self.shot_damage = shot_damage
        self.shot_speed = shot_speed
        self.reload_time = reload_time
        self.rotation_speed = rotation_speed
        self.ammo_capacity = ammo_capacity
        self.speed = speed
        self.rotating = False
        self.rotating_clockwise = False
        self.moving = False
        self.is_forward = True
        self.tank_animation = Animation(anim_name="light_tank", screen=self.screen, game_object=self, is_anim_cycled=True, frame_duration=frame_duration, is_anim_active=False, render_layer=render_layer)
        self.projectile_emitter = ProjectileEmitter(self.shot_damage, self.shot_speed, self.coordinates, self.rotation, self.screen, game_class, [self.obj_rect])

        self.smoke_emitter = AnimEmitter(name="smoke", coordinates=self.coordinates, rotation=self.rotation, tag="shot_expl", screen=self.screen, game_class=self.game_class, sprite_size=[40, 40],
                                         is_anim_cycled=True, parent_object=self, emitter_offset=-40, render_layer=7)

        self.game_class.anim_sequences.append(self.smoke_emitter.animation)
        self.game_class.anim_sequences.append(self.tank_animation)
        self.projectile_emitter.coordinates = utils.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

    def update_tank(self, dt):
        # Обновляем коллизии один раз за кадр
        self.update_collisions()

        if self.rotating:
            self.turn(self.rotating_clockwise, dt)

        if self.moving:
            self.move_forward(dt)
        self.game_object_class.update_object()

        self.tank_animation.is_anim_active = self.rotating or self.moving
        self.projectile_emitter.move_projectiles(dt)
        # self.smoke_emitter.rotation = self.rotation
        # self.smoke_emitter.coordinates = utils.get_emitter_offset(self.coordinates[0], self.coordinates[1], -40, self.rotation)

    def turn(self, clockwise, dt):
        if clockwise:
            self.rotation -= self.rotation_speed * dt
        else:
            self.rotation += self.rotation_speed * dt
        self.projectile_emitter.rotation = self.rotation
        self.projectile_emitter.coordinates = utils.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

    def move_forward(self, dt):
        rad_rotation = math.radians(self.rotation)
        sin = math.sin(rad_rotation)
        cos = math.cos(rad_rotation)
        dir_multi = 1
        if not self.is_forward:
            dir_multi = -1

        # Рассчитываем новые координаты
        new_x = self.coordinates[0] - self.speed * sin * dt * dir_multi
        new_y = self.coordinates[1] - self.speed * cos * dt * dir_multi

        # Получаем размеры экрана
        screen_width, screen_height = self.screen.get_size()

        # Получаем размеры танка (учитываем, что после поворота размеры могут измениться)
        tank_width = self.obj_rect.width
        tank_height = self.obj_rect.height

        # Проверяем границы экрана с учетом размеров танка
        if (new_x - tank_width / 2 < 0 or new_x + tank_width / 2 > screen_width or new_y - tank_height / 2 < 0 or new_y + tank_height / 2 > screen_height):
            return  # Не двигаемся, если выходим за границы

        coordinates_before = self.coordinates.copy()
        self.coordinates = [new_x, new_y]
        self.game_object_class.update_object()

        if len(self.obj_rect.collidelistall(self.collision_list)) != 0:
            print('ALARM')
            self.coordinates = coordinates_before

        self.game_object_class.update_object()

        self.projectile_emitter.coordinates = utils.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

    def change_moving_state(self, state, is_forward):
        self.moving = state
        self.is_forward = is_forward

    def change_rotation_state(self, state, clockwise):
        if not state and clockwise != self.rotating_clockwise:
            return
        self.rotating = state
        self.rotating_clockwise = clockwise


class LightTank(Tank):
    def __init__(self, coordinates, rotation, tag, screen, game_class):
        name = "light_tank"
        tank_data = self.read_json('tanks.json', name)
        health = tank_data['health']
        is_able_to_collide = tank_data['is_able_to_collide']
        shot_damage = tank_data['shot_damage']
        shot_speed = tank_data['shot_speed']
        reload_time = tank_data['reload_time']
        ammo_capacity = tank_data['ammo_capacity']
        speed = tank_data['speed']
        size = tank_data['size']
        rotation_speed = tank_data['rotation_speed']
        frame_duration = tank_data['frame_duration']
        render_layer = 5
        texture_path = self.get_texture_path(name)
        super().__init__(health, is_able_to_collide, coordinates, name, tag, shot_damage, shot_speed, reload_time, ammo_capacity, speed, screen, size, texture_path, rotation, rotation_speed,
                         game_class, frame_duration, render_layer)


class Floor(GameObject):
    def __init__(self, coordinates, rotation, tag, screen, game_class):
        import materials
        name = "floor"
        material = materials.Sprites().get_material_data(name)
        sprite_size = material['size']
        destructible = material['destructible']
        render_layer = 0
        super().__init__(name=name, coordinates=coordinates, rotation=rotation, tag=tag, screen=screen, sprite_size=sprite_size, game_class=game_class, destructible=destructible,
                         render_layer=render_layer)


class Box(GameObject):
    def __init__(self, coordinates, rotation, tag, screen, game_class):
        import materials
        name = "box"
        material = materials.Sprites().get_material_data(name)
        collision_size = material['collision_size']
        sprite_size = material['size']
        destructible = material['destructible']
        render_layer = 1
        explosion = AnimEmitter(name="explosion", coordinates=coordinates, rotation=0, tag="expl", screen=screen, game_class=game_class)
        super().__init__(name=name, coordinates=coordinates, rotation=rotation, tag=tag, screen=screen, sprite_size=sprite_size, collision_size=collision_size, game_class=game_class,
                         destructible=destructible, explosion_anim=explosion, render_layer=render_layer)


class AnimEmitter(GameObject):
    def __init__(self, name, coordinates, rotation, tag, screen, game_class, sprite_size=None, parent_object=None, is_anim_cycled=False, emitter_offset=0, render_layer=7):
        import materials
        name = name
        material = materials.Sprites().get_material_data(name)
        collision_size = material['collision_size']
        if sprite_size is None:
            sprite_size = material['size']
        destructible = material['destructible']
        has_animation = material['has_anim']
        frame_duration = material['frame_duration']
        render_layer = render_layer
        super().__init__(name=name, coordinates=coordinates, rotation=rotation, tag=tag, screen=screen, sprite_size=sprite_size, collision_size=collision_size, game_class=game_class,
                         destructible=destructible, has_animation=True, frame_duration=frame_duration, parent_object=parent_object, is_anim_cycled=is_anim_cycled, emitter_offset=emitter_offset,
                         render_layer=render_layer)
