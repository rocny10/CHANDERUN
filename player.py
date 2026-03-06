# ============================================
# PLAYER.PY - PERSONAJE (64x64)
# ============================================
import pygame
from config import *

class Stickman:
    def __init__(self, x, y):
        # Posición base: el sprite se dibuja con su centro inferior en (x, y)
        self.x = x
        self.y = y
        self.vel_y = 0
        self.en_suelo = True
        self.agachado = False          # No implementado con sprite aún
        self.tiempo_carga = 0
        self.saltando = False
        self.powerups = []
        self.saltos_totales = 0
        self.distancia = 0
        self.esquivados = 0

        # Sprite (placeholder rojo)
        self.sprite = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
        self.sprite.fill(ROJO)
        # Aquí cargarías tu sprite real

    def aplicar_powerup(self, nombre):
        self.powerups.append(nombre)

    def tiene_powerup(self, nombre):
        return nombre in self.powerups

    def usar_powerup(self, nombre):
        if nombre in self.powerups:
            self.powerups.remove(nombre)
            return True
        return False

    def iniciar_carga(self):
        if self.en_suelo and not self.agachado:
            self.saltando = True
            self.tiempo_carga = 0

    def finalizar_carga(self):
        if self.saltando:
            t = min(self.tiempo_carga, 30)
            fuerza = VEL_SALTO_MIN + (VEL_SALTO_MAX - VEL_SALTO_MIN) * (t / 30)
            self.vel_y = fuerza
            self.en_suelo = False
            self.saltando = False
            self.saltos_totales += 1

    def agachar(self, activar):
        self.agachado = activar   # Podría cambiar el sprite más adelante

    def esquivar(self):
        self.esquivados += 1

    def update(self):
        if self.saltando:
            self.tiempo_carga += 1
        self.vel_y += GRAVEDAD
        self.y += self.vel_y
        if self.y >= SUELO_Y:
            self.y = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True
        else:
            self.en_suelo = False
        self.distancia += 1

    def dibujar(self, pantalla):
        # El sprite se dibuja con su esquina superior izquierda en (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE)
        pantalla.blit(self.sprite, (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE))

    def get_rect(self):
        return pygame.Rect(self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)