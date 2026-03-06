# ============================================
# player.py - COMPLETO
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

        self.animaciones = {}
        self.animacion_actual = "idle"
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.ultimo_tiempo = pygame.time.get_ticks()
        self.velocidad_animacion = 150
        
        self.cargar_animaciones()

    def cargar_animaciones(self):
        try:
            sheet = pygame.image.load("assets/idle_sheet.png").convert_alpha()
            frame_width = 56
            frame_height = 56
            frames_idle = []
            frames_por_fila = 5
            total_frames = 8
            
            for i in range(total_frames):
                fila = i // frames_por_fila
                columna = i % frames_por_fila
                x = columna * frame_width
                y = fila * frame_height
                frame = sheet.subsurface((x, y, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                frames_idle.append(frame)
            
            self.animaciones["idle"] = frames_idle
            print(f"✅ Idle spritesheet cargado: {len(frames_idle)} frames")
        except:
            frames_idle = []
            for i in range(4):
                surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
                color = (200 + i*10, 50, 50)
                pygame.draw.rect(surf, color, (5, 5, SPRITE_SIZE-10, SPRITE_SIZE-10), border_radius=10)
                pygame.draw.rect(surf, BLANCO, (5, 5, SPRITE_SIZE-10, SPRITE_SIZE-10), 3)
                frames_idle.append(surf)
            self.animaciones["idle"] = frames_idle

        try:
            sheet = pygame.image.load("assets/run_sheet.png").convert_alpha()
            frame_width = 56
            frame_height = 56
            frames_run = []
            frames_por_fila = 5
            total_frames = 8
            
            for i in range(total_frames):
                fila = i // frames_por_fila
                columna = i % frames_por_fila
                x = columna * frame_width
                y = fila * frame_height
                frame = sheet.subsurface((x, y, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                frames_run.append(frame)
            
            self.animaciones["run"] = frames_run
            print(f"✅ Run spritesheet cargado: {len(frames_run)} frames")
        except:
            frames_run = []
            for i in range(4):
                surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
                offset = i * 5
                color = (50, 100 + i*30, 200)
                pygame.draw.rect(surf, color, (5 + offset, 5, SPRITE_SIZE-20, SPRITE_SIZE-10), border_radius=5)
                pygame.draw.rect(surf, BLANCO, (5 + offset, 5, SPRITE_SIZE-20, SPRITE_SIZE-10), 2)
                frames_run.append(surf)
            self.animaciones["run"] = frames_run

    def set_animacion(self, nombre):
        if nombre in self.animaciones and nombre != self.animacion_actual:
            self.animacion_actual = nombre
            self.frame_actual = 0

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
        else:
            self.en_suelo = False

        self.distancia += 1

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_tiempo > self.velocidad_animacion:
            self.ultimo_tiempo = ahora
            frames = self.animaciones[self.animacion_actual]
            self.frame_actual = (self.frame_actual + 1) % len(frames)

    def dibujar(self, pantalla):
        frames = self.animaciones[self.animacion_actual]
        frame = frames[self.frame_actual]
        pantalla.blit(frame, (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE))

    def get_rect(self):
        return pygame.Rect(self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)