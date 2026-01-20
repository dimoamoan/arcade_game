import arcade
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class PauseView(arcade.View):

    def on_draw(self):
        self.clear()

        # Затемнение экрана
        arcade.draw_lrbt_rectangle_filled(
            0,
            SCREEN_WIDTH,
            0,
            SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        arcade.draw_text(
            "PAUSE",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "ESC — continue",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.previous_view)
