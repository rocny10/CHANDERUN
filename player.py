# ============================================
# player.py
# ============================================
import pygame
import os
import math
from config import *


def _cargar_sheet(path, fw, fh, cols, total, out_size):
    frames = []
    sheet  = pygame.image.load(path).convert_alpha()
    for i in range(total):
        x = (i % cols) * fw
        y = (i // cols) * fh
        frame = sheet.subsurface((x, y, fw, fh))
        frames.append(pygame.transform.scale(frame, (out_size, out_size)))
    return frames


def _vector_run(cc, cd, n=6, sz=None):
    sz = sz or PLAYER_SIZE
    frames = []
    ciclo = [(-20,-10,15,5),(-10,0,10,-5),(0,15,5,-10),
             (10,20,-5,15),(20,10,-10,5),(10,0,5,-10)]
    for i in range(n):
        s = pygame.Surface((sz, sz), pygame.SRCALPHA)
        a1,a2,a3,a4 = [math.radians(a) for a in ciclo[i]]
        cx = sz//2; cy_c = sz//5; rc = sz//9
        pygame.draw.circle(s, cc, (cx, cy_c), rc)
        pygame.draw.circle(s, cd, (cx, cy_c), rc, 2)
        tt = cy_c+rc; tb = sz*55//100
        pygame.draw.line(s, cd, (cx,tt), (cx,tb), 3)
        hom = tt+4; lb = sz//4
        for sg,ag in ((1,a1),(-1,a2)):
            bx=int(cx+sg*math.cos(ag)*lb); by=int(hom+math.sin(abs(ag))*lb)
            pygame.draw.line(s, cd, (cx,hom), (bx,by), 2)
        lp = sz//3
        for sg,ag in ((1,a3),(-1,a4)):
            rx=int(cx+sg*math.cos(ag)*lp*0.5); ry=int(tb+lp*0.5)
            px=int(rx+sg*math.cos(ag*0.5)*lp*0.6); py=int(ry+lp*0.45)
            pygame.draw.line(s, cd, (cx,tb), (rx,ry), 3)
            pygame.draw.line(s, cd, (rx,ry), (px,py), 3)
        frames.append(s)
    return frames


def _vector_idle(cc, cd, n=4, sz=None):
    sz = sz or PLAYER_SIZE
    frames = []; cx = sz//2
    for i in range(n):
        s = pygame.Surface((sz, sz), pygame.SRCALPHA)
        bob = int(math.sin(i*math.pi/2)*2)
        cy_c = sz//5+bob; rc = sz//9
        pygame.draw.circle(s, cc, (cx,cy_c), rc)
        pygame.draw.circle(s, cd, (cx,cy_c), rc, 2)
        tt = cy_c+rc; tb = sz*55//100+bob
        pygame.draw.line(s, cd, (cx,tt), (cx,tb), 3)
        hom = tt+4
        for sg in (1,-1):
            pygame.draw.line(s, cd, (cx,hom), (cx+sg*sz//5, hom+sz//5), 2)
        for sg in (1,-1):
            pygame.draw.line(s, cd, (cx,tb), (cx+sg*sz//8, sz*90//100), 3)
        frames.append(s)
    return frames


def _vector_jump(cc, cd, n=4, sz=None):
    sz = sz or PLAYER_SIZE
    frames = []; cx = sz//2
    for _ in range(n):
        s = pygame.Surface((sz, sz), pygame.SRCALPHA)
        cy_c = sz//6; rc = sz//9
        pygame.draw.circle(s, cc, (cx,cy_c), rc)
        pygame.draw.circle(s, cd, (cx,cy_c), rc, 2)
        tt = cy_c+rc; tb = sz*50//100
        pygame.draw.line(s, cd, (cx,tt), (cx,tb), 3)
        hom = tt+4
        for sg in (1,-1):
            pygame.draw.line(s, cd, (cx,hom), (cx+sg*sz//3, hom-sz//8), 2)
        for sg in (1,-1):
            rx=cx+sg*sz//4; ry=tb+sz//4
            pygame.draw.line(s, cd, (cx,tb), (rx,ry), 3)
            pygame.draw.line(s, cd, (rx,ry), (cx+sg*sz//5, tb+sz//3), 3)
        frames.append(s)
    return frames


SKINS_DEF = [
    {'idle':"assets/idle_sheet.png",  'run':"assets/run_sheet.png",  'jump':"assets/jump_sheet.png",
     'cc':(220,180,140), 'cd':(30,30,30)},
    {'idle':"assets/idle_sheet_2.png",'run':"assets/run_sheet_2.png",'jump':"assets/jump_sheet_2.png",
     'cc':(80,140,220),  'cd':(20,60,130)},
]
_COLS=5; _FRAMES=8; _FW=56; _FH=56


class Stickman:
    def __init__(self, x, y, skin=0):
        self.x = float(x); self.y = float(y)
        self.vel_y = 0.0; self.en_suelo = True
        self.agachado = False; self.saltando = False
        self.mov_izq = False; self.mov_der = False
        self.powerups = []
        self.saltos_totales = 0; self.distancia = 0

        self.anim_actual = "idle"; self.frame_idx = 0
        self.ms_por_frame = 110
        self._ultimo_tick = pygame.time.get_ticks()

        self._skins: list = []
        self._cargar_skins()
        self._skin = min(skin, len(self._skins)-1)

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, value):
        value = max(0, min(value, len(self._skins)-1))
        self._skin = value
        self.frame_idx = 0
        self._ultimo_tick = pygame.time.get_ticks()

    @property
    def frames(self):
        return self._skins[self._skin]

    def _cargar_skins(self):
        for sdef in SKINS_DEF:
            d = {"idle":[], "run":[], "jump":[]}
            for anim in ("idle","run","jump"):
                path = sdef[anim]
                if os.path.exists(path):
                    try:
                        # Cargar a PLAYER_SIZE (no SPRITE_SIZE, aunque son lo mismo)
                        d[anim] = _cargar_sheet(path, _FW, _FH, _COLS, _FRAMES, PLAYER_SIZE)
                        print(f"OK {NOMBRE_SKIN.get(len(self._skins),'?')} {anim}: {len(d[anim])} frames @{PLAYER_SIZE}px")
                    except Exception as e:
                        print(f"Warn {anim}: {e}")
            cc, cd = sdef['cc'], sdef['cd']
            if not d['idle']:  d['idle'] = _vector_idle(cc, cd, sz=PLAYER_SIZE)
            if not d['run']:   d['run']  = _vector_run(cc, cd, sz=PLAYER_SIZE)
            if not d['jump']:  d['jump'] = _vector_jump(cc, cd, sz=PLAYER_SIZE)
            self._skins.append(d)

    def set_animacion(self, nombre):
        if nombre in self.frames and nombre != self.anim_actual:
            self.anim_actual = nombre
            self.frame_idx = 0
            self._ultimo_tick = pygame.time.get_ticks()

    def avanzar_frame(self):
        ahora = pygame.time.get_ticks()
        if ahora - self._ultimo_tick >= self.ms_por_frame:
            lista = self.frames[self.anim_actual]
            if lista:
                self.frame_idx = (self.frame_idx+1) % len(lista)
            self._ultimo_tick = ahora

    def saltar(self):
        if self.en_suelo and not self.agachado:
            self.vel_y = VEL_SALTO
            self.en_suelo = False; self.saltando = True
            self.saltos_totales += 1

    def soltar_salto(self):
        if self.saltando and self.vel_y < VEL_SALTO_CORTE:
            self.vel_y = VEL_SALTO_CORTE
        self.saltando = False

    def agachar(self, activar):
        self.agachado = activar

    def aplicar_powerup(self, n): self.powerups.append(n)
    def tiene_powerup(self, n):   return n in self.powerups
    def usar_powerup(self, n):
        if n in self.powerups: self.powerups.remove(n); return True
        return False

    def update(self, jugando=True):
        if self.mov_izq: self.x = max(X_MIN, self.x - VEL_LATERAL)
        if self.mov_der: self.x = min(X_MAX, self.x + VEL_LATERAL)

        self.vel_y += GRAVEDAD
        self.y     += self.vel_y
        if self.y >= SUELO_Y:
            self.y = SUELO_Y; self.vel_y = 0
            self.en_suelo = True; self.saltando = False

        if jugando:
            if not self.en_suelo: self.set_animacion("jump")
            else:                 self.set_animacion("run")

        self.avanzar_frame()
        self.distancia += 1

    def dibujar(self, pantalla, alpha=255):
        lista = self.frames[self.anim_actual]
        if not lista: return
        frame = lista[self.frame_idx % len(lista)]

        if self.agachado:
            # mitad inferior, aplastado
            f = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE//2))
            x = int(self.x) - PLAYER_SIZE//2
            y = int(self.y) - PLAYER_SIZE//2
        else:
            f = frame
            x = int(self.x) - PLAYER_SIZE//2
            y = int(self.y) - PLAYER_SIZE          # pies = self.y exacto

        if alpha < 255:
            f = f.copy()
            f.set_alpha(alpha)
        pantalla.blit(f, (x, y))

    def get_rect(self):
        if self.agachado:
            return pygame.Rect(int(self.x)-HITBOX_W//2,
                               int(self.y)-PLAYER_SIZE//2,
                               HITBOX_W, PLAYER_SIZE//2)
        return pygame.Rect(int(self.x)-HITBOX_W//2,
                           int(self.y)-HITBOX_H,
                           HITBOX_W, HITBOX_H)

    def get_frame_preview(self, skin_idx, anim="idle", size=None):
        """Devuelve un frame de la skin pedida, escalado si hace falta."""
        if skin_idx >= len(self._skins): return None
        lista = self._skins[skin_idx][anim]
        if not lista: return None
        frame = lista[0]
        if size and size != PLAYER_SIZE:
            frame = pygame.transform.scale(frame, (size, size))
        return frame
