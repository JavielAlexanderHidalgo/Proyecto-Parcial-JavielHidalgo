#JAVIEL ALEXANDER HIDALGO 21-EISN-2-019
import pygame
import numpy as np
import random
from enemigo import Enemy
from personaje import Player
from espada import sword

# Configuración
WIDTH, HEIGHT = 1280, 720
columnas, filas = 16, 9
TILE_SIZE = min(WIDTH // columnas, HEIGHT // filas)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUEGO MODULAR")

#Cargar imágenes
pared = pygame.transform.scale(pygame.image.load('Images/pared2.jpg'), (TILE_SIZE, TILE_SIZE))
suelo = pygame.transform.scale(pygame.image.load('Images/ground2.jpg'), (TILE_SIZE, TILE_SIZE))
robot = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
robot_left = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))
enemy_image = pygame.transform.scale(pygame.image.load('Images/ROBOT1.png'), (TILE_SIZE, TILE_SIZE))

sword_images = {
    'derecha': pygame.transform.scale(pygame.image.load('Images/sword_right.png'), (TILE_SIZE//2, TILE_SIZE//2)),
    'izquierda': pygame.transform.scale(pygame.image.load('Images/sword_left.png'), (TILE_SIZE//2, TILE_SIZE//2)),
    'arriba': pygame.transform.scale(pygame.image.load('Images/sword_up.png'), (TILE_SIZE//2, TILE_SIZE//2)),
    'abajo': pygame.transform.scale(pygame.image.load('Images/sword_down.png'), (TILE_SIZE//2, TILE_SIZE//2)),
}

#  Mapa
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

# Crear jugador
player = Personaje(0, 0, robot, robot_left)

#  Función para crear enemigos
def crear_enemigos(cantidad):
    enemies = pygame.sprite.Group()
    posiciones_ocupadas = [(0,0),(columnas-1,filas-1)]
    for _ in range(cantidad):
        while True:
            x, y = random.randint(0,columnas-1), random.randint(0,filas-1)
            if mapa[y][x] == 0 and (x,y) not in posiciones_ocupadas:
                enemies.add(Enemy(x, y, enemy_image, columnas, filas))
                posiciones_ocupadas.append((x,y))
                break
    return enemies

#Función principal
def main():
    pygame.init()
    running = True
    fin = False
    perdio = False

    enemies = crear_enemigos(5)
    swords = pygame.sprite.Group()

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if not fin and not perdio:
                    if event.key == K_LEFT and player.x > 0 and mapa[player.y][player.x-1]==0:
                        player.direccion = 'izquierda'
                        player.mover(-1,0)
                    elif event.key == K_RIGHT and player.x < columnas-1 and mapa[player.y][player.x+1]==0:
                        player.direccion = 'derecha'
                        player.mover(1,0)
                    elif event.key == K_UP and player.y > 0 and mapa[player.y-1][player.x]==0:
                        player.direccion = 'arriba'
                        player.mover(0,-1)
                    elif event.key == K_DOWN and player.y < filas-1 and mapa[player.y+1][player.x]==0:
                        player.direccion = 'abajo'
                        player.mover(0,1)
                    elif event.key == K_SPACE:
                        sword = Sword(player.x*TILE_SIZE + TILE_SIZE//2, player.y*TILE_SIZE + TILE_SIZE//2, player.direccion, sword_images)
                        swords.add(sword)
                if fin or perdio:
                    if event.key == K_RETURN:
                        player.x, player.y = 0, 0
                        player.direccion = 'derecha'
                        enemies = crear_enemigos(5)
                        swords.empty()
                        fin = False
                        perdio = False

        # Dibujar mapa
        for y in range(filas):
            for x in range(columnas):
                screen.blit(pared if mapa[y][x]==1 else suelo, (x*TILE_SIZE, y*TILE_SIZE))

        # Dibujar jugador
        screen.blit(player.get_imagen(), (player.x*TILE_SIZE, player.y*TILE_SIZE))

        # Actualizar enemigos
        if not fin and not perdio:
            for enemy in enemies:
                enemy.update((player.x, player.y), mapa)
            enemies.draw(screen)

        # Verificar colisión con enemigos
        for enemy in enemies:
            if enemy.rect.colliderect(pygame.Rect(player.x*TILE_SIZE, player.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)):
                perdio = True

        # Actualizar y dibujar espadas
        swords.update(enemies, mapa, TILE_SIZE, columnas, filas)
        swords.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

#  Ejecutar
if __name__ == "__main__":
    main()
