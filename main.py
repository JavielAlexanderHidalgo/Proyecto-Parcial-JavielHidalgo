import pygame
from pygame.locals import *
import numpy as np
import random
from sword import Sword
from enemy import Enemy

# Configuración de la ventana
WIDTH, HEIGHT = 1280, 720
columnas, filas = 16, 9
TILE_SIZE = min(WIDTH // columnas, HEIGHT // filas)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUEGO")

# Cargar imágenes del juego
pared = pygame.transform.scale(pygame.image.load('Images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
suelo = pygame.transform.scale(pygame.image.load('Images/ground2.jpg'), (TILE_SIZE, TILE_SIZE))
robot = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
robot_left = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
out1 = pygame.transform.scale(pygame.image.load('Images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
fin_bg = pygame.transform.scale(pygame.image.load('Images/FONDO1.jpg'), (WIDTH, HEIGHT))
lose_bg = pygame.transform.scale(pygame.image.load('Images/lose_screen.png'), (WIDTH, HEIGHT))

# Imágenes de las espadas
sword_right_image = pygame.transform.scale(pygame.image.load('Images/sword_right.png'), (TILE_SIZE//2, TILE_SIZE//2))
sword_left_image = pygame.transform.scale(pygame.image.load('Images/sword_left.png'), (TILE_SIZE//2, TILE_SIZE//2))
sword_up_image = pygame.transform.scale(pygame.image.load('Images/sword_up.png'), (TILE_SIZE//2, TILE_SIZE//2))
sword_down_image = pygame.transform.scale(pygame.image.load('Images/sword_down.png'), (TILE_SIZE//2, TILE_SIZE//2))

# Laberinto del juego
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

# Crear enemigos en posiciones aleatorias
def crear_enemigos(cantidad):
    enemies = pygame.sprite.Group()
    posiciones_ocupadas = [(0,0),(columnas-1,filas-1)]  # evitar jugador y salida
    for _ in range(cantidad):
        while True:
            x, y = random.randint(0, columnas-1), random.randint(0, filas-1)
            if mapa[y][x] == 0 and (x,y) not in posiciones_ocupadas:
                enemy = Enemy(x, y)
                enemies.add(enemy)
                posiciones_ocupadas.append((x,y))
                break
    return enemies

# Reiniciar el juego
def reset_game(enemies):
    global pos_x, pos_y, direccion, fin, perdio
    pos_x, pos_y = 0,0
    direccion = 'derecha'
    fin = False
    perdio = False
    enemies.empty()
    return crear_enemigos(5)

# Función principal
def main():
    global pos_x, pos_y, direccion, fin, perdio
    pygame.init()
    running = True
    pos_x, pos_y = 0, 0
    direccion = 'derecha'
    fin = False
    perdio = False

    enemies = crear_enemigos(5)
    swords = pygame.sprite.Group()

    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # Movimiento del jugador
                if not fin and not perdio:
                    if event.key == K_LEFT and pos_x > 0 and mapa[pos_y][pos_x-1]==0:
                        direccion = 'izquierda'
                        pos_x -= 1
                    elif event.key == K_RIGHT and pos_x < columnas-1 and mapa[pos_y][pos_x+1]==0:
                        direccion = 'derecha'
                        pos_x += 1
                    elif event.key == K_UP and pos_y > 0 and mapa[pos_y-1][pos_x]==0:
                        direccion = 'arriba'
                        pos_y -= 1
                    elif event.key == K_DOWN and pos_y < filas-1 and mapa[pos_y+1][pos_x]==0:
                        direccion = 'abajo'
                        pos_y += 1
                    elif event.key == K_SPACE:  # disparar espada
                        sword = Sword(pos_x*TILE_SIZE+TILE_SIZE//2,pos_y*TILE_SIZE+TILE_SIZE//2,direccion)
                        swords.add(sword)
                # Reiniciar juego
                if fin or perdio:
                    if event.key == K_RETURN:
                        enemies = reset_game(enemies)
                        swords.empty()

        # Dibujar el laberinto
        for y in range(filas):
            for x in range(columnas):
                if mapa[y][x]==1:
                    screen.blit(pared,(x*TILE_SIZE,y*TILE_SIZE))
                else:
                    screen.blit(suelo,(x*TILE_SIZE,y*TILE_SIZE))

        # Dibujar jugador y salida
        screen.blit(robot if direccion=='derecha' else robot_left,(pos_x*TILE_SIZE,pos_y*TILE_SIZE))
        screen.blit(out1,((columnas-1)*TILE_SIZE,(filas-1)*TILE_SIZE))

        # Comprobar victoria
        if (pos_x,pos_y)==(columnas-1,filas-1):
            screen.blit(fin_bg,(0,0))
            fin = True

        # Actualizar y dibujar enemigos
        if not fin and not perdio:
            for enemy in enemies:
                enemy.update((pos_x,pos_y), mapa)
            enemies.draw(screen)

        # Colisión con enemigos
        for enemy in enemies:
            if enemy.rect.colliderect(pygame.Rect(pos_x*TILE_SIZE,pos_y*TILE_SIZE,TILE_SIZE,TILE_SIZE)):
                screen.blit(lose_bg,(0,0))
                perdio = True

        # Actualizar espadas
        swords.update(enemies,mapa)
        swords.draw(screen)

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()
