import pygame
WIDTH = 640
HEIGHT = 480
FPS = 60
TILESIZE = 32

#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "./graphics/font/font.ttf"
UI_FONT_SIZE = 15

#general colours
WATER_COLOUR = "#70BDC9"
UI_BG_COLOUR = "#000000"
UI_BORDER_COLOUR = "#222222"
TEXT_COLOUR = "#E2D9D9"

# UI colours
HEALTH_COLOUR = "red"
ENERGY_COLOUR = "blue"
UI_BORDER_COLOUR_ACTIVE = "#C88A17"

weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphics": "./graphics/weapon/sword/full.png"},
    "axe": {"cooldown": 400, "damage": 30, "graphics": "./graphics/weapon/axe/full.png"},
    "lance": {"cooldown": 300, "damage": 20, "graphics": "./graphics/weapon/lance/full.png"}
}

#magic
magic_data = {
    "spirit": {"strength": 10, "cost": 20, "graphics": "./graphics/magic/spirit/spirit.png"},
    "heal": {"strength": 5, "cost": 10, "graphics": "./graphics/magic/heal/heal.png"}
}

#mob
mob_data ={
    "snowman": {"health": 50, "xp": 13, "damage": 15, "attack_type": "snow", "attack_sound": "./audio/attack/", "speed": 3, "resistance": 10, "attack_radius": 70, "notice_radius": 200},
    "gingerbread": {"health": 30, "xp": 13, "damage": 10, "attack_type": "cane", "attack_sound": "", "speed": 2, "resistance": 8, "attack_radius": 100, "notice_radius": 200},
    "krampus": {"health": 200, "xp": 55, "damage": 30, "attack_type": "grinch", "attack_sound": "", "speed": 3, "resistance": 30, "attack_radius": 200, "notice_radius": 300}
}
