# ============================================
# player.py - CON ANIMACIÓN POR FRAMES MEJORADA
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

        # Frames de animación
        self.frames = {"idle": [], "run": [], "jump": []}
        self.frame_actual = 0
        self.ultimo_tiempo_anim = pygame.time.get_ticks()
        self.velocidad_anim = 150  # ms por frame

        self.cargar_sprites()

    def cargar_sprites(self):
        """Carga los sprites desde archivos. Para idle, carga todos los frames del spritesheet."""
        # IDLE: intentar cargar spritesheet
        try:
            if os.path.exists("assets/idle_sheet.png"):
                sheet = pygame.image.load("assets/idle_sheet.png").convert_alpha()
                frame_w, frame_h = 56, 56
                cols = 5
                total_frames = 8
                for i in range(total_frames):
                    fila = i // cols
                    col = i % cols
                    x = col * frame_w
                    y = fila * frame_h
                    frame = sheet.subsurface((x, y, frame_w, frame_h))
                    frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                    self.frames["idle"].append(frame)
                print(f"✅ Idle: {len(self.frames['idle'])} frames cargados")
            else:
                print("⚠️ No se encontró idle_sheet.png, usando jump como fallback")
                # Usar los frames de jump si existen
                if os.path.exists("assets/jump_sheet.png"):
                    sheet = pygame.image.load("assets/jump_sheet.png").convert_alpha()
                    frame_w, frame_h = 56, 56
                    cols = 5
                    total_frames = 8
                    for i in range(total_frames):
                        fila = i // cols
                        col = i % cols
                        x = col * frame_w
                        y = fila * frame_h
                        frame = sheet.subsurface((x, y, frame_w, frame_h))
                        frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                        self.frames["idle"].append(frame)
                    print("✅ Usando jump como idle temporal")
                else:
                    # Crear frames simples
                    for i in range(4):
                        surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
                        surf.fill((200 + i*15, 50, 50))
                        self.frames["idle"].append(surf)
        except Exception as e:
            print(f"❌ Error cargando idle: {e}, creando frames simples")
            for i in range(4):
                surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
                surf.fill((200 + i*15, 50, 50))
                self.frames["idle"].append(surf)

        # JUMP
        try:
            if os.path.exists("assets/jump_sheet.png"):
                sheet = pygame.image.load("assets/jump_sheet.png").convert_alpha()
                frame_w, frame_h = 56, 56
                cols = 5
                total_frames = 8
                for i in range(total_frames):
                    fila = i // cols
                    col = i % cols
                    x = col * frame_w
                    y = fila * frame_h
                    frame = sheet.subsurface((x, y, frame_w, frame_h))
                    frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                    self.frames["jump"].append(frame)
                print(f"✅ Jump: {len(self.frames['jump'])} frames cargados")
            else:
                print("⚠️ No se encontró jump_sheet.png, usando idle como fallback")
                self.frames["jump"] = self.frames["idle"]
        except Exception as e:
            print(f"❌ Error cargando jump: {e}")
            self.frames["jump"] = self.frames["idle"]

        # RUN (usar idle si no existe)
        try:
            if os.path.exists("assets/run_sheet.png"):
                sheet = pygame.image.load("assets/run_sheet.png").convert_alpha()
                frame_w, frame_h = 56, 56
                cols = 5
                total_frames = 8
                for i in range(total_frames):
                    fila = i // cols
                    col = i % cols
                    x = col * frame_w
                    y = fila * frame_h
                    frame = sheet.subsurface((x, y, frame_w, frame_h))
                    frame = pygame.transform.scale(frame, (SPRITE_SIZE, SPRITE_SIZE))
                    self.frames["run"].append(frame)
                print(f"✅ Run: {len(self.frames['run'])} frames cargados")
            else:
                self.frames["run"] = self.frames["idle"]
        except:
            self.frames["run"] = self.frames["idle"]

    def set_animacion(self, anim):
        if anim in self.frames and anim != self.animacion_actual:
            self.animacion_actual = anim
            self.frame_actual = 0
            self.ultimo_tiempo_anim = pygame.time.get_ticks()

    def actualizar_animacion(self):
        """Avanza el frame de la animación actual basado en el tiempo."""
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_tiempo_anim > self.velocidad_anim:
            self.ultimo_tiempo_anim = ahora
            frames = self.frames[self.animacion_actual]
            if frames:
                self.frame_actual = (self.frame_actual + 1) % len(frames)

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
        # Física
        if self.cargando_salto:
            self.tiempo_carga += 1

        self.vel_y += GRAVEDAD
        self.y += self.vel_y

        if self.y >= SUELO_Y:
            self.y = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True
            if self.animacion_actual == "jump":
                self.set_animacion("idle")
        else:
            self.en_suelo = False

        self.distancia += 1

        # Animación (se actualiza en el bucle principal también)

    def dibujar(self, pantalla):
        frames = self.frames[self.animacion_actual]
        if frames:
            frame = frames[self.frame_actual]
            pantalla.blit(frame, (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))

    def get_rect(self):
        return pygame.Rect(self.x - SPRITE_SIZE//2, self.y - SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)