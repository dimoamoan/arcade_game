import arcade

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class FinalView(arcade.View):
    def __init__(self, win: bool, visited: int, total: int):
        super().__init__()
        self.win = win
        self.visited = visited
        self.total = total

    def on_draw(self):
        self.clear()

        if self.win:
            title = "MISSION COMPLETE"
            color = arcade.color.GREEN
        else:
            title = "MISSION FAILED"
            color = arcade.color.RED

        arcade.draw_text(
            title,
            self.window.width / 2,
            self.window.height / 2 + 40,
            color,
            36,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Visited planets: {self.visited}/{self.total}",
            self.window.width / 2,
            self.window.height / 2 - 10,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ENTER to restart",
            self.window.width / 2,
            self.window.height / 2 - 60,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())
