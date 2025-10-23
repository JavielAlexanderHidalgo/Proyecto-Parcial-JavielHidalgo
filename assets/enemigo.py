import pygame
import math

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, velocidad=2, vida_max=100):
        super().__init__()
        self.imagen_original = pygame.image.load(imagen).convert_alpha()
        self.image = pygame.transform.scale(self.imagen_original, (60, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad
        self.vida = vida_max
        self.vida_max = vida_max
        self.vivo = True

    def moverse_hacia(self, jugador_pos):
        if not self.vivo:
            return
        dx, dy = jugador_pos[0] - self.rect.x, jugador_pos[1] - self.rect.y
        distancia = math.hypot(dx, dy)
        if distancia > 0:
            dx, dy = dx / distancia, dy / distancia
            self.rect.x += dx * self.velocidad
            self.rect.y += dy * self.velocidad

    def recibir_daño(self, cantidad):
        if self.vivo:
            self.vida -= cantidad
            self.actualizar_color()
            if self.vida <= 0:
                self.vivo = False

    def actualizar_color(self):
        # Cambia progresivamente a rojo
        porcentaje = 1 - (self.vida / self.vida_max)
        nueva_imagen = self.imagen_original.copy()
        rojo = int(255 * porcentaje)
        superficie_tintada = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        superficie_tintada.fill((rojo, 0, 0, 100))
        nueva_imagen.blit(superficie_tintada, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = nueva_imagen

    def dibujar_barra_vida(self, pantalla):
        if not self.vivo:
            return
        ancho_barra = 60
        alto_barra = 6
        x = self.rect.centerx - ancho_barra // 2
        y = self.rect.top - 10
        vida_actual = int((self.vida / self.vida_max) * ancho_barra)
        pygame.draw.rect(pantalla, (255, 0, 0), (x, y, ancho_barra, alto_barra))
        pygame.draw.rect(pantalla, (0, 255, 0), (x, y, vida_actual, alto_barra))
