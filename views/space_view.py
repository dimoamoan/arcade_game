import arcade
from sprites.player_ship import PlayerShip
from sprites.celestial_body import CelestialBody
import math
from views.victory_view import VictoryView
import random
from views.final_view import FinalView

# ИМПОРТИРУЕМ НОВЫЙ ВИД ВМЕСТО СТАРОГО
from views.minigame_view import MiniGameView


class SpaceView(arcade.View):

    def __init__(self):
        super().__init__()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.ship = PlayerShip(0, 0)
        self.keys = set()
        self.bodies = []

        self.black_hole = CelestialBody(
            0, 0, radius=120, mass=80000,
            color=arcade.color.BLACK, body_type="black_hole"
        )
        self.bodies.append(self.black_hole)

        center = (0, 0)
        colors = [
            arcade.color.BLUE, arcade.color.GREEN, arcade.color.ORANGE,
            arcade.color.CYAN, arcade.color.PURPLE, arcade.color.BROWN,
            arcade.color.LIGHT_BLUE,
        ]
        orbit_radii = [600, 1000, 1500, 2100, 2800, 3600, 4500]

        # ГЕНЕРАЦИЯ ПЛАНЕТ С НОМЕРАМИ
        for i, orbit_radius in enumerate(orbit_radii):
            angle = random.uniform(0, math.tau)
            planet_radius = random.randint(30, 70)
            mass = planet_radius * 40

            # i + 1, чтобы уровни начинались с 1, а не с 0
            planet_number = i + 1

            body = CelestialBody(
                x=0, y=0,
                radius=planet_radius,
                mass=mass,
                color=colors[i % len(colors)],
                orbit_center=center,
                orbit_radius=orbit_radius,
                orbit_angle=angle,
                body_type="planet",
                planet_index=planet_number  # <--- ПЕРЕДАЕМ НОМЕР
            )

            body.update_orbit()
            self.bodies.append(body)

        # Логика старта (спавн корабля у самой дальней)
        planets = [b for b in self.bodies if b.body_type == "planet"]
        farthest = max(planets, key=lambda b: math.hypot(b.x, b.y))

        self.ship.center_x = farthest.x + farthest.radius + 80
        self.ship.center_y = farthest.y
        self.ship.vx = 0
        self.ship.vy = 0

        self.visited_planets = 0
        self.total_planets = len(self.bodies) - 1  # минус черная дыра

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, key, modifiers):
        self.keys.add(key)

    def on_key_release(self, key, modifiers):
        self.keys.discard(key)

    def on_update(self, dt):
        # Гравитация
        for body in self.bodies:
            ax, ay = body.gravity_at(self.ship)
            self.ship.apply_gravity(ax, ay, dt)

        # Управление
        if arcade.key.LEFT in self.keys:
            self.ship.angle += self.ship.turn_speed * dt
        if arcade.key.RIGHT in self.keys:
            self.ship.angle -= self.ship.turn_speed * dt

        if arcade.key.UP in self.keys:
            self.ship.throttle = min(1.0, self.ship.throttle + 1.5 * dt)
        elif arcade.key.DOWN in self.keys:
            self.ship.throttle = max(0.0, self.ship.throttle - 3.5 * dt)

        # Проверка приземления
        for body in self.bodies:
            dx = self.ship.center_x - body.x
            dy = self.ship.center_y - body.y
            dist = math.hypot(dx, dy)

            if dist <= body.radius + 5:
                # Если это не черная дыра
                if body.body_type == "planet":
                    speed = math.hypot(self.ship.vx, self.ship.vy)
                    if speed >= 250:
                        self.ship.health -= 20
                    self.land_on(body)
                elif body.body_type == "black_hole":
                    # Логика черной дыры (победа или конец)
                    if self.visited_planets == self.total_planets:
                        self.window.show_view(VictoryView())
                    else:
                        self.window.show_view(FinalView(False, self.visited_planets, self.total_planets))

        # Если взлетели (пока не используется, т.к. мы уходим в мини-игру)
        if self.ship.landed and arcade.key.UP in self.keys:
            pass

        rad = math.radians(self.ship.angle)
        # Сопротивление среды (космос, но для играбельности)
        self.ship.vx *= 0.99
        self.ship.vy *= 0.99

        self.ship.update(dt)

        self.world_camera.position = (self.ship.center_x, self.ship.center_y)

        # Проверка жизни
        if self.ship.health <= 0:
            self.window.show_view(FinalView(False, self.visited_planets, self.total_planets))

    def land_on(self, body):
        # Ставим корабль на поверхность визуально
        dx = self.ship.center_x - body.x
        dy = self.ship.center_y - body.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            nx, ny = 1, 0
        else:
            nx, ny = dx / dist, dy / dist

        self.ship.center_x = body.x + nx * (body.radius + 5)
        self.ship.center_y = body.y + ny * (body.radius + 5)
        self.ship.vx = 0
        self.ship.vy = 0
        self.ship.throttle = 0
        self.ship.landed = True
        self.ship.landed_body = body

        # ЗАПУСК ВТОРОЙ ИГРЫ
        # Передаем self (SpaceView), чтобы вернуться назад
        # И передаем body.planet_index, чтобы открыть нужный уровень
        minigame = MiniGameView(self, body.planet_index)
        self.window.show_view(minigame)



    def draw_grid(self):
        step = 300
        size = 15000
        for x in range(-size, size + 1, step):
            arcade.draw_line(x, -size, x, size, arcade.color.DARK_GRAY)
        for y in range(-size, size + 1, step):
            arcade.draw_line(-size, y, size, y, arcade.color.DARK_GRAY)

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


    def draw_hud(self):
        padding = 10
        panel_width = 280
        panel_height = 80
        left = padding
        bottom = self.window.height - panel_height - padding

        arcade.draw_lbwh_rectangle_filled(left, bottom, panel_width, panel_height, arcade.color.BLACK_OLIVE)
        arcade.draw_lbwh_rectangle_outline(left, bottom, panel_width, panel_height, arcade.color.WHITE, 2)

        arcade.draw_text(f"Fuel: {int(self.ship.fuel)}", left + 10, bottom + panel_height - 25, arcade.color.WHITE, 14)
        arcade.draw_text(f"Health: {int(self.ship.health)}", left + 10, bottom + panel_height - 45, arcade.color.WHITE,
                         14)
        arcade.draw_text(f"Score: {self.ship.score}", left + 10, bottom + panel_height - 65, arcade.color.WHITE, 14)
        arcade.draw_text(f"Speed: {self.ship.get_speed():.1f}", left + 150, bottom + panel_height - 65,
                         arcade.color.WHITE, 14)
        arcade.draw_text(f"Visited: {self.visited_planets}/{self.total_planets}", left + 150,
                         bottom + panel_height - 45, arcade.color.LIME, 14)