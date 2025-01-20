import pygame
from setting import *
from entity import Entity
from support import *
from player import *

class Mob (Entity):
    def __init__ (self, mob_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp): #feijoada de PUTAAAAA

        #setup
        super().__init__(groups)
        self.sprite_type = "mob"

        #graphics
        self.import_graphics(mob_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # mov
        self.rect = self.image.get_rect (topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        #stats nessa buceta então já que não tem speed // biblioteca em atributos
        self.mob_name = mob_name
        mob_info = mob_data [self.mob_name]
        self.health  = mob_info ["health"]
        self.xp = mob_info["xp"]
        self.sp = mob_info ["speed"]
        self.attack_damage = mob_info ["damage"]
        self.resistance = mob_info ["resistance"]
        self.attack_radius = mob_info ["attack_radius"]
        self.notice_radius= mob_info ["notice_radius"]
        self.attack_type = mob_info ["attack_type"]

        #interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 500
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_xp = add_xp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


    def import_graphics (self, name):
        self.animations = {"idle":[], "move":[], "attack":[]}
        main_path = f"./graphics/mob/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            
    def get_player_distance_direction (self, player):

        #odeio vetor
        mob_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2 (player.rect.center)
        distance = (player_vec - mob_vec).magnitude()

        if distance > 0:
            direction = (player_vec - mob_vec).normalize()

        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status (self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"

        else:
            self.status = "idle"    

    def action(self, player):
        if self.status == "attack" and self.can_attack:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1] #1 = índice direção
        else:
            self.direction = pygame.math.Vector2() # se o player sair do raio, ele para

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_sp
        if self.frame_index >= len(animation):

            if self.status == "attack":
                self.can_attack = False #o player só para de poder atacar depois da animação
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            #flick
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255) #set alpha é a transparência da camada, 255 é o valor cheio então se ele não tá vulnerável, ele fica normal

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True


    def get_damage(self,player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage() #magic
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
                self.kill()
                self.trigger_death_particles(self.rect.center, self.mob_name)
                self.add_xp(self.xp)
                

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):

        self.hit_reaction()
        self.move(self.sp)
        self.animate()
        self.cooldown()
        self.check_death()

    def mob_update (self, player):
        self.get_status(player)
        self.action(player)
        