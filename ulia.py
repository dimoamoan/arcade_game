import arcade
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Geometry Shooter"

PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 2
RESOURCE_SPEED = 1.5


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.resource_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player_sprite = None
        self.score = 0
        self.resources = 0

        # Создаем текстуры программно
        self.player_texture = arcade.make_circle_texture(40, arcade.color.CYAN)
        self.alien_texture = arcade.make_soft_circle_texture(30, arcade.color.RED_ORANGE)
        self.resource_texture = arcade.make_circle_texture(20, arcade.color.GOLD)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def setup(self):
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Таймеры появления
        arcade.schedule(self.spawn_alien, 1.5)
        arcade.schedule(self.spawn_resource, 3.5)

    def on_draw(self):
        self.clear()

        # Рисуем списки объектов
        self.alien_list.draw()
        self.resource_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # Интерфейс
        arcade.draw_text(f"Счет: {self.score}", 10, 570, arcade.color.WHITE, 12)
        arcade.draw_text(f"Ресурсы: {self.resources}", 10, 550, arcade.color.GOLD, 12)

    # ВАЖНО: Метод должен называться on_update
    def on_update(self, delta_time):
        self.player_list.update()
        self.bullet_list.update()
        self.alien_list.update()
        self.resource_list.update()

        # Ограничение игрока в пределах экрана
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        # Проверка попаданий пуль во врагов
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.alien_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for alien in hit_list:
                    alien.remove_from_sprite_lists()
                    self.score += 10

        # Сбор ресурсов
        resources_got = arcade.check_for_collision_with_list(self.player_sprite, self.resource_list)
        for res in resources_got:
            res.remove_from_sprite_lists()
            self.resources += 1

        # Удаление пуль за экраном
        for bullet in self.bullet_list:
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(5, 15, arcade.color.WHITE)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

    def spawn_alien(self, delta_time):
        alien = arcade.Sprite(self.alien_texture)
        alien.center_x = random.randrange(SCREEN_WIDTH)
        alien.top = SCREEN_HEIGHT
        alien.change_y = -ALIEN_SPEED
        self.alien_list.append(alien)

    def spawn_resource(self, delta_time):
        res = arcade.Sprite(self.resource_texture)
        res.center_x = random.randrange(SCREEN_WIDTH)
        res.top = SCREEN_HEIGHT
        res.change_y = -RESOURCE_SPEED
        self.resource_list.append(res)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()