import pygame
from setting import *
from support import *
from entity import *


class Player (Entity):


    def __init__ (self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/player/down_idle/idle_down.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -16)

        #graphic setup
        self.import_player_asset ()
        self.status = "down"

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None # criar timer
        self.obstacle_sprites = obstacle_sprites

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None



        #stat
        self.stats = {"health": 100, "energy": 50, "attack": 10, "magic": 5, "speed": 8}
        self.max_stats = {"health": 300, "energy": 150, "attack": 30, "magic": 15, "speed": 10}
        self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.xp = 0
        self.sp = self.stats["speed"]

        #damage timer ugh
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_asset (self):
        character_path = "./graphics/player/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
                           "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []}
        
        for animation in self.animations.keys ():
            full_path = character_path + animation
            self.animations [animation] = import_folder (full_path)

    def input (self):

        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1 
                self.status = "down"
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

        #attack
            if keys [pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks ()
                self.create_attack () #problema de blit // não ataca mais de +1

        #magic
            if keys [pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic (style, strength, cost)

            if keys [pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1: #resolvido.
                    self.magic_index += 1 # só tem 3 AARGGGHHHHH
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]
        

            if keys [pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1: #resolvido.
                    self.weapon_index += 1 # só tem 3 AARGGGHHHHH
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status (self):
        
        #idle
        if self.direction.x ==  0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    #overwrite idle
                    self.status = self.status.replace ("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace ("_attack", "")

    def cooldown (self):
        current_time = pygame.time.get_ticks () # if só roda uma vez mas o get ticks faz rodar infinitamente

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking  = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate (self):
        animation = self.animations [self.status]

        #loop do frame index
        self.frame_index += self.animation_sp
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # image
        self.image = animation [int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flick
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def update (self):
        
        self.input()
        self.cooldown()
        self.get_status()
        self.animate ()
        self.move(self.sp)
        self.energy_recovery()