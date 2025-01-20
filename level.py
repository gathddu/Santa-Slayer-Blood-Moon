import pygame
from setting import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from player import *
from weapon import *
from ui import *
from mob import *
from final import final_battle
from cutscene import *
from particles import *
from magic import *

class Level:
    # central do jogo inteiro
    def __init__ (self, clock):
        
        self.clock = clock
        # dava pra passar o screen como método de level mas.. melhor pegar o display surface de qualquer parte do código né?
        self.display_surface = pygame.display.get_surface()

        # sprite setup
        self.visible_sprites = YCameraGroup() # visible sprites são aqueles que vão ser desenhados
        self.obstacle_sprites = pygame.sprite.Group() # sprites que colidem com o player


        #attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        # interface
        self.ui = UI()

        #particle animation
        self.animation_player = AnimationPlayer()
        self.magic_player = Magic(self.animation_player)


    def create_map (self): # eu vou me matar
        layouts = {
           "boundary": import_csv_layout("./graphics/tilemap/csv/boundary.csv"),
           "detail": import_csv_layout("./graphics/tilemap/csv/detail.csv"),
           "entities": import_csv_layout("./graphics/tilemap/csv/entities.csv"),
           "larger": import_csv_layout("./graphics/tilemap/csv/larger.csv")
        }

        graphics = {
            "details": import_folder("./graphics/tilemap/details"),
            "largers": import_folder("./graphics/tilemap/details")
        }




        # quando a gente criar um tile, vai ter os visíveis e de obstáculo // collision

        for style, layout in layouts.items():

            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "detail":
                            surf = graphics["details"][int(col)]
                            Tile((x, y), [self.visible_sprites,self.obstacle_sprites], "detail", surf)

                        if style == "larger":
                            surf = graphics["largers"][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "larger", surf)


                        if style == "entities":
                            if col == "68":
                                self.player = Player (
                                (x,y), [self.visible_sprites],
                                self.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic)
                            else:
                                if col == "54":
                                    mob_name = "krampus"
                                    krampus = Mob(mob_name, (x, y), 
                                                [self.visible_sprites, self.attackable_sprites],
                                                self.obstacle_sprites, self.damage_player,
                                                self.trigger_death_particles, self.add_xp)
                                elif col == "84":
                                    mob_name = "snowman"
                                    Mob (mob_name, (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,self.damage_player,
                                        self.trigger_death_particles,self.add_xp)
                                elif col == "69":
                                    mob_name = "gingerbread"
                                    Mob (mob_name, (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,self.damage_player,
                                        self.trigger_death_particles,self.add_xp)
                                

            
        

    def create_attack (self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic (self, style, strength, cost):

        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "spirit":
            self.magic_player.spirit(self.player, cost, [self.visible_sprites, self.attack_sprites])


    def destroy_attack (self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # determina se caso o sprite colidir com o grupo, a gente pode matar
    def player_attack_logic (self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "mob":
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            if self.player.health < 0:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            #particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_xp (self, amount):

        self.player.xp += amount


    def run (self):

        # atualizando e rodando o jogo
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.mob_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
    

        #krampus radius
        #krampus battle trigger based on proximity
        krampus_sprite = next((sprite for sprite in self.visible_sprites if getattr(sprite, "mob_name", None) == "krampus"), None)
        if krampus_sprite:
            distance = pygame.math.Vector2(self.player.rect.center).distance_to(pygame.math.Vector2(krampus_sprite.rect.center))

            if distance < 270:  # trigger dialogue if player gets close
                final_battle(self.player, krampus_sprite, self.display_surface, self.clock, self.visible_sprites)

        if krampus_sprite is None:
            play_cutscene(self.display_surface, "krampus defeated")
            return

class YCameraGroup (pygame.sprite.Group): # esse grupo de sprite vai funcionar como uma câmera através das coordenadas y
    
    def __init__ (self):

        # setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # o truque foi conectar o offset no player

        # chão
        self.floor_surf = pygame.image.load("./graphics/tilemap/map.png").convert() # png do mapa, literalmente
        self.floor_rect = self.floor_surf.get_rect (topleft = (0, 0))

    def custom_draw(self, player):

        
        # PORRAAAAAAAA
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #desenhando chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)


        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit (sprite.image, offset_pos)

    def mob_update(self, player):
        mob_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "mob"]
        for mob in mob_sprites:
            mob.mob_update(player)