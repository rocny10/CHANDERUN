# ============================================
# world.py - Completo y funcional
# ============================================
import pygame
import random
import math
import os
from config import *

# -------------------------------------------------------------------
# Fondo personalizado con imagen (con detección de errores)
# -------------------------------------------------------------------
class FondoPersonalizado:
    def __init__(self, archivo="assets/fondo.jpg"):
        """
        archivo: ruta a la imagen de fondo (por defecto assets/fondo.jpg)
        """
        self.archivo = archivo
        self.imagen = None
        self.ancho = ANCHO
        self.alto = ALTO
        self.cargar()

    def cargar(self):
        """Intenta cargar la imagen; si falla, usa un fondo de color sólido."""
        if not os.path.exists(self.archivo):
            print(f"⚠️ No se encuentra el archivo: {self.archivo}")
            print(f"   Buscando en: {os.path.abspath(self.archivo)}")
            self.usar_fondo_azul()
            return

        try:
            # Cargar la imagen
            img_original = pygame.image.load(self.archivo)
            # Convertir según el tipo (con o sin canal alfa)
            if self.archivo.lower().endswith('.png'):
                img_original = img_original.convert_alpha()
            else:
                img_original = img_original.convert()
            # Escalar al tamaño de la pantalla
            self.imagen = pygame.transform.scale(img_original, (self.ancho, self.alto))
            print(f"✅ Fondo cargado correctamente: {self.archivo}")
        except Exception as e:
            print(f"❌ Error al cargar la imagen {self.archivo}: {e}")
            self.usar_fondo_azul()

    def usar_fondo_azul(self):
        """Crea un fondo de color azul como respaldo."""
        self.imagen = pygame.Surface((self.ancho, self.alto))
        self.imagen.fill((135, 206, 235))  # Azul cielo
        print("⚠️ Usando fondo azul de emergencia")

    def update(self, velocidad):
        # Por ahora sin desplazamiento, pero se puede añadir después
        pass

    def dibujar(self, pantalla):
        """Dibuja el fondo en la pantalla."""
        pantalla.blit(self.imagen, (0, 0))

# -------------------------------------------------------------------
# Refresco (moneda) – intenta cargar un sprite; si no, usa placeholder
# -------------------------------------------------------------------
# Intentamos cargar la imagen del refresco una sola vez (para todos los objetos)
REFRESCO_IMG = None
try:
    img_temp = pygame.image.load("assets/refresco.png").convert_alpha()
    REFRESCO_IMG = pygame.transform.scale(img_temp, (30, 30))
    print("✅ Sprite de refresco cargado")
except:
    print("⚠️ No se encontró assets/refresco.png, se usará placeholder")

class Refresco:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.recogido = False
        self.valor = REFRESCO_VALOR_BASE
        self.imagen = REFRESCO_IMG  # Puede ser None

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        if self.recogido or self.x < -self.ancho:
            return
        if self.imagen:
            # Dibujar el sprite
            pantalla.blit(self.imagen, (self.x, self.y - 15))
        else:
            # Placeholder: rectángulo rojo con texto "LATA"
            pygame.draw.rect(pantalla, ROJO, (self.x, self.y - 15, self.ancho, self.alto))
            pygame.draw.rect(pantalla, BLANCO, (self.x + 5, self.y - 10, 20, 20), 2)
            fuente = pygame.font.Font(None, 15)
            texto = fuente.render("LATA", True, BLANCO)
            pantalla.blit(texto, (self.x + 2, self.y - 10))

    def get_rect(self):
        return pygame.Rect(self.x, self.y - 15, self.ancho, self.alto)

# -------------------------------------------------------------------
# Sierra (enemigo que mata)
# -------------------------------------------------------------------
class Sierra:
    def __init__(self, x):
        self.x = x
        self.y = SUELO_Y + 20 - 50
        self.ancho = 50
        self.alto = 50

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        # Cuerpo gris
        pygame.draw.circle(pantalla, GRIS, (int(self.x + 25), int(self.y + 25)), 25)
        # Dientes (ocho círculos pequeños alrededor)
        for i in range(8):
            ang = i * math.pi / 4
            dx = self.x + 25 + math.cos(ang) * 30
            dy = self.y + 25 + math.sin(ang) * 30
            pygame.draw.circle(pantalla, GRIS_OSCURO, (int(dx), int(dy)), 5)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# -------------------------------------------------------------------
# Caja (obstáculo que no mata si pasas por encima)
# -------------------------------------------------------------------
class Caja:
    def __init__(self, x):
        self.x = x
        self.y = SUELO_Y + 20 - 60
        self.ancho = 60
        self.alto = 60

    def update(self, velocidad):
        self.x -= velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, MARRON, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, NEGRO, (self.x, self.y, self.ancho, self.alto), 3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    