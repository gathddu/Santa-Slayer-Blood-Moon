import pygame

# a gente vai desenhar a arma na margem do personagem

class Weapon (pygame.sprite.Sprite):

    def __init__ (self, player, groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]

        #graphics
        full_path = f"./graphics/weapon/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        #posicionamento
        if direction == "right":

            self.rect = self.image.get_rect (midleft = player.rect.midright + pygame.math.Vector2 (0,9))

        elif direction == "left":
            self.rect = self.image.get_rect (midright = player.rect.midleft + pygame.math.Vector2 (0, 9))
        
        elif direction == "down":
            self.rect = self.image.get_rect (midtop = player.rect.midbottom + pygame.math.Vector2 (10, 0))

        else:
            self.rect = self.image.get_rect (midbottom = player.rect.midtop + pygame.math.Vector2 (-15,0))