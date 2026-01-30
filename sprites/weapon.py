# sprites/weapon.py
import arcade

class WeaponPickup(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y

        self.texture = arcade.make_soft_square_texture(
            14, arcade.color.RED, 255
        )