#JAVIEL ALEXANDER HIDALGO
# Esta es mi clase Personaje
import pygame
from sword import Sword

class Player:
    def __init__(self, x, y, images, tile_size):
        self.x = x
        self.y = y
        self.images = images
        self.tile_size = tile_size
        self.direccion = 'derecha'

    def mover(self, dx, dy, mapa):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < len(mapa[0]) and 0 <= ny < len(mapa) and mapa[ny][nx]==0:
            self.x, self.y = nx, ny

    def atacar(self, swords_group, sword_images):
        sword = Sword(self.x*self.tile_size+self.tile_size//2,
                      self.y*self.tile_size+self.tile_size//2,
                      self.direccion, sword_images, self.tile_size)
        swords_group.add(sword)

    def dibujar(self, screen):
        img = self.images['derecha'] if self.direccion=='derecha' else self.images['izquierda']
        screen.blit(img, (self.x*self.tile_size, self.y*self.tile_size))
