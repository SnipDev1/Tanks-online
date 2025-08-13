import json
import math

import pygame as pg

import materials
import utils


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
                 collision_size=[100, 100], has_texture=True, game_class=None, destructible=False):

        self.name = name
        self.game_object_class = self
        self.screen = screen
        self.rotation = rotation
        self.sprite_size = sprite_size
        self.collision_size = [self.sprite_size[0] * 0.9, self.sprite_size[1] * 0.9]
        self.tag = tag
        self.health = health
        self.start_health = health
        self.is_able_to_collide = is_able_to_collide
        self.destructible = destructible
        self.coordinates = coordinates
        self.texture_path = texture_path
        self.sprites = materials.Sprites()
        self.game_class = game_class
        # print(self.tag, self.object_index, self.game_class)
        self.obj_sprite = utils.load_image(self.sprites.get_image_path('box'))
        self.default_obj_sprite = self.obj_sprite.copy()
        self.breaking_decals = []
        self.stages = []
        if is_able_to_collide and destructible:
            self.load_decals()
            print(self.stages)
        self.isAlive = True

        if has_texture:
            self.obj_sprite = utils.load_image(self.sprites.get_image_path(self.name))
        self.obj_rect = self.obj_sprite.get_rect()
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]

    def load_decals(self):
        paths = self.sprites.get_image_path('breaking_stages')
        self.stages.append(self.start_health)
        for i in range(len(paths)):
            path = paths[i]
            self.breaking_decals.append(utils.load_image(path))
        step = (self.start_health - self.start_health * 0.2) // len(self.breaking_decals)
        for i in range(len(self.breaking_decals)):
            self.stages.append(step*(i+1))
        self.stages.reverse()


    def delete_decals(self):
        obj_sprite = self.default_obj_sprite
        obj_sprite = pg.transform.scale(obj_sprite, self.obj_sprite.get_size())
        obj_sprite = pg.transform.rotate(obj_sprite, self.rotation)
        obj_pos = [self.obj_sprite.get_rect().x, self.obj_sprite.get_rect().y]
        self.obj_sprite.blit(obj_sprite, obj_pos)

    def check_decal(self):
        self.delete_decals()
        index = utils.nearest_value(self.stages, self.health, True)
        try:
            decal = self.breaking_decals[index]
        except IndexError:
            return
        decal = pg.transform.scale(decal, self.obj_sprite.get_size())
        decal = pg.transform.rotate(decal, self.rotation)
        decal_pos = [self.obj_sprite.get_rect().x, self.obj_sprite.get_rect().y]
        self.obj_sprite.blit(decal, decal_pos)




    def find_object_index(self):
        try:
            return self.game_class.active_objects.index(self)
        except ValueError:
            print("DICK")
            print(self, self.game_class.active_objects)
            return -1  # или другое значение по умолчанию

    def decrease_health(self, amount_to_decrease):
        # print(self.game_class)

        self.health -= amount_to_decrease
        self.check_decal()
        print(f"OBJECT {self.tag}, HEALTH: {self.health}")
        if self.health <= 0:
            self.isAlive = False
            self.destroy()

    def destroy(self):
        object_index = self.find_object_index()
        self.game_class.active_objects.pop(object_index)

    def update_object(self):
        if not self.isAlive:
            return
        obj_sprite = pg.transform.scale(self.obj_sprite, self.sprite_size)
        copy_obj = pg.transform.rotate(obj_sprite, self.rotation)
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]
        self.obj_rect.size = self.collision_size

        # if self.tag == "Box1":
        # print(self.obj_rect, self.coordinates)
        self.screen.blit(copy_obj, (self.coordinates[0] - int(copy_obj.get_width() / 2), self.coordinates[1] - int(copy_obj.get_height() / 2)))


class ProjectileEmitter(GameObject):
    def __init__(self, projectile_damage, projectile_speed, emitter_coordinates, emitter_rotation, screen, game_class):
        self.projectile_damage = projectile_damage
        self.projectile_speed = projectile_speed
        self.bullets = []
        self.active_objects = game_class.active_objects
        super().__init__(screen=screen, has_texture=False, coordinates=emitter_coordinates, rotation=emitter_rotation, health=99999999, is_able_to_collide=False, collision_size=[0, 0],
                         sprite_size=[0, 0], game_class=game_class)

    def get_emitter_offset(self, tank_center_x, tank_center_y, gun_length, gun_angle_degrees):

        angle_rad = math.radians(-gun_angle_degrees - 90)

        offset_x = gun_length * math.cos(angle_rad)
        offset_y = gun_length * math.sin(angle_rad)

        emitter_x = tank_center_x + offset_x
        emitter_y = tank_center_y + offset_y

        return [emitter_x, emitter_y]

    def shoot(self):
        # print("bulletasasdasd " + str(self.game_class))
        new_bullet = Projectile(self.projectile_damage, self.projectile_speed, self.coordinates, self.rotation, self.screen, self.game_class)
        self.bullets.append(new_bullet)

    def move_projectiles(self, dt):
        for bullet in self.bullets:
            # print(bullet.coordinates)
            bullet.move_forward(dt)
        self.update_projectiles()

    def update_projectiles(self):
        for bullet in self.bullets:
            self.update_object()


class Active(GameObject):
    def __init__(self, health, is_able_to_collide, coordinates, name, tag, sprite_size, screen, texture_path, rotation, game_class):
        # print(game_class)
        super().__init__(health=health, is_able_to_collide=is_able_to_collide, coordinates=coordinates, name=name, tag=tag, sprite_size=sprite_size, screen=screen, texture_path=texture_path,
                         rotation=rotation, game_class=game_class)
        # self.game_class = game_class
        self.active_objects = game_class.active_objects
        self.collision_list = []

    def update_collisions(self):
        self.collision_list = []
        for active_object in self.active_objects:
            if active_object != self:
                self.collision_list.append(active_object.obj_rect)


class Projectile(Active):
    def __init__(self, projectile_damage, projectile_speed, emitter_coordinates, emitter_rotation, screen, game_class):
        self.name = 'bullet'
        self.tag = self.name
        self.projectile_damage = projectile_damage
        self.projectile_speed = projectile_speed
        self.game_class = game_class
        self.active_objects = game_class.active_objects
        self.collision_list = []
        self.update_collisions()
        self.is_able_to_collide = True
        self.met_obstacle = False
        material = self.read_json("materials.json", self.name)

        health = material['health']
        sprite_size = material['size']
        collision_size = material['collision_size']
        # print(self.collision_list)
        # texture_path = self.get_teaxture_path(self.name)
        # super().__init__(screen=screen, name=self.name, health=health, coordinates=emitter_coordinates, rotation=emitter_rotation, is_able_to_collide=True, sprite_size=sprite_size, game_class=game_class)
        super().__init__(health, self.is_able_to_collide, emitter_coordinates, self.name, self.tag, sprite_size, screen, "", emitter_rotation, game_class)



    def move_forward(self, dt):
        if self.met_obstacle:
            return
        self.update_collisions()
        rad_rotation = math.radians(self.rotation)
        sin = math.sin(rad_rotation)
        cos = math.cos(rad_rotation)
        coordinates_before = self.coordinates.copy()
        self.coordinates = [self.coordinates[0] - self.projectile_speed * sin * dt, self.coordinates[1] - self.projectile_speed * cos * dt]
        self.update_object()
        collided_with = self.obj_rect.collidelistall(self.collision_list)
        if len(self.obj_rect.collidelistall(self.collision_list)) != 0:
            print(self.obj_rect.collidelistall(self.collision_list))
            self.coordinates = coordinates_before
            self.met_obstacle = True
            self.on_collision(collided_with)
            self.update_object()

    def on_collision(self, collided_with):
        for i in collided_with:
            self.active_objects[i].decrease_health(self.projectile_damage)


class Tank(Active):
    def __init__(self, health: float, is_able_to_collide: bool, coordinates: list, name: str, tag: str, shot_damage: float, shot_speed: float, reload_time: float, ammo_capacity: int, speed: float,
                 screen, sprite_size, texture_path, rotation, rotation_speed, game_class):
        # print(game_class)
        super().__init__(health, is_able_to_collide, coordinates, name, tag, sprite_size, screen, texture_path, rotation, game_class)
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

        self.projectile_emitter = ProjectileEmitter(self.shot_damage, self.shot_speed, self.coordinates, self.rotation, self.screen, game_class)
        self.projectile_emitter.coordinates = self.projectile_emitter.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

    def update_tank(self, dt):
        self.update_collisions()
        if self.rotating:
            self.turn(self.rotating_clockwise, dt)
        if self.moving:
            self.move_forward(dt)
        self.projectile_emitter.move_projectiles(dt)

    def turn(self, clockwise, dt):
        if clockwise:
            self.rotation -= self.rotation_speed * dt
        else:
            self.rotation += self.rotation_speed * dt
        self.projectile_emitter.rotation = self.rotation
        self.projectile_emitter.coordinates = self.projectile_emitter.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

    def move_forward(self, dt):

        rad_rotation = math.radians(self.rotation)
        sin = math.sin(rad_rotation)
        cos = math.cos(rad_rotation)
        dir_multi = 1
        if not self.is_forward:
            dir_multi = -1
        coordinates_before = self.coordinates.copy()
        self.coordinates = [self.coordinates[0] - self.speed * sin * dt * dir_multi, self.coordinates[1] - self.speed * cos * dt * dir_multi]
        self.update_object()
        if len(self.obj_rect.collidelistall(self.collision_list)) != 0:
            print('ALARM')
            self.coordinates = coordinates_before

        # self.projectile_emitter.coordinates = [self.coordinates[0], self.coordinates[1] - 50]
        # print(self.coordinates, self.rotation)
        self.update_object()
        self.projectile_emitter.coordinates = self.projectile_emitter.get_emitter_offset(self.coordinates[0], self.coordinates[1], 50, self.rotation)

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
        texture_path = self.get_texture_path(name)
        super().__init__(health, is_able_to_collide, coordinates, name, tag, shot_damage, shot_speed, reload_time, ammo_capacity, speed, screen, size, texture_path, rotation, rotation_speed,
                         game_class)


class Box(GameObject):
    def __init__(self, coordinates, rotation, tag, screen, game_class):
        import materials
        name = "box"
        material = materials.Sprites().get_material_data(name)
        collision_size = material['collision_size']
        sprite_size = material['size']
        destructible = material['destructible']
        super().__init__(name=name, coordinates=coordinates, rotation=rotation, tag=tag, screen=screen, sprite_size=sprite_size, collision_size=collision_size, game_class=game_class, destructible=destructible)
