import arcade
from sprites.player_ship import PlayerShip
from sprites.celestial_body import CelestialBody
import math
from views.victory_view import VictoryView
import random
from views.final_view import FinalView


class SpaceView(arcade.View):
    def __init__(self):
        super().__init__()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.ship = PlayerShip(0, 0)

        self.keys = set()

        self.bodies = []

        self.black_hole = CelestialBody(
            0,
            0,
            radius=120,
            mass=80000,
            color=arcade.color.BLACK,
            body_type="black_hole"
        )

        self.bodies.append(self.black_hole)

        center = (0, 0)

        colors = [
            arcade.color.BLUE,
            arcade.color.GREEN,
            arcade.color.ORANGE,
            arcade.color.CYAN,
            arcade.color.PURPLE,
            arcade.color.BROWN,
            arcade.color.LIGHT_BLUE,
        ]

        orbit_radii = [600, 1000, 1500, 2100, 2800, 3600, 4500]

        for i, orbit_radius in enumerate(orbit_radii):
            angle = random.uniform(0, math.tau)

            planet_radius = random.randint(30, 70)
            mass = planet_radius * 40

            body = CelestialBody(
                x=0,
                y=0,
                radius=planet_radius,
                mass=mass,
                color=colors[i % len(colors)],
                orbit_center=center,
                orbit_radius=orbit_radius,
                orbit_angle=angle,
                body_type="planet"
            )

            body.update_orbit()
            self.bodies.append(body)

        planets = [b for b in self.bodies if b.body_type == "planet"]

        farthest = max(
            planets,
            key=lambda b: math.hypot(b.x, b.y)
        )

        self.ship.center_x = farthest.x + farthest.radius + 80
        self.ship.center_y = farthest.y
        self.ship.vx = 0
        self.ship.vy = 0

        self.visited_planets = 0
        self.total_planets = len(self.bodies)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, key, modifiers):
        self.keys.add(key)

    def on_key_release(self, key, modifiers):
        self.keys.discard(key)

    def on_update(self, dt):
        for body in self.bodies:
            ax, ay = body.gravity_at(self.ship)
            self.ship.apply_gravity(ax, ay, dt)

        if arcade.key.LEFT in self.keys:
            self.ship.angle += self.ship.turn_speed * dt
        if arcade.key.RIGHT in self.keys:
            self.ship.angle -= self.ship.turn_speed * dt

        if arcade.key.UP in self.keys:
            self.ship.throttle = min(1.0, self.ship.throttle + 1.5 * dt)
        elif arcade.key.DOWN in self.keys:
            self.ship.throttle = max(0.0, self.ship.throttle - 3.5 * dt)

        for body in self.bodies:
            dx = self.ship.center_x - body.x
            dy = self.ship.center_y - body.y
            dist = math.hypot(dx, dy)

            if dist <= body.radius + 5:
                speed = math.hypot(self.ship.vx, self.ship.vy)

                if speed < 250:
                    self.land_on(body)
                else:
                    self.ship.health -= 20
                    self.land_on(body)

        if self.ship.landed and arcade.key.UP in self.keys:
            self.ship.landed = False
            self.ship.landed_body = None

            rad = math.radians(self.ship.angle)
            self.ship.vx += math.cos(rad) * 150
            self.ship.vy += math.sin(rad) * 150

        self.ship.update(dt)

        self.world_camera.position = (
            self.ship.center_x,
            self.ship.center_y
        )

        for body in self.bodies:
            if body.body_type != "planet":
                continue

            dx = self.ship.center_x - body.x
            dy = self.ship.center_y - body.y
            dist = math.hypot(dx, dy)

            if dist < body.radius + 5 and not body.visited:
                body.visited = True
                self.visited_planets += 1

        dx = self.ship.center_x - self.black_hole.x
        dy = self.ship.center_y - self.black_hole.y
        dist = math.hypot(dx, dy)

        if dist < self.black_hole.radius + 5:
            if self.visited_planets == self.total_planets:
                victory = VictoryView()
                self.window.show_view(victory)
            else:
                self.window.show_view(
                    FinalView(
                        win=False,
                        visited=self.visited_planets,
                        total=self.total_planets
                    )
                )

        if self.ship.health <= 0:
            self.window.show_view(
                FinalView(
                    win=False,
                    visited=self.visited_planets,
                    total=self.total_planets
                )
            )
            return

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        self.draw_grid()

        for body in self.bodies:
            body.draw_orbit()

        for body in self.bodies:
            body.draw()

        self.ship.draw()

        self.gui_camera.use()
        self.draw_hud()

    def draw_grid(self):
        step = 300
        size = 15000

        for x in range(-size, size + 1, step):
            arcade.draw_line(x, -size, x, size, arcade.color.DARK_GRAY)

        for y in range(-size, size + 1, step):
            arcade.draw_line(-size, y, size, y, arcade.color.DARK_GRAY)

    def draw_hud(self):
        padding = 10
        panel_width = 280
        panel_height = 80

        left = padding
        bottom = self.window.height - panel_height - padding

        arcade.draw_lbwh_rectangle_filled(
            left,
            bottom,
            panel_width,
            panel_height,
            arcade.color.BLACK_OLIVE
        )

        arcade.draw_lbwh_rectangle_outline(
            left,
            bottom,
            panel_width,
            panel_height,
            arcade.color.WHITE,
            2
        )

        arcade.draw_text(
            f"Fuel: {int(self.ship.fuel)}",
            left + 10,
            bottom + panel_height - 25,
            arcade.color.WHITE,
            14
        )

        arcade.draw_text(
            f"Health: {int(self.ship.health)}",
            left + 10,
            bottom + panel_height - 45,
            arcade.color.WHITE,
            14
        )

        arcade.draw_text(
            f"Score: {self.ship.score}",
            left + 10,
            bottom + panel_height - 65,
            arcade.color.WHITE,
            14
        )

        arcade.draw_text(
            f"X: {int(self.ship.center_x)}  Y: {int(self.ship.center_y)}",
            padding,
            10,
            arcade.color.GRAY,
            12
        )

        arcade.draw_text(
            f"Throttle: {int(self.ship.throttle * 100)}%",
            left + 150,
            bottom + panel_height - 25,
            arcade.color.WHITE,
            14
        )

        status = "LANDED" if self.ship.landed else "FLYING"

        arcade.draw_text(
            f"Status: {status}",
            left + 150,
            bottom + panel_height - 45,
            arcade.color.WHITE,
            14
        )

        speed = self.ship.get_speed()

        arcade.draw_text(
            f"Speed: {speed:.1f}",
            left + 150,
            bottom + panel_height - 65,
            arcade.color.WHITE,
            14
        )

        arcade.draw_text(
            f"Visited: {self.visited_planets}/{self.total_planets}",
            left + 150,
            bottom + panel_height - 45,
            arcade.color.LIME,
            14
        )

    def land_on(self, body):
        dx = self.ship.center_x - body.x
        dy = self.ship.center_y - body.y
        dist = math.hypot(dx, dy)

        if dist == 0:
            nx, ny = 1, 0
        else:
            nx = dx / dist
            ny = dy / dist

        self.ship.center_x = body.x + nx * (body.radius + 5)
        self.ship.center_y = body.y + ny * (body.radius + 5)

        self.ship.vx = 0
        self.ship.vy = 0
        self.ship.throttle = 0

        self.ship.landed = True
        self.ship.landed_body = body
