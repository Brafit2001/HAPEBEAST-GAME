from random import randint
import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

END_GAME = 0


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hapebeast Game")
        pyxel.load("jump_game.pyxres")
        self.score = 0
        self.player_x = 72
        self.player_y = -16
        self.player_dy = 0
        self.is_alive = True
        self.lives = 2
        self.scene = SCENE_TITLE
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.fruit = [(i * 60, randint(0, 104), randint(0, 2), True) for i in range(6)]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_P):
            pyxel.stop(0)

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_player()
            for i, v in enumerate(self.floor):
                self.floor[i] = self.update_floor(*v)
            for i, v in enumerate(self.fruit):
                self.fruit[i] = self.update_fruit(*v)
        elif self.scene == SCENE_GAMEOVER:
            self.update_game_over_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_game_over_scene(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.score = 0
            self.scene = SCENE_PLAY
            self.lives = 2
            self.player_x = 72
            self.player_y = -16
            self.player_dy = 0
            pyxel.load("jump_game.pyxres")
            pyxel.playm(0, loop=True)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + 1, 8)

        if self.player_y > pyxel.height:
            if self.is_alive:
                self.is_alive = False

                if self.lives == END_GAME:
                    print(self.lives)
                    print(END_GAME)
                    self.scene = SCENE_GAMEOVER
                else:
                    self.lives -= 1
                pyxel.play(3, 5)
            if self.player_y > 600:
                self.player_x = 72
                self.player_y = -16
                self.player_dy = 0
                self.is_alive = True

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        x -= 2
        if x < -40:
            x += 240
            y = randint(8, 104)
            is_alive = True
        return x, y, is_alive

    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score += (kind + 1) * 100
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(3, 4)
        x -= 2
        if x < -40:
            x += 240
            y = randint(0, 104)
            kind = randint(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)

    def draw(self):
        pyxel.cls(11)
        pyxel.load("test_resource.pyxres")

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            pyxel.load("jump_game.pyxres")
            pyxel.cls(12)
            # Draw sky
            pyxel.blt(0, 88, 0, 0, 88, 160, 32)

            # Draw mountain
            pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

            # Draw trees
            offset = pyxel.frame_count % 160
            for i in range(2):
                pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

            # Draw clouds
            offset = (pyxel.frame_count // 16) % 160
            for i in range(2):
                for x, y in self.far_cloud:
                    pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
            offset = (pyxel.frame_count // 8) % 160
            for i in range(2):
                for x, y in self.near_cloud:
                    pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

            # Draw floors
            for x, y, is_alive in self.floor:

                pyxel.blt(x, y, 0,
                          0, 16,  # x, y en el banco
                          40, 8,  # ancho y alto
                          12)  #

            # Draw fruits
            for x, y, kind, is_alive in self.fruit:
                if is_alive:
                    pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

            # Draw player
            pyxel.blt(
                self.player_x,
                self.player_y,
                0,
                16 if self.player_dy > 0 else 0,
                0,
                16,
                16,
                12,
            )

            # Draw score
            s = f"SCORE {self.score:>4}"
            pyxel.text(5, 4, s, 1)
            pyxel.text(4, 4, s, 7)
        elif self.scene == SCENE_GAMEOVER:
            self.draw_game_over_scene()
    def draw_title_scene(self):

        altura_profile = 80
        # brafit
        pyxel.circ(30, altura_profile, 23, 6)
        pyxel.blt(15, altura_profile-17, 0,
                  0, 126,
                  35, 34,
                  colkey=0)
        pyxel.text(22, altura_profile + 27, "Brafit", 0)

        # Augusto
        pyxel.load("monos.pyxres")
        pyxel.circ(80, altura_profile, 23, 8)
        pyxel.blt(65, altura_profile-17, 1,
                  0, 0,
                  35, 34,
                  colkey=0)
        pyxel.text(72, altura_profile + 27, "Augusto", 0)
        #Mauricio

        pyxel.circ(130, altura_profile, 23, 10)
        pyxel.blt(115, altura_profile-17, 0,
                  0, 0,
                  35, 34,
                  colkey=0)
        pyxel.text(122, altura_profile + 27, "Mauricio", 0)


        pyxel.text(55, 15, "HAPEBEAST GAME", 8)
        pyxel.text(54, 28, "- PRESS ENTER -", pyxel.frame_count % 16)
        pyxel.text(54, 47, "Game Created By:", 0)
        pyxel.text(0,0, "Press P to stop de music", 0)

    def draw_game_over_scene(self):
        pyxel.cls(2)
        #  MONO FINAL
        pyxel.load("monos_bg.pyxres")
        pyxel.circ(80, 85, 60, 7)
        pyxel.blt(50, 30, 2,
                  0, 0,
                  100, 112, colkey=0)

        pyxel.text(55,5, "GAME OVER", 10)
        s = f"SCORE {self.score:>4}"
        pyxel.text(0, 0, s, 0)
        pyxel.text(10, 15, "Thanks For playing HapeBeast Game", 10)
        pyxel.stop(0)

        #  RECTANGULO IZQ
        pyxel.rect(0,92,50,30,7)
        pyxel.rectb(0,92,50,28,10)
        pyxel.text(4, 95, "Visit", 0)
        pyxel.text(4, 105, "hapebeast", 0)
        pyxel.text(4, 112, ".com", 8)

        #  RECTANGULO DER
        pyxel.rect(114, 96, 50, 33, 7)
        pyxel.rectb(114, 96, 46, 24, 10)
        pyxel.text(117, 100, "Press R", 0)
        pyxel.text(117, 110, "to restart", 0)

App()
# BRAFIT, AUGUSTO AND MAURICIO
