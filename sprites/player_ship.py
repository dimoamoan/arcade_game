import arcade
import math
from settings import START_FUEL, START_HEALTH

class PlayerShip:
    def __init__(self, x: float, y: float):
        self.center_x = x
        self.center_y = y


        self.angle = 0  # градусов


        self.vx = 0.0
        self.vy = 0.0


        self.throttle = 0.0
        self.thrust = 1200
        self.turn_speed = 180

        # ресурсы
        self.fuel = START_FUEL
        self.health = START_HEALTH
        self.score = 0

        self.color = arcade.color.WHITE


    def update(self, dt: float):

        if self.throttle > 0 and self.fuel > 0:
            self.fuel -= self.throttle * dt * 15

            rad = math.radians(self.angle)
            ax = math.cos(rad) * self.throttle * self.thrust
            ay = math.sin(rad) * self.throttle * self.thrust

            self.vx += ax * dt
            self.vy += ay * dt


        self.center_x += self.vx * dt
        self.center_y += self.vy * dt


    def draw(self):

        local_points = [
            (-14,  9),
            (20,   0),
            (-14, -9)
        ]

        rad = math.radians(self.angle)
        points = []

        for x, y in local_points:
            rx = x * math.cos(rad) - y * math.sin(rad)
            ry = x * math.sin(rad) + y * math.cos(rad)
            points.append((self.center_x + rx, self.center_y + ry))

        arcade.draw_polygon_filled(points, self.color)


        if self.throttle > 0 and self.fuel > 0:
            back_x = self.center_x - math.cos(rad) * 14
            back_y = self.center_y - math.sin(rad) * 14

            arcade.draw_circle_filled(
                back_x,
                back_y,
                5 + self.throttle * 6,
                arcade.color.ORANGE_RED
            )
