import arcade
from sprites.player_ship import PlayerShip


class SpaceView(arcade.View):
    def __init__(self):
        super().__init__()


        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()


        self.ship = PlayerShip(0, 0)


        self.keys = set()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, key, modifiers):
        self.keys.add(key)

    def on_key_release(self, key, modifiers):
        self.keys.discard(key)

    def on_update(self, dt):
        if arcade.key.LEFT in self.keys:
            self.ship.angle += self.ship.turn_speed * dt
        if arcade.key.RIGHT in self.keys:
            self.ship.angle -= self.ship.turn_speed * dt

        # ТЯГА
        if arcade.key.UP in self.keys:
            self.ship.throttle = min(1.0, self.ship.throttle + 1.5 * dt)
        elif arcade.key.DOWN in self.keys:
            self.ship.throttle = max(0.0, self.ship.throttle - 3.5 * dt)

        self.ship.update(dt)


        self.world_camera.position = (
            self.ship.center_x,
            self.ship.center_y
        )

    def on_draw(self):
        self.clear()


        self.world_camera.use()
        self.draw_grid()
        self.ship.draw()


        self.gui_camera.use()
        self.draw_hud()


    def draw_grid(self):
        step = 200
        size = 3000

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



