import arcade
import math


class CelestialBody:
    def __init__(
            self,
            x,
            y,
            radius,
            mass,
            color,
            orbit_center=None,
            orbit_radius=None,
            orbit_angle=0,
            body_type="planet",
            planet_index=0
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.orbit_center = orbit_center
        self.orbit_radius = orbit_radius
        self.orbit_angle = orbit_angle
        self.body_type = body_type

        self.planet_index = planet_index
        self.visited = False


    def draw(self):
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            self.color
        )

        if self.body_type == "planet":
            arcade.draw_text(str(self.planet_index), self.x, self.y, arcade.color.WHITE, 12, anchor_x="center")


    def draw_orbit(self):
        if self.orbit_center is None:
            return

        color = arcade.color.DARK_GREEN if self.visited else arcade.color.RED

        arcade.draw_circle_outline(
            self.orbit_center[0],
            self.orbit_center[1],
            self.orbit_radius,
            color,
            2
        )


    def update_orbit(self):
        if self.orbit_center is None:
            return

        cx, cy = self.orbit_center
        self.x = cx + self.orbit_radius * math.cos(self.orbit_angle)
        self.y = cy + self.orbit_radius * math.sin(self.orbit_angle)


    def gravity_at(self, ship):
        dx = self.x - ship.center_x
        dy = self.y - ship.center_y

        dist_sq = dx * dx + dy * dy
        dist = math.sqrt(dist_sq)

        if dist < self.radius:
            return 0, 0

        dist_sq = max(dist_sq, 400)

        G = 800
        force = G * self.mass / dist_sq

        ax = dx / dist * force
        ay = dy / dist * force

        return ax, ay