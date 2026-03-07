# ============================================
# player.py - VERSIÓN DEFINITIVA
# ============================================
import pygame
import os
from config import *

class Stickman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.en_suelo = True
        self.agachado = False
        self.powerups = []
        self.saltos_totales = 0
        self.distancia = 0
        self.esquivados = 0

        self.cargando_salto = False
        self.tiempo_carga = 0
        self.animacion_actual = "idle"

        # Sprites
        self.sprites = {}
        self.cargar_sprites()
        self.sprite_actual = self.sprites.get("idle", self._crear_fallback())

    def _crear_fallback(self):
        surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        surf.fill(ROJO)
        return surf

    def cargar_sprites(self):
        """Carga los sprites desde archivos individuales o spritesheets"""
        # Intenta cargar cada animación
        animaciones = ["idle", "run", "jump"]
        for anim in animaciones:
            sprite = None
            # Buscar archivo: assets/anim.png o assets/anim_sheet.png
            rutas = [f"assets/{anim}.png", f"assets/{anim}_sheet.png"]
            for ruta in rutas:
                if os.path.exists(ruta):
                    try:
                        img = pygame.image.load(ruta).convert_alpha()
                        # Si es spritesheet, tomar el primer frame
                        if img.get_width() > 64:
                            # Asumimos primer frame de 56x56
                            img = img.subsurface((0, 0, 56, 56))
                        sprite = pygame.transform.scale(img, (SPRITE_SIZE, SPRITE_SIZE))
                        print(f"✅ {anim} cargado desde {ruta}")
                        break
                    except Exception as e:
                        print(f"❌ Error cargando {ruta}: {e}")
            if sprite is None:
                print(f"⚠️ {anim} no encontrado, usando fallback")
                sprite = self._crear_fallback()
            self.sprites[anim] = sprite

    def set_animacion(self, anim):
        if anim in self.sprites and anim != self.animacion_actual:
            self.animacion_actual = anim
            self.sprite_actual = self.sprites[anim]

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
            self.cargando_salto = True
            self.tiempo_carga = 0

    def cancelar_carga(self):
        self.cargando_salto = False

    def ejecutar_salto(self):
        if self.cargando_salto:
            t = min(self.tiempo_carga, 30)
            fuerza = VEL_SALTO_BASE + (VEL_SALTO_MAX - VEL_SALTO_BASE) * (t / 30)
            self.vel_y = fuerza
            self.en_suelo = False
            self.cargando_salto = False
            self.saltos_totales += 1
            self.set_animacion("jump")

    def agachar(self, activar):
        self.agachado = activar
        if activar:
            self.cancelar_carga()

    def esquivar(self):
        self.esquivados += 1

    def update(self):
        if self.cargando_salto:
            self.tiempo_carga += 1

        self.vel_y += GRAVEDAD
        self.y += self.vel_y

        if self.y >= SUELO_Y:
            self.y = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True
            if self.animacion_actual == "jump":
                self.set_animacion("idle")  # o "run" si estás corriendo
        else:
            self.en_suelo = False

        self.distancia += 1

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite_actual, (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE))

    def get_rect(self):
        return pygame.Rect(self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)