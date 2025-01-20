import pygame
from support import *


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            
            #magic
            "spirit": import_folder("./graphics/magic/spirit/frames"),
            "heal": import_folder("./graphics/magic/heal/frames"),
            "aura": import_folder("./graphics/magic/aura"),


            #attacks
            "snow": import_folder("./graphics/magic/snow"),
            "cane": import_folder("./graphics/magic/cane"),
            "grinch": import_folder("./graphics/magic/grinch"),
            "sparkle": import_folder("./graphics/magic/sparkle"),

            #mob death
            "snowman": import_folder("./graphics/magic/smoke_orange"),
            "gingerbread": import_folder("./graphics/magic/raccoon"),
            "krampus": import_folder("./graphics/magic/nova")

        }
    


    def create_particles(self,animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__ (self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_sp = 0.5
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    

    def animate(self):
        self.frame_index += self.animation_sp

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()