#JAVIEL ALEXANDER HIDALGO
# Esta mi clase personaje
import pygame

class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, velocidad=5):
        super().__init__()
        self.frames = [pygame.image.load(f).convert_alpha() for f in frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = velocidad
        self.direccion = 'derecha'
        self.animacion_contador = 0

    def mover(self, keys, mapa, columnas, filas, TILE_SIZE):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] and self.rect.x > 0 and mapa[self.rect.y // TILE_SIZE][(self.rect.x - self.velocidad) // TILE_SIZE] == 0:
            dx = -self.velocidad
            self.direccion = 'izquierda'
        elif keys[pygame.K_RIGHT] and self.rect.x // TILE_SIZE < columnas - 1 and mapa[self.rect.y // TILE_SIZE][(self.rect.x + self.velocidad) // TILE_SIZE] == 0:
            dx = self.velocidad
            self.direccion = 'derecha'
        elif keys[pygame.K_UP] and self.rect.y > 0 and mapa[(self.rect.y - self.velocidad) // TILE_SIZE][self.rect.x // TILE_SIZE] == 0:
            dy = -self.velocidad
            self.direccion = 'arriba'
        elif keys[pygame.K_DOWN] and self.rect.y // TILE_SIZE < filas - 1 and mapa[(self.rect.y + self.velocidad) // TILE_SIZE][self.rect.x // TILE_SIZE] == 0:
            dy = self.velocidad
            self.direccion = 'abajo'

        self.rect.x += dx
        self.rect.y += dy

    def animar(self):
        self.animacion_contador += 1
        if self.animacion_contador >= 5:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animacion_contador = 0

    def disparar(self, swords_group):
        from sword import Sword
        espada = Sword(self.rect.centerx, self.rect.centery, self.direccion)
        swords_group.add(espada)

