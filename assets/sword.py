#JAVIEL ALEXANDER HIDALGO
# Clase para la espada
import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, sword_images, tile_size):
        super().__init__()
        self.direction = direction
        self.tile_size = tile_size
        if direction == 'derecha':
            self.image = sword_images['derecha']
        elif direction == 'izquierda':
            self.image = sword_images['izquierda']
        elif direction == 'arriba':
            self.image = sword_images['arriba']
        elif direction == 'abajo':
            self.image = sword_images['abajo']

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = tile_size // 1.5

    def update(self, enemies, mapa):
        new_x, new_y = self.rect.x, self.rect.y
        if self.direction == 'derecha':
            new_x += self.speed
        elif self.direction == 'izquierda':
            new_x -= self.speed
        elif self.direction == 'arriba':
            new_y -= self.speed
        elif self.direction == 'abajo':
            new_y += self.speed

        tile_x = new_x // self.tile_size
        tile_y = new_y // self.tile_size

        if 0<=tile_x<len(mapa[0]) and 0<=tile_y<len(mapa):
            if mapa[tile_y][tile_x]==1:
                self.kill()
                return
            self.rect.topleft = (new_x,new_y)

            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.kill()
                    self.kill()
                    break
