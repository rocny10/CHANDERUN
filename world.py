# ============================================
# world.py - CON SPRITE PARA CAJA
# ============================================
import pygame
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
            print("Fondo cargado correctamente")
        except:
            self.usar_fondo_azul()
    def usar_fondo_azul(self):
        self.imagen = pygame.Surface((self.ancho, self.alto))
        self.imagen.fill((135,206,235))
    def update(self, velocidad):
        pass
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (0,0))

class Refresco:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE
        self.recogido = False
        self.valor = REFRESCO_VALOR_BASE
        self.imagen = None
        try:
            tmp = pygame.image.load("assets/refresco.png").convert_alpha()
            self.imagen = pygame.transform.scale(tmp, (SPRITE_SIZE, SPRITE_SIZE))
            print("✅ Sprite refresco cargado")
        except:
            pass
    def update(self, velocidad):
        self.x -= velocidad
    def dibujar(self, pantalla):
        if self.recogido or self.x < -self.ancho:
            return
        y = self.y_suelo - self.alto
        if self.imagen:
            pantalla.blit(self.imagen, (self.x, y))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.x, y, self.ancho, self.alto))
            pygame.draw.rect(pantalla, BLANCO, (self.x+5, y+10, 20,20),2)
            f = pygame.font.Font(None,15)
            t = f.render("LATA", True, BLANCO)
            pantalla.blit(t, (self.x+10, y+20))
    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)

class Sierra:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE
        self.imagen = None
        try:
            tmp = pygame.image.load("assets/sierra.png").convert_alpha()
            self.imagen = pygame.transform.scale(tmp, (SPRITE_SIZE, SPRITE_SIZE))
            print("✅ Sprite sierra cargado")
        except:
            pass
    def update(self, velocidad):
        self.x -= velocidad
    def dibujar(self, pantalla):
        y = self.y_suelo - self.alto
        if self.imagen:
            pantalla.blit(self.imagen, (self.x, y))
        else:
            cx = self.x + self.ancho//2
            cy = y + self.alto//2
            radio = self.ancho//2 - 4
            pygame.draw.circle(pantalla, GRIS, (cx, cy), radio)
            for i in range(8):
                ang = i * math.pi/4
                dx = cx + math.cos(ang) * (radio+6)
                dy = cy + math.sin(ang) * (radio+6)
                pygame.draw.circle(pantalla, GRIS_OSCURO, (int(dx), int(dy)), 5)
    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)

class Caja:
    def __init__(self, x, y_suelo):
        self.x = x
        self.y_suelo = y_suelo
        self.ancho = SPRITE_SIZE
        self.alto = SPRITE_SIZE
        self.imagen = None
        try:
            tmp = pygame.image.load("assets/caja.png").convert_alpha()
            self.imagen = pygame.transform.scale(tmp, (SPRITE_SIZE, SPRITE_SIZE))
            print("✅ Sprite caja cargado")
        except:
            pass
    def update(self, velocidad):
        self.x -= velocidad
    def dibujar(self, pantalla):
        y = self.y_suelo - self.alto
        if self.imagen:
            pantalla.blit(self.imagen, (self.x, y))
        else:
            pygame.draw.rect(pantalla, MARRON, (self.x, y, self.ancho, self.alto))
            pygame.draw.rect(pantalla, NEGRO, (self.x, y, self.ancho, self.alto), 3)
    def get_rect(self):
        return pygame.Rect(self.x, self.y_suelo - self.alto, self.ancho, self.alto)