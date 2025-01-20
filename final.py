import pygame
from setting import *
from dialogue import *
from cutscene import play_cutscene

# Global variable to track dialogue state
dialogue_triggered = False
defeat_sequence_started = False

def final_battle(player, krampus, screen, clock, visible_sprites):
    global dialogue_triggered

    # Skip dialogue if already shown
    if dialogue_triggered:
        return

    pygame.event.clear()
    clock.tick(0)

    fade_to_black(screen, clock)

    # Pre-battle dialogue
    fight_dialogue = [
        "KRAMPUS: IT IS I. KRAMPUS.",
        "KRAMPUS: ...",
        "KRAMPUS: i wasn’t always like this..",
        "KRAMPUS: budget cuts and tight deadlines \nhave reduced me to a raindrop :(",
        "KRAMPUS: ANYWAYS!",
        "KRAMPUS: you dare challenge me on this blood moon..?",
        "KRAMPUS: look around, your holiday is ash!",
        "KRAMPUS: this isn't your fight anymore. it's mine to finish."
    ]
    display_dialogue(screen, fight_dialogue)

    fade_from_black(screen, clock)

    dialogue_triggered = True


def handle_krampus_defeat(screen, clock):
    global defeat_sequence_started

    if defeat_sequence_started:
        return

    defeat_sequence_started = True

    fade_to_black(screen, clock)

    # Victory dialogue and player choice
    victory_dialogue = [
        "KRAMPUS: You have defeated me...",
        "KRAMPUS: But tell me, hero...",
        "KRAMPUS: Are you satisfied with this outcome?"
    ]
    display_dialogue(screen, victory_dialogue)

    # Present player choices
    player_choice = present_choices(
        screen, clock,
        ["* Hell yeah, this game is amazeballs!", "* Nah, this is trash."]
    )

    fade_from_black(screen, clock)

    # Handle player choice outcome
    if player_choice == 0:
        play_cutscene(screen, "happy_ending")
    elif player_choice == 1:
        play_cutscene(screen, "salty_ending")

def fade_to_black(screen, clock, duration=1000):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def fade_from_black(screen, clock, duration=1000):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(255, 0, -5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def present_choices(screen, clock, options):
    """Presents the player with a list of choices and waits for input."""
    font = pygame.font.Font(UI_FONT, 20)

    while True:
        screen.fill("black")

        # Render options
        for i, option in enumerate(options):
            text_surface = font.render(option, True, TEXT_COLOUR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 0
                elif event.key == pygame.K_DOWN:
                    return 1
