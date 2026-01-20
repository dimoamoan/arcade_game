import arcade
from views.pause_view import PauseView
from views.final_view import FinalView
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites.player_ship import PlayerShip


class SpaceView(arcade.View):
    def __init__(self):
        super().__init__()

        # Инициализация корабля сразу
        self.ship = PlayerShip(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

        # Набор нажатых клавиш
        self.pressed_keys = set()

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

        # Сбрасываем позицию корабля при повторном показе
        self.ship.center_x = SCREEN_WIDTH // 2
        self.ship.center_y = SCREEN_HEIGHT // 2

    def on_update(self, delta_time):
        # Защита на всякий случай
        if self.ship is None:
            return

        self.ship.change_x = 0
        self.ship.change_y = 0

        if self.ship.fuel > 0:
            if "up" in self.pressed_keys:
                self.ship.change_y += self.ship.speed
            if "down" in self.pressed_keys:
                self.ship.change_y -= self.ship.speed
            if "left" in self.pressed_keys:
                self.ship.change_x -= self.ship.speed
            if "right" in self.pressed_keys:
                self.ship.change_x += self.ship.speed

            if self.pressed_keys:
                self.ship.fuel -= 1

        self.ship.update()

    def on_draw(self):
        self.clear()

        if self.ship:
            self.ship.draw()

        arcade.draw_text(
            f"Fuel: {self.ship.fuel if self.ship else 0}",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            14
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause = PauseView()
            pause.previous_view = self
            self.window.show_view(pause)

        if key in (arcade.key.W, arcade.key.UP):
            self.pressed_keys.add("up")
        if key in (arcade.key.S, arcade.key.DOWN):
            self.pressed_keys.add("down")
        if key in (arcade.key.A, arcade.key.LEFT):
            self.pressed_keys.add("left")
        if key in (arcade.key.D, arcade.key.RIGHT):
            self.pressed_keys.add("right")

        if key == arcade.key.F:
            self.window.show_view(FinalView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.pressed_keys.discard("up")
        if key in (arcade.key.S, arcade.key.DOWN):
            self.pressed_keys.discard("down")
        if key in (arcade.key.A, arcade.key.LEFT):
            self.pressed_keys.discard("left")
        if key in (arcade.key.D, arcade.key.RIGHT):
            self.pressed_keys.discard("right")
