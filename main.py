#JAVIEL ALEXANDER HIDALGO
import pygame
from pygame.locals import *
import numpy as np
from assets.personaje import Personaje
from assets.enemigo import Enemigo
from assets.sword import Sword

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1280, 720
columnas, filas = 16, 9
TILE_SIZE = min(WIDTH // columnas, HEIGHT // filas)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PROYECTO PARCIAL JAVIEL ALEXANDER")

# Cargar imágenes del mapa
pared = pygame.transform.scale(pygame.image.load('assets/images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
suelo = pygame.transform.scale(pygame.image.load('assets/images/ground2.jpg'), (TILE_SIZE, TILE_SIZE))
fondo = pygame.transform.scale(pygame.image.load('assets/images/FONDO1.jpg'), (WIDTH, HEIGHT))

# Mapa del juego
mapa = np.array([
    [0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1],
    [1,1,1,0,1,1,0,0,0,0,1,1,1,1,0,1],
    [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,0,0,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0]
])


jugador = Personaje(100, 100)
enemigos = pygame.sprite.Group(
    Enemigo(500, 400, 'assets/images/ROBOT1.png'),
    Enemigo(800, 200, 'assets/images/ROBOT1.png')
)
espadas = pygame.sprite.Group()

clock = pygame.time.Clock()

# Bucle principal
def main():
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                jugador.atacar(espadas)

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas, mapa)


        espadas.update(enemigos, mapa)
        for enemigo in enemigos:
            enemigo.moverse_hacia(jugador.rect.center)

        # Dibujar todo
        screen.blit(fondo, (0, 0))
        for y in range(filas):
            for x in range(columnas):
                if mapa[y][x] == 1:
                    screen.blit(pared, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    screen.blit(suelo, (x * TILE_SIZE, y * TILE_SIZE))

        enemigos.draw(screen)
        espadas.draw(screen)
        screen.blit(jugador.image, jugador.rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
