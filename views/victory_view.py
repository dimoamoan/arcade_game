import arcade

class VictoryView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "YOU ESCAPED THE SYSTEM",
            self.window.width // 2,
            self.window.height // 2 + 40,
            arcade.color.LIME,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ENTER to exit",
            self.window.width // 2,
            self.window.height // 2 - 20,
            arcade.color.GRAY,
            16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            arcade.exit()
