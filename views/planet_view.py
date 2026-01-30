# views/planet_view.py
import arcade
import random

from sprites.astronaut import Astronaut
from sprites.alien import Alien
from sprites.weapon import WeaponPickup


class PlanetView(arcade.View):
    def __init__(self, space_view):
        super().__init__()
        self.space_view = space_view

        self.player = Astronaut(0, 0)
        self.aliens = arcade.SpriteList()
        self.pickups = arcade.SpriteList()

        self.score = space_view.ship.score

        # спавн инопланетян
        for _ in range(8):
            self.aliens.append(
                Alien(
                    random.randint(-500, 500),
                    random.randint(-300, 300)
                )
            )

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BROWN)

    # ---------- INPUT ----------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        if key == arcade.key.S:
            self.player.change_y = -self.player.speed
        if key == arcade.key.A:
            self.player.change_x = -self.player.speed
        if key == arcade.key.D:
            self.player.change_x = self.player.speed

        # атака (ближняя)
        if key == arcade.key.F:
            for alien in arcade.check_for_collision_with_list(
                self.player, self.aliens
            ):
                alien.health -= 40
                if alien.health <= 0:
                    alien.remove_from_sprite_lists()
                    self.score += 1

                    if random.random() < 0.5:
                        self.pickups.append(
                            WeaponPickup(
                                alien.center_x,
                                alien.center_y
                            )
                        )

        # возврат в корабль
        if key == arcade.key.SPACE:
            self.space_view.ship.score = self.score
            self.window.show_view(self.space_view)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    # ---------- UPDATE ----------
    def on_update(self, dt):
        self.player.update(dt)

        for alien in self.aliens:
            alien.update(dt)

        for pickup in self.pickups:
            if arcade.check_for_collision(self.player, pickup):
                pickup.remove_from_sprite_lists()
                self.score += 2

    # ---------- DRAW ----------
    def on_draw(self):
        self.clear()

        self.aliens.draw()
        self.pickups.draw()
        self.player.draw()

        arcade.draw_text(
            f"Score: {self.score}",
            10, self.window.height - 30,
            arcade.color.WHITE, 16
        )

        arcade.draw_text(
            "WASD — движение | F — атака | SPACE — к кораблю",
            10, 10,
            arcade.color.LIGHT_GRAY, 12
        )