# ============================================
# player.py
# ============================================
import pygame, os, math
from config import *


# ── Sheet loader ─────────────────────────────────────────────────

def _load_sheet(path, fw, fh, cols, total, out_w, out_h=None):
    out_h = out_h or out_w
    frames = []
    sheet  = pygame.image.load(path).convert_alpha()
    for i in range(total):
        x = (i % cols) * fw
        y = (i // cols) * fh
        frames.append(pygame.transform.scale(
            sheet.subsurface((x, y, fw, fh)), (out_w, out_h)))
    return frames


# ── Vector fallbacks ─────────────────────────────────────────────

def _vec(cc, cd, tipo="run", n=6, sz=None):
    sz = sz or PLAYER_SIZE
    cx = sz // 2
    frames = []

    if tipo == "idle":
        for i in range(max(n, 4)):
            s = pygame.Surface((sz, sz), pygame.SRCALPHA)
            bob = int(math.sin(i * math.pi / 2) * 2)
            cy_c = sz // 5 + bob; rc = sz // 9
            pygame.draw.circle(s, cc, (cx, cy_c), rc)
            pygame.draw.circle(s, cd, (cx, cy_c), rc, 2)
            tt = cy_c + rc; tb = sz * 55 // 100 + bob
            pygame.draw.line(s, cd, (cx, tt), (cx, tb), 3)
            hom = tt + 4
            for sg in (1, -1):
                pygame.draw.line(s, cd, (cx, hom), (cx+sg*sz//5, hom+sz//5), 2)
            for sg in (1, -1):
                pygame.draw.line(s, cd, (cx, tb), (cx+sg*sz//8, sz*90//100), 3)
            frames.append(s)

    elif tipo == "run":
        ciclo = [(-20,-10,15,5),(-10,0,10,-5),(0,15,5,-10),
                 (10,20,-5,15),(20,10,-10,5),(10,0,5,-10)]
        for i in range(max(n, 6)):
            s = pygame.Surface((sz, sz), pygame.SRCALPHA)
            a1,a2,a3,a4 = [math.radians(a) for a in ciclo[i%6]]
            cy_c = sz//5; rc = sz//9
            pygame.draw.circle(s, cc, (cx, cy_c), rc)
            pygame.draw.circle(s, cd, (cx, cy_c), rc, 2)
            tt = cy_c+rc; tb = sz*55//100
            pygame.draw.line(s, cd, (cx,tt),(cx,tb),3)
            hom = tt+4; lb = sz//4
            for sg,ag in ((1,a1),(-1,a2)):
                bx=int(cx+sg*math.cos(ag)*lb); by=int(hom+math.sin(abs(ag))*lb)
                pygame.draw.line(s, cd, (cx,hom),(bx,by),2)
            lp = sz//3
            for sg,ag in ((1,a3),(-1,a4)):
                rx=int(cx+sg*math.cos(ag)*lp*0.5); ry=int(tb+lp*0.5)
                px=int(rx+sg*math.cos(ag*0.5)*lp*0.6); py=int(ry+lp*0.45)
                pygame.draw.line(s, cd,(cx,tb),(rx,ry),3)
                pygame.draw.line(s, cd,(rx,ry),(px,py),3)
            frames.append(s)

    elif tipo == "jump":
        for _ in range(max(n, 4)):
            s = pygame.Surface((sz, sz), pygame.SRCALPHA)
            cy_c = sz//6; rc = sz//9
            pygame.draw.circle(s, cc, (cx, cy_c), rc)
            pygame.draw.circle(s, cd, (cx, cy_c), rc, 2)
            tt = cy_c+rc; tb = sz*50//100
            pygame.draw.line(s, cd, (cx,tt),(cx,tb),3)
            hom = tt+4
            for sg in (1,-1):
                pygame.draw.line(s, cd, (cx,hom),(cx+sg*sz//3, hom-sz//8),2)
            for sg in (1,-1):
                rx=cx+sg*sz//4; ry=tb+sz//4
                pygame.draw.line(s, cd,(cx,tb),(rx,ry),3)
                pygame.draw.line(s, cd,(rx,ry),(cx+sg*sz//5,tb+sz//3),3)
            frames.append(s)

    elif tipo == "slide":
        # Stickman agachado — mismo tamaño PLAYER_SIZE×PLAYER_SIZE
        # El sprite cubre la mitad inferior del cuadrado
        for i in range(max(n, 8)):
            s = pygame.Surface((sz, sz), pygame.SRCALPHA)
            # Cuerpo en la mitad inferior
            base_y = sz * 3 // 5
            cy_c   = base_y - sz // 6; rc = sz // 10
            pygame.draw.circle(s, cc, (cx, cy_c), rc)
            pygame.draw.circle(s, cd, (cx, cy_c), rc, 2)
            # Torso inclinado hacia adelante
            tx = cx + sz // 5; ty = base_y + 4
            pygame.draw.line(s, cd, (cx, cy_c+rc), (tx, ty), 3)
            # Brazo adelante
            pygame.draw.line(s, cd, (cx+sz//8, cy_c+rc+4),
                             (cx+sz//3, ty-6), 2)
            # Piernas corriendo agachado
            t = (i % 4) / 4.0 * math.pi * 2
            for sg, off in ((1, 0), (-1, math.pi)):
                lx = int(cx + sg * sz//4 * math.cos(t+off) * 0.6)
                ly = int(base_y + sz//5 * abs(math.sin(t+off)) + 2)
                pygame.draw.line(s, cd, (tx, ty), (lx, min(ly, sz-4)), 3)
            frames.append(s)

    elif tipo == "dead":
        for i in range(max(n, 6)):
            s = pygame.Surface((sz, sz), pygame.SRCALPHA)
            prog = i / max(n-1, 1)
            cy_c = int(sz//2 + prog*sz//4)
            cx_c = int(sz//4 + prog*sz//4)
            rc   = sz // 9
            pygame.draw.circle(s, cc, (cx_c, cy_c), rc)
            pygame.draw.circle(s, cd, (cx_c, cy_c), rc, 2)
            ex = int(cx_c + sz//3)
            pygame.draw.line(s, cd, (cx_c, cy_c+rc), (ex, cy_c+rc), 3)
            pygame.draw.line(s, cd, (cx_c+sz//6, cy_c+rc+4),
                             (cx_c+sz//6, cy_c+rc+sz//5), 2)
            pygame.draw.line(s, cd, (ex, cy_c+rc),
                             (ex+sz//5, cy_c+rc+int(prog*sz//4)), 3)
            pygame.draw.line(s, cd, (ex-sz//8, cy_c+rc),
                             (ex-sz//8+sz//5, cy_c+rc+int(prog*sz//5)), 3)
            frames.append(s)

    elif tipo == "spin":
        # Spin simple: rotación del idle
        n_real = max(n, 8)
        base = _vec(cc, cd, "idle", 4, sz)
        for i in range(n_real):
            ang  = 360 * i / n_real
            scl  = max(0.2, abs(math.cos(math.radians(ang))))
            src  = base[i % len(base)]
            w    = max(4, int(sz * scl))
            rotf = pygame.transform.scale(src, (w, sz))
            canvas = pygame.Surface((sz, sz), pygame.SRCALPHA)
            canvas.blit(rotf, ((sz-w)//2, 0))
            frames.append(canvas)

    if not frames:
        surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
        surf.fill((*cc, 200)); frames = [surf]
    return frames


# ── Skins definición ─────────────────────────────────────────────
def _sufijo(idx):
    return ("", "2", "3")[idx]

def _path(anim, idx):
    return f"assets/{anim}_sheet{_sufijo(idx)}.png"

SKINS_COLORES = [
    {'cc':(220,180,140), 'cd':(30,30,30)},    # Chande
    {'cc':(80, 140,220), 'cd':(20,60,130)},    # Pelo
    {'cc':(200, 80,200), 'cd':(100,20,100)},   # Arube
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

        self.anim_actual  = "idle"
        self.frame_idx    = 0
        self.ms_por_frame = 110
        self._ultimo_tick = pygame.time.get_ticks()

        # Slide state machine
        # 'down'=bajando, 'hold'=quieto agachado, 'up'=levantándose
        self._slide_phase = 'down'
        self._SLIDE_HOLD  = 3   # frame donde se detiene al agacharse

        # Muerte
        self._muriendo    = False
        self._muerte_done = False

        self._skins: list = []
        self._cargar_skins()
        self._skin = min(skin, len(self._skins)-1)

    # ── skin property ────────────────────────────────────────────
    @property
    def skin(self): return self._skin

    @skin.setter
    def skin(self, v):
        v = max(0, min(v, len(self._skins)-1))
        self._skin = v
        self.frame_idx = 0
        self._ultimo_tick = pygame.time.get_ticks()

    @property
    def frames(self): return self._skins[self._skin]

    # ── Carga skins ───────────────────────────────────────────────
    def _cargar_skins(self):
        for idx, col in enumerate(SKINS_COLORES):
            cc, cd = col['cc'], col['cd']
            d = {a: [] for a in ("idle","run","jump","slide","dead","spin")}

            for anim in ("idle","run","jump","slide","dead","spin"):
                path = _path(anim, idx)
                if os.path.exists(path):
                    try:
                        d[anim] = _load_sheet(
                            path, _FW, _FH, _COLS, _FRAMES,
                            PLAYER_SIZE, PLAYER_SIZE)
                        print(f"OK {NOMBRE_SKIN[idx]} {anim}")
                    except Exception as e:
                        print(f"Warn {NOMBRE_SKIN[idx]} {anim}: {e}")

            if not d['idle']:  d['idle']  = _vec(cc, cd, "idle",  8, PLAYER_SIZE)
            if not d['run']:   d['run']   = _vec(cc, cd, "run",   8, PLAYER_SIZE)
            if not d['jump']:  d['jump']  = _vec(cc, cd, "jump",  8, PLAYER_SIZE)
            if not d['slide']: d['slide'] = _vec(cc, cd, "slide", 8, PLAYER_SIZE)
            if not d['dead']:  d['dead']  = _vec(cc, cd, "dead",  8, PLAYER_SIZE)
            if not d['spin']:  d['spin']  = _vec(cc, cd, "spin",  8, PLAYER_SIZE)

            self._skins.append(d)

    # ── Animación ────────────────────────────────────────────────
    def set_animacion(self, nombre):
        if nombre in self.frames and nombre != self.anim_actual:
            self.anim_actual  = nombre
            self.frame_idx    = 0
            self._ultimo_tick = pygame.time.get_ticks()

    def avanzar_frame(self):
        ahora = pygame.time.get_ticks()
        if ahora - self._ultimo_tick < self.ms_por_frame:
            return
        self._ultimo_tick = ahora

        lista = self.frames[self.anim_actual]
        if not lista: return
        n = len(lista)

        if self.anim_actual == "dead":
            # Una sola pasada
            if self.frame_idx < n - 1:
                self.frame_idx += 1
            else:
                self._muerte_done = True
            return

        if self.anim_actual == "slide":
            hold = min(self._SLIDE_HOLD, n-1)
            if self._slide_phase == 'down':
                if self.frame_idx < hold:
                    self.frame_idx += 1
                else:
                    self.frame_idx    = hold
                    self._slide_phase = 'hold'
            elif self._slide_phase == 'hold':
                self.frame_idx = hold   # fijo
            elif self._slide_phase == 'up':
                if self.frame_idx < n - 1:
                    self.frame_idx += 1
                else:
                    # animación terminada → volver a run
                    self.agachado = False
                    self.set_animacion("run")
            return

        # Loop normal
        self.frame_idx = (self.frame_idx + 1) % n

    # ── Acciones ─────────────────────────────────────────────────
    def saltar(self):
        if self.en_suelo and not self.agachado and not self._muriendo:
            self.vel_y = VEL_SALTO
            self.en_suelo = False; self.saltando = True
            self.saltos_totales += 1

    def soltar_salto(self):
        if self.saltando and self.vel_y < VEL_SALTO_CORTE:
            self.vel_y = VEL_SALTO_CORTE
        self.saltando = False

    def agachar(self, activar):
        if self._muriendo: return
        if activar and not self.agachado:
            self.agachado     = True
            self._slide_phase = 'down'
            self.set_animacion("slide")
        elif not activar and self.agachado:
            if self._slide_phase in ('down', 'hold'):
                self._slide_phase = 'up'
                # Continuar desde el frame de hold
                lista = self.frames.get("slide", [])
                self.frame_idx = min(self._SLIDE_HOLD, len(lista)-1)
                self._ultimo_tick = pygame.time.get_ticks()

    def morir(self):
        self._muriendo    = True
        self._muerte_done = False
        self.vel_y = 0
        self.agachado = False
        self.set_animacion("dead")

    @property
    def muerte_terminada(self): return self._muerte_done

    def aplicar_powerup(self, n): self.powerups.append(n)
    def tiene_powerup(self, n):   return n in self.powerups
    def usar_powerup(self, n):
        if n in self.powerups: self.powerups.remove(n); return True
        return False

    # ── Update ───────────────────────────────────────────────────
    def update(self, jugando=True):
        if self._muriendo:
            self.avanzar_frame(); return

        if self.mov_izq: self.x = max(X_MIN, self.x - VEL_LATERAL)
        if self.mov_der: self.x = min(X_MAX, self.x + VEL_LATERAL)

        self.vel_y += GRAVEDAD
        self.y     += self.vel_y
        if self.y >= SUELO_Y:
            self.y = SUELO_Y; self.vel_y = 0
            self.en_suelo = True; self.saltando = False

        if jugando:
            if not self.en_suelo:
                self.set_animacion("jump")
            elif not self.agachado:
                self.set_animacion("run")
            # Si agachado → set_animacion("slide") ya fue llamado por agachar()

        self.avanzar_frame()
        self.distancia += 1

    # ── Dibujo ───────────────────────────────────────────────────
    def dibujar(self, pantalla, alpha=255):
        lista = self.frames[self.anim_actual]
        if not lista: return
        frame = lista[self.frame_idx % len(lista)]

        # Todos los frames se dibujan al mismo tamaño PLAYER_SIZE×PLAYER_SIZE
        # SIN escalar — el sprite ya contiene la pose correcta
        # Posición: pies en self.y
        x = int(self.x) - PLAYER_SIZE // 2
        y = int(self.y) - PLAYER_SIZE

        if alpha < 255:
            frame = frame.copy(); frame.set_alpha(alpha)

        pantalla.blit(frame, (x, y))

    # ── Hitbox ───────────────────────────────────────────────────
    def get_rect(self):
        if self.agachado:
            # Mitad inferior (agachado)
            return pygame.Rect(
                int(self.x) - HITBOX_W // 2,
                int(self.y) - PLAYER_SIZE // 2,
                HITBOX_W, PLAYER_SIZE // 2)
        return pygame.Rect(
            int(self.x) - HITBOX_W // 2,
            int(self.y) - HITBOX_H,
            HITBOX_W, HITBOX_H)

    # ── Preview animado para tienda / menú ───────────────────────
    def get_frame_preview(self, skin_idx, anim="spin", tick=0, size=None):
        if skin_idx >= len(self._skins): return None
        d = self._skins[skin_idx]
        lista = d.get(anim) or d.get("idle", [])
        if not lista: return None
        idx   = (tick // 110) % len(lista)
        frame = lista[idx]
        if size and size != PLAYER_SIZE:
            frame = pygame.transform.scale(frame, (size, size))
        return frame
