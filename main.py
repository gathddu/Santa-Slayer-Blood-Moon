import pygame
import sys
from setting import *
from level import *
from player import *
from menu import mostrar_configuracoes

# playlist pra programar bem:
# i'm with you // avril lavigne
# amoeba // clairo
# drive // incubus
# peach // kevin abstract

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SANTA SLAYER: BLOOD MOON")
        self.clock = pygame.time.Clock()
        self.level = Level(self.clock)

        # Inicializar música para o menu
        pygame.mixer.music.load("./audio/Santa_Baby.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def run(self):
        # Música do jogo
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./audio/Santa_Baby.mp3")
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Abrir menu ao pressionar ESC
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mostrar_configuracoes()  # Exibe o menu de configurações

            # Atualizar tela do jogo
            self.screen.fill("grey")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
