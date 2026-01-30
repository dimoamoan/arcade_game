# sprites/alien.py
import arcade
import random
import math

class Alien(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y

        self.health = 40
        self.speed = 40

        self.texture = arcade.make_soft_circle_texture(
            26, arcade.color.GREEN, 255
        )

        self.direction = random.uniform(0, math.tau)
        self.timer = random.uniform(1, 3)

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.direction = random.uniform(0, math.tau)
            self.timer = random.uniform(1, 3)

        self.center_x += math.cos(self.direction) * self.speed * dt
        self.center_y += math.sin(self.direction) * self.speed * dt