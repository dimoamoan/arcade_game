import arcade

from settings import START_FUEL, START_HEALTH, PLAYER_SPEED


class PlayerShip(arcade.Sprite):
    def __init__(self, x: float, y: float):
        """
        Игровой корабль игрока
        """
        super().__init__()

        # ВРЕМЕННО: рисуем корабль как прямоугольник
        # (позже легко заменим на текстуру)
        self.width = 40
        self.height = 20
        self.color = arcade.color.WHITE

        self.center_x = x
        self.center_y = y

        self.change_x = 0
        self.change_y = 0

        self.speed = PLAYER_SPEED
        self.fuel = START_FUEL
        self.health = START_HEALTH

    def update(self):
        """Обновление позиции корабля"""
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self):
        """Отрисовка корабля для старой версии Arcade"""
        # draw_lbwh_rectangle_filled(left, bottom, width, height, color)
        arcade.draw_lbwh_rectangle_filled(
            self.center_x - self.width / 2,  # left
            self.center_y - self.height / 2,  # bottom
            self.width,  # width
            self.height,  # height
            self.color  # цвет
        )

