# ============================================
# player.py (CORREGIDO)
# ============================================
import pygame
from config import *

class Stickman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.en_suelo = True
        self.agachado = False
        self.tiempo_carga = 0
        self.saltando = False
        self.powerups = []
        self.saltos_totales = 0
        self.distancia = 0
        self.esquivados = 0

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
            # Usar valores directamente para evitar NameError
            min_salto = -12
            max_salto = -25
            t = min(self.tiempo_carga, 30)
            fuerza = min_salto + (max_salto - min_salto) * (t / 30)
            self.vel_y = fuerza
            self.en_suelo = False
            self.saltando = False
            self.saltos_totales += 1

    def agachar(self, activar):
        self.agachado = activar

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
        if self.agachado:
            pygame.draw.rect(pantalla, ROJO, (self.x - 20, self.y - 20, 40, 20))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.x - 15, self.y - 40, 30, 40))

    def get_rect(self):
        if self.agachado:
            return pygame.Rect(self.x - 20, self.y - 20, 40, 20)
        return pygame.Rect(self.x - 15, self.y - 40, 30, 40)