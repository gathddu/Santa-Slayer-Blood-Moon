import pygame
from setting import *

def play_cutscene(screen, outcome):
    #cutscene baseado no outcome
    screen.fill("black")
    font = pygame.font.Font(UI_FONT, 20)

    if outcome == "krampus defeated":
        text = "KRAMPUS has been defeated! peace returns to the land."
    elif outcome == "player defeated":
        text = "you were defeated, weakling.. KRAMPUS reigns supreme."
    else:
        text = "unknown outcome."

    text_surface = font.render(text, True, TEXT_COLOUR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(5000)  # 5 seconds before exiting
