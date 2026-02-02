import arcade
import random
import math


class MiniGameView(arcade.View):
    def __init__(self, space_view, level_index, planet_body):
        super().__init__()
        self.space_view = space_view
        self.level = level_index
        self.planet_body = planet_body


        self.win_resources_target = 3 + self.level
        self.win_score_target = 50 + (self.level * 20)
        self.current_alien_speed = 2 + (self.level * 0.5)

        self.score = 0
        self.resources_collected = 0
        self.game_over = False
        self.victory = False


        self.player_texture = arcade.make_circle_texture(30, arcade.color.CYAN)
        self.alien_texture = arcade.make_soft_circle_texture(30, arcade.color.RED_ORANGE)
        self.resource_texture = arcade.make_circle_texture(20, arcade.color.GOLD)


        self.ui_text_level = arcade.Text(f"PLANET {self.level}", 10, self.window.height - 30, arcade.color.WHITE, 20)
        self.ui_text_score = arcade.Text("", 10, self.window.height - 60, arcade.color.WHITE, 14)
        self.ui_text_res = arcade.Text("", 10, self.window.height - 80, arcade.color.GOLD, 14)

        self.end_text_title = arcade.Text("", self.window.width / 2, self.window.height / 2 + 20,
                                          arcade.color.WHITE, 40, anchor_x="center")
        self.end_text_sub = arcade.Text("Press SPACE to takeoff", self.window.width / 2,
                                        self.window.height / 2 - 40,
                                        arcade.color.CYAN, 16, anchor_x="center")

        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.resource_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = self.window.width // 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        arcade.unschedule(self.spawn_alien)
        arcade.unschedule(self.spawn_resource)
        spawn_rate = max(0.2, 1.0 - (self.level * 0.05))
        arcade.schedule(self.spawn_alien, spawn_rate)
        arcade.schedule(self.spawn_resource, 2.0)

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        self.player_list.draw()
        self.alien_list.draw()
        self.resource_list.draw()
        self.bullet_list.draw()

        self.ui_text_score.text = f"Score: {self.score}/{self.win_score_target}"
        self.ui_text_res.text = f"Resources: {self.resources_collected}/{self.win_resources_target}"
        self.ui_text_level.draw()
        self.ui_text_score.draw()
        self.ui_text_res.draw()

        if self.game_over:
            self.draw_end_screen("MISSION FAILED", arcade.color.RED)
        elif self.victory:
            self.draw_end_screen("PLANET CONQUERED", arcade.color.GREEN)

    def draw_end_screen(self, title, color):
        arcade.draw_lrbt_rectangle_filled(0, self.window.width,
            0,
            self.window.height,
            (0, 0, 0, 200))

        self.end_text_title.text = title
        self.end_text_title.color = color
        self.end_text_title.draw()
        self.end_text_sub.draw()

    def on_update(self, dt):
        if self.game_over or self.victory:
            return

        self.player_list.update()
        self.bullet_list.update()


        if self.player_sprite.left < 0: self.player_sprite.left = 0
        if self.player_sprite.right > self.window.width: self.player_sprite.right = self.window.width


        for sprite in self.alien_list:
            sprite.center_y -= self.current_alien_speed
            if sprite.top < 0: sprite.remove_from_sprite_lists()

        for sprite in self.resource_list:
            sprite.center_y -= 2
            if sprite.top < 0: sprite.remove_from_sprite_lists()


        for bullet in self.bullet_list:
            hit = arcade.check_for_collision_with_list(bullet, self.alien_list)
            if hit:
                bullet.remove_from_sprite_lists()
                for alien in hit:
                    alien.remove_from_sprite_lists()
                    self.score += 10


        if arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
            self.score -= 10
            for alien in arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
                alien.remove_from_sprite_lists()

        for res in arcade.check_for_collision_with_list(self.player_sprite, self.resource_list):
            res.remove_from_sprite_lists()
            self.resources_collected += 1

        if self.score >= self.win_score_target and self.resources_collected >= self.win_resources_target:
            self.victory = True

            self.space_view.ship.score += self.score
            self.space_view.ship.fuel += self.resources_collected * 20

            if not self.planet_body.visited:
                self.planet_body.visited = True
                self.space_view.visited_planets += 1

            arcade.unschedule(self.spawn_alien)
            arcade.unschedule(self.spawn_resource)

    def spawn_alien(self, dt):
        alien = arcade.Sprite(self.alien_texture)
        alien.center_x = random.randrange(self.window.width)
        alien.bottom = self.window.height
        self.alien_list.append(alien)

    def spawn_resource(self, dt):
        res = arcade.Sprite(self.resource_texture)
        res.center_x = random.randrange(self.window.width)
        res.bottom = self.window.height
        self.resource_list.append(res)

    def on_key_press(self, key, modifiers):
        if (self.game_over or self.victory) and key == arcade.key.SPACE:
            self.space_view.ship.landed = False
            self.window.show_view(self.space_view)
            return

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5
        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(5, 15, color=arcade.color.WHITE)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            bullet.change_y = 10
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT): self.player_sprite.change_x = 0
