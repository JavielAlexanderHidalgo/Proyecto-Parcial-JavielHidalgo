#JAVIEL ALEXANDER HIDALGO
# Clase para la espada
class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # Cargar la imagen de la espada según la dirección
        if direction == 'derecha':
            self.image = sword_right_image
        elif direction == 'izquierda':
            self.image = sword_left_image
        elif direction == 'arriba':
            self.image = sword_up_image
        elif direction == 'abajo':
            self.image = sword_down_image

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 40  # Velocidad de la espada
        self.direction = direction

    def update(self, enemies, mapa):
        # Mover la espada según la dirección
        new_x, new_y = self.rect.x, self.rect.y
        if self.direction == 'derecha':
            new_x += self.speed
        elif self.direction == 'izquierda':
            new_x -= self.speed
        elif self.direction == 'arriba':
            new_y -= self.speed
        elif self.direction == 'abajo':
            new_y += self.speed

        # Convertir coordenadas a índices de matriz
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE

        # Comprobar colisión con paredes
        if 0 <= tile_x < columnas and 0 <= tile_y < filas:
            if mapa[tile_y][tile_x] == 1:
                self.kill()
                return

            # Actualizar posición de la espada
            self.rect.topleft = (new_x, new_y)

            # Comprobar colisiones con enemigos
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    # Reducir vida del enemigo y actualizar su color
                    if hasattr(enemy, 'vida') and hasattr(enemy, 'vivo') and enemy.vivo:
                        enemy.vida -= 85  # Ajusta el daño a tu gusto
                        if enemy.vida <= 0:
                            enemy.vivo = False
                            enemy.kill()
                        else:
                            # Cambiar el color del enemigo progresivamente a rojo
                            rojo = 255 - enemy.vida
                            overlay = pygame.Surface(enemy.image.get_size(), pygame.SRCALPHA)
                            overlay.fill((rojo, 0, 0, 100))
                            enemy.image = enemy.image.copy()
                            enemy.image.blit(overlay, (0, 0))
                    self.kill()
                    break
