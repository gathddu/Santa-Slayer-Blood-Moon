import pygame
from math import sin

class Entity (pygame.sprite.Sprite):
    def __init__ (self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_sp = 0.5
        self.direction = pygame.math.Vector2() # x e y
    
    def move (self, sp):
        # então, tive que fazer uns ajustes
        # quando o player movia diagonalmente, a velocidade aumentava, então normalizei a direção
        # basicamente mudando o tamanho do vetor pra 1 
        if self.direction.magnitude()  != 0: # um vetor de 0 não pode ser normalizado
            self.direction = self.direction.normalize()
            # não importa mais qual direção o jogador move, o tamanho do vetor sempre vai ser 1
        self.hitbox.x += self.direction.x * sp
        self.collision ("horizontal")
        self.hitbox.y += self.direction.y * sp
        self.collision ("vertical")
        self.rect.center = self.hitbox.center
        

    def collision (self, direction):
        
        if direction == "horizontal":

            for sprite in self.obstacle_sprites:

                if sprite.hitbox.colliderect(self.hitbox):

                    if self.direction.x > 0: # move pra direita
                        self.hitbox.right = sprite.hitbox.left
                    
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            
            for sprite in self.obstacle_sprites:

                if sprite.hitbox.colliderect (self.hitbox):

                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):

        #a gente tem um gráfico, e uma senoide. a gente pode checar cada ponto da onda com o tempo. se a curva for positiva o retorno é 255 e se for negativo, vai ser 0

        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0