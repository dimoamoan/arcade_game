import arcade
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Survival: Win or Lose"

PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 3
RESOURCE_SPEED = 2

# Состояния игры
STATE_PLAYING = 0
STATE_WON = 1
STATE_LOST = 2


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Списки спрайтов
        self.player_list = None
        self.alien_list = None
        self.resource_list = None
        self.bullet_list = None

        self.player_sprite = None
        self.score = 0
        self.resources = 0
        self.state = STATE_PLAYING

        # Создаем текстуры программно
        self.player_texture = arcade.make_circle_texture(40, arcade.color.CYAN)
        self.alien_texture = arcade.make_soft_circle_texture(30, arcade.color.RED_ORANGE)
        self.resource_texture = arcade.make_circle_texture(20, arcade.color.GOLD)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def setup(self):
        """ Сброс игры к начальному состоянию """
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.resource_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        self.score = 0
        self.resources = 0
        self.state = STATE_PLAYING

        # Сброс таймеров (чтобы они не дублировались при перезапуске)
        arcade.unschedule(self.spawn_alien)
        arcade.unschedule(self.spawn_resource)
        arcade.schedule(self.spawn_alien, 1.0)
        arcade.schedule(self.spawn_resource, 2.5)

    def draw_game_over(self, title, color):
        """ Универсальный метод для рисования экранов финала """
        arcade.draw_text(title, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
                         color, 50, anchor_x="center")
        arcade.draw_text(f"Счет: {self.score} | Ресурсы: {self.resources}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                         arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text("Нажмите 'R' для перезапуска или 'ESC' для выхода",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80,
                         arcade.color.LIGHT_GRAY, 12, anchor_x="center")

    def on_draw(self):
        self.clear()

        if self.state == STATE_PLAYING:
            self.alien_list.draw()
            self.resource_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()

            arcade.draw_text(f"Счет: {self.score} / 100", 10, 570, arcade.color.WHITE, 12)
            arcade.draw_text(f"Ресурсы: {self.resources} / 100", 10, 550, arcade.color.GOLD, 12)

        elif self.state == STATE_WON:
            self.draw_game_over("ПОБЕДА!", arcade.color.GOLD)

        elif self.state == STATE_LOST:
            self.draw_game_over("ИГРА ОКОНЧЕНА", arcade.color.RED)

    def on_update(self, delta_time):
        if self.state != STATE_PLAYING:
            return

        self.player_list.update()
        self.bullet_list.update()
        self.alien_list.update()
        self.resource_list.update()

        # Ограничения экрана
        if self.player_sprite.left < 0: self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH: self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0: self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT: self.player_sprite.top = SCREEN_HEIGHT

        # Столкновения: пули и враги
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.alien_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for alien in hit_list:
                    alien.remove_from_sprite_lists()
                    self.score += 10

        # Столкновения: игрок и враги (ШТРАФ)
        if arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
            for enemy in arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
                enemy.remove_from_sprite_lists()
                self.score -= 10

        # Сбор ресурсов
        res_list = arcade.check_for_collision_with_list(self.player_sprite, self.resource_list)
        for res in res_list:
            res.remove_from_sprite_lists()
            self.resources += 10

        # ПРОВЕРКА УСЛОВИЙ
        if self.score < 0:
            self.state = STATE_LOST
        elif self.score >= 100 and self.resources >= 100:
            self.state = STATE_WON

        # Чистка памяти
        for alien in self.alien_list:
            if alien.top < 0: alien.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if self.state == STATE_PLAYING:
            if key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_SPEED
            elif key == arcade.key.UP:
                self.player_sprite.change_y = PLAYER_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -PLAYER_SPEED
            elif key == arcade.key.SPACE:
                bullet = arcade.SpriteSolidColor(5, 15, arcade.color.WHITE)
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top
                bullet.change_y = BULLET_SPEED
                self.bullet_list.append(bullet)

        # Перезапуск
        if key == arcade.key.R:
            self.setup()
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT): self.player_sprite.change_x = 0
        if key in (arcade.key.UP, arcade.key.DOWN): self.player_sprite.change_y = 0

    def spawn_alien(self, delta_time):
        if self.state == STATE_PLAYING:
            alien = arcade.Sprite(self.alien_texture)
            alien.center_x = random.randrange(SCREEN_WIDTH)
            alien.top = SCREEN_HEIGHT
            alien.change_y = -ALIEN_SPEED
            self.alien_list.append(alien)

    def spawn_resource(self, delta_time):
        if self.state == STATE_PLAYING:
            res = arcade.Sprite(self.resource_texture)
            res.center_x = random.randrange(SCREEN_WIDTH)
            res.top = SCREEN_HEIGHT
            res.change_y = -RESOURCE_SPEED
            self.resource_list.append(res)


if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()