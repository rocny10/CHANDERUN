# world.py (versión estable)
import pygame
import random
import math
import os
from config import *

class FondoPersonalizado:
    def __init__(self, archivo="assets/fondo.jpg"):
        self.archivo = archivo
        self.imagen = None
        self.ancho = ANCHO
        self.alto = ALTO
        self.cargar()

    def cargar(self):
        if not os.path.exists(self.archivo):
            print(f"Fondo no encontrado: {self.archivo}, usando azul")
            self.usar_fondo_azul()
            return
        try:
            img = pygame.image.load(self.archivo)
            if self.archivo.lower().endswith('.png'):
                img = img.convert_alpha()
            else:
                img = img.convert()
            self.imagen = pygame.transform.scale(img, (self.ancho, self.alto))
            print("Fondo cargado")
        except Exception as e:
            print(f"Error fondo: {e}, usando azul")
            self.usar_fondo_azul()

    def usar_fondo_azul(self):
        self.imagen = pygame.Surface((self.ancho, self.alto))
        self.imagen.fill((135,206,235))

    def update(self, velocidad):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (0,0))

# -------------------------------------------------------------------
# Refresco
# -------------------------------------------------------------------
REFRESCO_IMG = None
try:
    tmp = pygame.image.load("assets/refresco.png").convert_alpha()
    REFRESCO_IMG = pygame.transform.scale(tmp, (SPRITE_SIZE, SPRITE_SIZE))
    print("Sprite refresco cargado")
except:
    print("No se encontró assets/refresco.png, usando placeholder")
    REFRESCO_IMG = None

class Refresco:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE
        self.recogido = False
        self.valor = REFRESCO_VALOR_BASE
        self.imagen = REFRESCO_IMG

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        if self.recogido or self.x < -self.ancho:
            return
        y_dibujo = self.y_suelo - self.alto
        if self.imagen:
            pantalla.blit(self.imagen, (self.x, y_dibujo))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.x, y_dibujo, self.ancho, self.alto))
            pygame.draw.rect(pantalla, BLANCO, (self.x+5, y_dibujo+10, 20,20),2)
            f = pygame.font.Font(None,15)
            t = f.render("LATA", True, BLANCO)
            pantalla.blit(t, (self.x+10, y_dibujo+20))

    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)

# -------------------------------------------------------------------
# Sierra
# -------------------------------------------------------------------
class Sierra:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        # El rectángulo de dibujo: desde (self.x, self.y_suelo - self.alto) hasta (self.x + self.ancho, self.y_suelo)
        y_dibujo = self.y_suelo - self.alto
        centro_x = self.x + self.ancho // 2
        centro_y = y_dibujo + self.alto // 2
        radio = self.ancho // 2 - 4
        pygame.draw.circle(pantalla, GRIS, (centro_x, centro_y), radio)
        for i in range(8):
            ang = i * math.pi / 4
            dx = centro_x + math.cos(ang) * (radio + 6)
            dy = centro_y + math.sin(ang) * (radio + 6)
            pygame.draw.circle(pantalla, GRIS_OSCURO, (int(dx), int(dy)), 5)

    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)

# -------------------------------------------------------------------
# Caja
# -------------------------------------------------------------------
class Caja:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        y_dibujo = self.y_suelo - self.alto
        pygame.draw.rect(pantalla, MARRON, (self.x, y_dibujo, self.ancho, self.alto))
        pygame.draw.rect(pantalla, NEGRO, (self.x, y_dibujo, self.ancho, self.alto), 3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)