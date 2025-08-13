import pygame as pg


class GameObject:
    @staticmethod
    def get_texture_path(name):
        import materials
        texture_path = materials.Sprites().get_image_path(name)
        return texture_path

    def __init__(self, health=100.0, is_able_to_collide=True, coordinates=[0,0], name='blank', tag='blank', sprite_size=[100, 100], screen=None, texture_path=None, rotation=0, collision_size=[100, 100]):
        import materials
        import utils
        self.name = name
        self.screen = screen
        self.rotation = rotation
        self.sprite_size = sprite_size
        self.collision_size = [self.sprite_size[0]*0.9, self.sprite_size[1]*0.9]
        self.tag = tag
        self.health = health
        self.is_able_to_collide = is_able_to_collide
        self.coordinates = coordinates
        self.texture_path = texture_path
        self.sprites = materials.Sprites()
        self.obj_sprite = utils.load_image(self.sprites.get_image_path(self.name))
        self.obj_rect = self.obj_sprite.get_rect()
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]



    def update_object(self):
        obj_sprite = pg.transform.scale(self.obj_sprite, self.sprite_size)
        copy_obj = pg.transform.rotate(obj_sprite, self.rotation)
        self.obj_rect.x = self.coordinates[0]
        self.obj_rect.y = self.coordinates[1]
        self.obj_rect.size = self.collision_size
        # if self.tag == "Box1":
        #     print(self.obj_rect)


        self.screen.blit(copy_obj, (self.coordinates[0] - int(copy_obj.get_width()/2), self.coordinates[1] - int(copy_obj.get_height()/2)))








class Tank(GameObject):
    def __init__(self, health: float, is_able_to_collide: bool, coordinates: list, name: str, tag: str, shot_damage: float, shot_speed: float, reload_time: float, ammo_capacity: int, speed: float, screen, sprite_size, texture_path, rotation, rotation_speed, collision_list):
        super().__init__(health, is_able_to_collide, coordinates, name, tag, sprite_size, screen, texture_path, rotation)
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
        self.collision_list = collision_list


    def update_inputs(self, dt):
        if self.rotating:
            self.turn(self.rotating_clockwise, dt)
        if self.moving:
            self.move_forward(dt)


    def turn(self, clockwise, dt):
        if clockwise:
            self.rotation -= self.rotation_speed * dt
        else:
            self.rotation += self.rotation_speed * dt

    def move_forward(self, dt):
        import math
        rad_rotation = math.radians(self.rotation)
        sin = math.sin(rad_rotation)
        cos = math.cos(rad_rotation)
        dir_multi = 1
        if not self.is_forward:
            dir_multi = -1
        coordinates_before = self.coordinates.copy()
        self.coordinates = [self.coordinates[0] - self.speed * sin * dt * dir_multi, self.coordinates[1] - self.speed * cos * dt * dir_multi]
        self.update_object()
        # print(self.obj_rect.x)
        # if self.tag == "LT":
        #     print(self.obj_rect)
        #     print(self.obj_rect.collidelistall(self.collision_list))
        if len(self.obj_rect.collidelistall(self.collision_list)) != 0:
            # print('ALARM')
            self.coordinates = coordinates_before
            self.update_object()

    def change_moving_state(self, state, is_forward):
        self.moving = state
        self.is_forward = is_forward

    def change_rotation_state(self, state, clockwise):
        if not state and clockwise != self.rotating_clockwise:
            return
        self.rotating = state
        self.rotating_clockwise = clockwise

    def read_json(self, json_name, tank_name):
        import json
        with open(json_name, "r") as f:
            data = f.read()
        json_string = json.loads(data)
        return json_string[tank_name]


class LightTank(Tank):
    def __init__(self, coordinates, rotation, tag, screen, collision_list):
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
        super().__init__(health, is_able_to_collide, coordinates, name, tag, shot_damage, shot_speed, reload_time, ammo_capacity, speed, screen, size, texture_path, rotation, rotation_speed, collision_list)



class Box(GameObject):
    def __init__(self, coordinates, rotation, tag, screen):
        import materials
        name = "box"
        material = materials.Sprites().get_material_data(name)
        collision_size = material['collision_size']
        sprite_size = material['size']
        print(material)
        super().__init__(name=name, coordinates=coordinates, rotation=rotation, tag=tag, screen=screen, sprite_size=sprite_size, collision_size=collision_size)



class Player(GameObject):
    pass


class Enemy(GameObject):
    pass



