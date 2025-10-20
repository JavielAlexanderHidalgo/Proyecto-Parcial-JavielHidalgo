import pygame
from pygame.locals import *
import numpy as np
import random
import heapq

#Configuración de la ventana
WIDTH, HEIGHT = 1280, 720
columnas, filas = 16, 9
TILE_SIZE = min(WIDTH // columnas, HEIGHT // filas)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUEGO")

#Cargar sprites e imágenes básicas
pared = pygame.transform.scale(pygame.image.load('Images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
suelo = pygame.transform.scale(pygame.image.load('Images/ground2.jpg'), (TILE_SIZE, TILE_SIZE))
robot = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
robot_left = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
out1 = pygame.transform.scale(pygame.image.load('Images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
fin_bg = pygame.transform.scale(pygame.image.load('Images/FONDO1.jpg'), (WIDTH, HEIGHT))
enemy_image = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
lose_bg = pygame.transform.scale(pygame.image.load('Images/lose_screen.png'), (WIDTH, HEIGHT))
sword_right_image = pygame.transform.scale(pygame.image.load('Images/sword_right.png'),
                                           (TILE_SIZE // 2, TILE_SIZE // 2))
sword_left_image = pygame.transform.scale(pygame.image.load('Images/sword_left.png'), (TILE_SIZE // 2, TILE_SIZE // 2))
sword_up_image = pygame.transform.scale(pygame.image.load('Images/sword_up.png'), (TILE_SIZE // 2, TILE_SIZE // 2))
sword_down_image = pygame.transform.scale(pygame.image.load('Images/sword_down.png'), (TILE_SIZE // 2, TILE_SIZE // 2))

# Matriz del laberinto
mapa = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
])


Bucle principal
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Dibujar el mapa
        for y in range(filas):
            for x in range(columnas):
                if mapa[y][x] == 1:
                    screen.blit(pared, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    screen.blit(suelo, (x * TILE_SIZE, y * TILE_SIZE))

        # Dibujar jugador en posición inicial
        screen.blit(robot, (0, 0))
        screen.blit(out1, ((columnas - 1) * TILE_SIZE, (filas - 1) * TILE_SIZE))

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()


main()
