import arcade
import random
import constants as c  # Импортируем наш файл с константами


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)

        self.player_list = None
        self.alien_list = None
        self.resource_list = None
        self.bullet_list = None

        # Переменные для фона и звуков
        self.background_texture = None
        self.sound_shoot = None
        self.sound_collect = None
        self.sound_hit = None

        self.player_sprite = None
        self.score = 0
        self.resources = 0
        self.state = c.STATE_PLAYING

        # Программные текстуры (оставляем, чтобы не грузить лишние файлы спрайтов)
        self.player_texture = arcade.make_circle_texture(40, arcade.color.CYAN)
        self.alien_texture = arcade.make_soft_circle_texture(30, arcade.color.RED_ORANGE)
        self.resource_texture = arcade.make_circle_texture(20, arcade.color.GOLD)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.resource_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Загрузка внешних ресурсов
        try:
            self.background_texture = arcade.load_texture(c.BACKGROUND_PATH)
            self.sound_shoot = arcade.load_sound(c.SOUND_SHOOT)
            self.sound_collect = arcade.load_sound(c.SOUND_COLLECT)
            self.sound_hit = arcade.load_sound(c.SOUND_HIT)
        except Exception as e:
            print(f"Ошибка загрузки файлов: {e}. Проверьте наличие файлов в папке.")

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = c.SCREEN_WIDTH // 2
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        self.score = 0
        self.resources = 0
        self.state = c.STATE_PLAYING

        arcade.unschedule(self.spawn_alien)
        arcade.unschedule(self.spawn_resource)
        arcade.schedule(self.spawn_alien, 1.0)
        arcade.schedule(self.spawn_resource, 2.5)

    def on_draw(self):
        self.clear()

        # Рисуем фон, если он загружен
        if self.background_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT, self.background_texture)
        else:
            arcade.set_background_color(arcade.color.BLACK_OLIVE)

        if self.state == c.STATE_PLAYING:
            self.alien_list.draw()
            self.resource_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()

            arcade.draw_text(f"Счет: {self.score} / {c.WIN_SCORE}", 10, 570, arcade.color.WHITE, 12)
            arcade.draw_text(f"Ресурсы: {self.resources} / {c.WIN_RESOURCES}", 10, 550, arcade.color.GOLD, 12)

        elif self.state == c.STATE_WON:
            self.draw_end_screen("ПОБЕДА!", arcade.color.GOLD)
        elif self.state == c.STATE_LOST:
            self.draw_end_screen("ИГРА ОКОНЧЕНА", arcade.color.RED)

    def draw_end_screen(self, title, color):
        arcade.draw_text(title, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 + 20, color, 50, anchor_x="center")
        arcade.draw_text("Нажмите 'R' для перезапуска", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 40,
                         arcade.color.WHITE, 16, anchor_x="center")

    def on_update(self, delta_time):
        if self.state != c.STATE_PLAYING:
            return

        self.player_list.update()
        self.bullet_list.update()
        self.alien_list.update()
        self.resource_list.update()

        # Столкновения: пули и враги
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.alien_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                if self.sound_hit: arcade.play_sound(self.sound_hit)
                for alien in hit_list:
                    alien.remove_from_sprite_lists()
                    self.score += 10

        # Столкновения: игрок и враги
        enemy_hits = arcade.check_for_collision_with_list(self.player_sprite, self.alien_list)
        if enemy_hits:
            if self.sound_hit: arcade.play_sound(self.sound_hit)
            for enemy in enemy_hits:
                enemy.remove_from_sprite_lists()
                self.score -= 10

        # Сбор ресурсов
        res_hits = arcade.check_for_collision_with_list(self.player_sprite, self.resource_list)
        if res_hits:
            if self.sound_collect: arcade.play_sound(self.sound_collect)
            for res in res_hits:
                res.remove_from_sprite_lists()
                self.resources += 10

        if self.score < 0:
            self.state = c.STATE_LOST
        elif self.score >= c.WIN_SCORE and self.resources >= c.WIN_RESOURCES:
            self.state = c.STATE_WON

    def on_key_press(self, key, modifiers):
        if self.state == c.STATE_PLAYING:
            if key == arcade.key.LEFT:
                self.player_sprite.change_x = -c.PLAYER_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = c.PLAYER_SPEED
            elif key == arcade.key.UP:
                self.player_sprite.change_y = c.PLAYER_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -c.PLAYER_SPEED
            elif key == arcade.key.SPACE:
                if self.sound_shoot: arcade.play_sound(self.sound_shoot)
                bullet = arcade.SpriteSolidColor(5, 15, arcade.color.WHITE)
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top
                bullet.change_y = c.BULLET_SPEED
                self.bullet_list.append(bullet)

        if key == arcade.key.R:
            self.setup()
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT): self.player_sprite.change_x = 0
        if key in (arcade.key.UP, arcade.key.DOWN): self.player_sprite.change_y = 0

    def spawn_alien(self, delta_time):
        if self.state == c.STATE_PLAYING:
            alien = arcade.Sprite(self.alien_texture)
            alien.center_x = random.randrange(c.SCREEN_WIDTH)
            alien.top = c.SCREEN_HEIGHT
            alien.change_y = -c.ALIEN_SPEED
            self.alien_list.append(alien)

    def spawn_resource(self, delta_time):
        if self.state == c.STATE_PLAYING:
            res = arcade.Sprite(self.resource_texture)
            res.center_x = random.randrange(c.SCREEN_WIDTH)
            res.top = c.SCREEN_HEIGHT
            res.change_y = -c.RESOURCE_SPEED
            self.resource_list.append(res)


if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
