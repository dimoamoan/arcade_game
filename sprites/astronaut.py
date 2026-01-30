# sprites/astronaut.py
import arcade

class Astronaut(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y

        self.speed = 220
        self.health = 100

        self.texture = arcade.make_soft_square_texture(
            28, arcade.color.WHITE, 255
        )

    def update(self, dt):
        self.center_x += self.change_x * dt
        self.center_y += self.change_y * dt