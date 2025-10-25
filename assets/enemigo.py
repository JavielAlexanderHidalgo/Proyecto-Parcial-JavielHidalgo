#JAVIEL ALEXANDER HIDALGO
#ESTA ES MI CLASE ENEMIGO
import pygame
import math
import pygame
import heapq
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, columnas, filas, tile_size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x*tile_size, y*tile_size))
        self.path = []
        self.state = "patrullar"
        self.patrulla_direccion = random.choice([(0,1),(1,0),(0,-1),(-1,0)])
        self.columnas = columnas
        self.filas = filas
        self.tile_size = tile_size

    def update(self, player_pos, mapa):
        distancia = abs(player_pos[0] - self.rect.x // self.tile_size) + abs(player_pos[1] - self.rect.y // self.tile_size)
        if distancia < 3:
            self.state = "atacar"
        elif distancia < 6:
            self.state = "perseguir"
        else:
            self.state = "patrullar"

        if self.state == "patrullar":
            new_pos = (self.rect.x + self.patrulla_direccion[0]*self.tile_size,
                       self.rect.y + self.patrulla_direccion[1]*self.tile_size)
            tile_x, tile_y = new_pos[0]//self.tile_size, new_pos[1]//self.tile_size
            if 0<=tile_x<self.columnas and 0<=tile_y<self.filas and mapa[tile_y][tile_x]==0:
                self.rect.topleft = new_pos
            else:
                self.patrulla_direccion = random.choice([(0,1),(1,0),(0,-1),(-1,0)])

        elif self.state == "perseguir":
            if not self.path or (self.rect.x//self.tile_size,self.rect.y//self.tile_size)!=player_pos:
                self.path = self.a_star((self.rect.x//self.tile_size,self.rect.y//self.tile_size), player_pos, mapa)
            if self.path:
                next_cell = self.path.pop(0)
                self.rect.topleft = (next_cell[0]*self.tile_size,next_cell[1]*self.tile_size)
        elif self.state == "atacar":
            pass

    #Funciones A*
    def a_star(self, start, goal, mapa):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        rows, cols = len(mapa), len(mapa[0])
        open_set = []
        heapq.heappush(open_set,(0,start))
        came_from = {}
        g_score = {start:0}
        f_score = {start:self.heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current==goal:
                return self.reconstruct_path(came_from,current)

            for d in directions:
                neighbor = (current[0]+d[0], current[1]+d[1])
                if 0<=neighbor[0]<cols and 0<=neighbor[1]<rows and mapa[neighbor[1]][neighbor[0]]==0:
                    tentative_g = g_score[current]+1
                    if neighbor not in g_score or tentative_g<g_score[neighbor]:
                        came_from[neighbor]=current
                        g_score[neighbor]=tentative_g
                        f_score[neighbor]=tentative_g+self.heuristic(neighbor, goal)
                        heapq.heappush(open_set,(f_score[neighbor],neighbor))
        return []

    def heuristic(self,a,b):
        return abs(a[0]-b[0])+abs(a[1]-b[1])

    def reconstruct_path(self,came_from,current):
        path=[]
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

