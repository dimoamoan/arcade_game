import arcade

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from views.space_view import SpaceView


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "LAST FLIGHT HOME",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ENTER to start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(SpaceView())
