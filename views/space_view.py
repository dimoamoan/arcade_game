import arcade
from views.pause_view import PauseView


from settings import SCREEN_HEIGHT
from views.final_view import FinalView


class SpaceView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "SPACE",
            50,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            "Press F to finish (debug)",
            50,
            SCREEN_HEIGHT - 80,
            arcade.color.LIGHT_GRAY,
            14
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause = PauseView()
            pause.window = self.window
            self.window.previous_view = self
            self.window.show_view(pause)
        elif key == arcade.key.F:
            self.window.show_view(FinalView())




