# ============================================
# world.py
# ============================================
import pygame
import math
import os
import random
from config import *


def _cargar_sprite(path, size):
    if os.path.exists(path):
        try:
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), (size, size))
        except Exception as e:
            print(f"Warn {path}: {e}")
    return None


# ── FONDO CON PARALLAX ───────────────────────────────────────────
#
#  Capa 0 (bg):  velocidad × 0.15  — muy lenta
#  Capa 1 (mid): velocidad × 0.40  — media
#  Suelo:        velocidad × 1.00  — igual al juego
#
class Fondo:
    SUELO_COL  = ( 50,  48,  42)
    LINEA_COL  = ( 85,  78,  65)
    LINEA_ALT  = (110, 100,  82)

    def __init__(self, archivo="assets/fondo.jpg"):
        self._off_bg  = 0.0
        self._off_mid = 0.0
        self._off_suelo = 0.0

        # Intentar cargar imagen de fondo
        self._img_bg = None
        if os.path.exists(archivo):
            try:
                img = pygame.image.load(archivo)
                img = img.convert_alpha() if archivo.endswith('.png') else img.convert()
                self._img_bg = pygame.transform.scale(img, (ANCHO, ALTO))
                print("OK Fondo cargado")
            except Exception as e:
                print(f"Warn fondo: {e}")

        if not self._img_bg:
            s = pygame.Surface((ANCHO, ALTO))
            s.fill((45, 60, 100))
            self._img_bg = s

        # Crear capa media procedural (nubes/colinas superpuestas)
        self._mid_surf = self._crear_capa_media()

    def _crear_capa_media(self):
        """Capa semitransparente con elementos que dan sensación de profundidad."""
        s = pygame.Surface((ANCHO * 2, ALTO), pygame.SRCALPHA)
        # Algunas nubes/franjas horizontales difusas
        rng = random.Random(42)  # seed fija para consistencia
        for _ in range(18):
            x = rng.randint(0, ANCHO*2)
            y = rng.randint(30, SUELO_Y - 80)
            w = rng.randint(120, 320)
            h = rng.randint(18, 48)
            alpha = rng.randint(12, 28)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((255, 255, 255, alpha))
            s.blit(surf, (x, y))
        return s

    def update(self, velocidad):
        self._off_bg    = (self._off_bg    + velocidad * 0.12) % ANCHO
        self._off_mid   = (self._off_mid   + velocidad * 0.35) % (ANCHO * 2)
        self._off_suelo = (self._off_suelo + velocidad * 0.85) % 80

    def dibujar(self, pantalla):
        # ── Capa 0: bg looping ───────────────────────────────────
        ox = int(self._off_bg)
        pantalla.blit(self._img_bg, (-ox, 0))
        pantalla.blit(self._img_bg, (ANCHO - ox, 0))

        # ── Capa 1: nubes/mid paralax ────────────────────────────
        ox2 = int(self._off_mid)
        pantalla.blit(self._mid_surf, (-ox2, 0))
        # segunda pasada para seamless
        pantalla.blit(self._mid_surf, (ANCHO*2 - ox2, 0))

        # ── Suelo sólido ─────────────────────────────────────────
        suelo_h = ALTO - SUELO_Y
        pygame.draw.rect(pantalla, self.SUELO_COL, (0, SUELO_Y, ANCHO, suelo_h))
        pygame.draw.line(pantalla, self.LINEA_ALT,
                         (0, SUELO_Y), (ANCHO, SUELO_Y), 3)

        # ── Líneas de velocidad en el suelo ─────────────────────
        esp = 80
        for i in range(-1, ANCHO // esp + 2):
            x = int(i * esp - self._off_suelo)
            # línea larga
            pygame.draw.line(pantalla, self.LINEA_COL,
                             (x, SUELO_Y+10), (x+40, SUELO_Y+10), 2)
            # línea corta
            pygame.draw.line(pantalla, self.LINEA_COL,
                             (x+15, SUELO_Y+20), (x+38, SUELO_Y+20), 1)


# ── REFRESCO ─────────────────────────────────────────────────────

class Refresco:
    def __init__(self, x, y_suelo, row=0):
        self.x       = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.valor   = REFRESCO_VALOR_BASE
        self.imagen  = _cargar_sprite("assets/refresco.png", OBJ_SIZE)

    def update(self, v): self.x -= v

    def dibujar(self, pantalla):
        y = self._y_base - OBJ_SIZE
        if self.imagen:
            pantalla.blit(self.imagen, (int(self.x), y))
        else:
            bx = int(self.x); s = OBJ_SIZE
            # Lata pixel-art
            pygame.draw.rect(pantalla, (180,50,50), (bx+s//4, y+4, s//2, s-8))
            pygame.draw.rect(pantalla, (220,80,80), (bx+s//4+3, y+7, s//2-6, 8))
            pygame.draw.rect(pantalla, BLANCO,      (bx+s//4, y+4, s//2, s-8), 2)

    def get_rect(self):
        ox = int(self.x) + (OBJ_SIZE - OBJ_HB_W)//2
        return pygame.Rect(ox, self._y_base - OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ── SIERRA ───────────────────────────────────────────────────────

class Sierra:
    def __init__(self, x, y_suelo, row=0):
        self.x       = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.angulo  = 0.0
        self.imagen  = _cargar_sprite("assets/sierra.png", OBJ_SIZE)

    def update(self, v):
        self.x -= v
        self.angulo = (self.angulo + 5) % 360

    def dibujar(self, pantalla):
        y = self._y_base - OBJ_SIZE
        if self.imagen:
            rot   = pygame.transform.rotate(self.imagen, -self.angulo)
            off_x = (rot.get_width()  - OBJ_SIZE)//2
            off_y = (rot.get_height() - OBJ_SIZE)//2
            pantalla.blit(rot, (int(self.x)-off_x, y-off_y))
        else:
            cx = int(self.x)+OBJ_SIZE//2; cy = y+OBJ_SIZE//2
            r  = OBJ_SIZE//2 - 4
            pygame.draw.circle(pantalla, GRIS, (cx,cy), r)
            for i in range(10):
                a  = math.radians(self.angulo + i*36)
                dx = cx + math.cos(a)*(r+7)
                dy = cy + math.sin(a)*(r+7)
                pygame.draw.polygon(pantalla, GRIS_OSCURO, [
                    (int(cx+math.cos(a-0.22)*r), int(cy+math.sin(a-0.22)*r)),
                    (int(cx+math.cos(a+0.22)*r), int(cy+math.sin(a+0.22)*r)),
                    (int(dx), int(dy)),
                ])

    def get_rect(self):
        ox = int(self.x) + (OBJ_SIZE - OBJ_HB_W)//2
        return pygame.Rect(ox, self._y_base - OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ── CAJA ─────────────────────────────────────────────────────────
#  row=0 → suelo | row≥1 → elevada
#  Saltar encima funciona para cualquier row

class Caja:
    def __init__(self, x, y_suelo, row=0):
        self.x       = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.row     = row
        self.imagen  = _cargar_sprite("assets/caja.png", OBJ_SIZE)

    def update(self, v): self.x -= v

    def dibujar(self, pantalla):
        y  = self._y_base - OBJ_SIZE
        bx = int(self.x); s = OBJ_SIZE
        if self.imagen:
            pantalla.blit(self.imagen, (bx, y))
        else:
            pygame.draw.rect(pantalla, MARRON,        (bx,y,s,s))
            pygame.draw.rect(pantalla, (100,60,20),   (bx,y,s,s), 3)
            pygame.draw.line(pantalla, (100,60,20), (bx+4,y+4), (bx+s-4,y+s-4), 2)
            pygame.draw.line(pantalla, (100,60,20), (bx+s-4,y+4), (bx+4,y+s-4), 2)
            pygame.draw.rect(pantalla, (180,110,50), (bx+4,y+4,s-8,s-8), 1)

    def get_rect(self):
        ox = int(self.x) + (OBJ_SIZE - OBJ_HB_W)//2
        return pygame.Rect(ox, self._y_base - OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ══════════════════════════════════════════════
#  SISTEMA DE PATRONES
#
#  Cada celda: {'tipo': 'B'|'S'|'M', 'col': int, 'row': int}
#  col → posición horizontal (0 = borde derecho + offset)
#  row → altura desde suelo (0 = suelo, 1 = 1 caja arriba)
# ══════════════════════════════════════════════

def _B(c, r=0): return {'tipo':'B','col':c,'row':r}
def _S(c, r=0): return {'tipo':'S','col':c,'row':r}
def _M(c, r=1): return {'tipo':'M','col':c,'row':r}

_G = OBJ_SIZE + 2   # gap entre columnas

# ─── FÁCIL ────────────────────────────────────────────────────────
EASY = [
    [_S(0)],
    [_S(0), _S(1)],
    [_B(0)],
    [_B(0), _B(1)],
    [_B(0), _B(0,1)],                          # torre 2
    [_M(0), _S(2)],
    [_M(0), _B(2)],
    [_B(0), _M(0,2)],
    [_S(0), _M(2)],
]

# ─── NORMAL ────────────────────────────────────────────────────────
NORMAL = EASY + [
    [_S(0), _S(1), _S(2)],                     # 3 sierras fila
    [_B(0), _B(0,1), _B(0,2)],                 # torre 3
    [_B(0), _B(1), _B(2)],                     # 3 cajas fila
    [_B(0), _S(1), _B(2)],                     # sierra entre cajas
    [_S(0,1), _S(1,1)],                        # 2 sierras elevadas (agacharse)
    [_B(0), _B(0,1), _B(1)],                   # L pequeña
    [_B(0), _B(0,1), _B(0,2), _S(0,3)],        # torre+sierra encima
    [_M(0), _M(1,2), _M(2)],                   # monedas arco
    [_S(0), _S(2), _S(4)],                     # sierras alternadas
    [_B(0), _B(2)],                            # 2 cajas separadas
]

# ─── DIFÍCIL ───────────────────────────────────────────────────────
HARD = NORMAL + [
    # Fila larga de cajas
    [_B(0),_B(1),_B(2),_B(3),_B(4)],
    # Torre 4
    [_B(0),_B(0,1),_B(0,2),_B(0,3)],
    # L grande: torre 3 + fila 4
    [_B(0,3),_B(0,2),_B(0,1),_B(0),_B(1),_B(2),_B(3)],
    # L invertida
    [_B(3,3),_B(3,2),_B(3,1),_B(0),_B(1),_B(2),_B(3)],
    # Torre + sierra al costado
    [_B(0),_B(0,1),_B(0,2),_B(0,3),_S(2)],
    # Arco de cajas
    [_B(0),_B(0,1),_B(1,2),_B(2,2),_B(3,2),_B(4,1),_B(4)],
    # 3 sierras elevadas (pasar agachado)
    [_S(0,2),_S(1,2),_S(2,2)],
    # Escalera ascendente
    [_B(0),_B(1),_B(1,1),_B(2,1),_B(2,2)],
    # Escalera descendente
    [_B(0,2),_B(0,1),_B(1,1),_B(1),_B(2)],
    # Torre+sierras apiladas al lado
    [_S(0),_S(0,1)],
    # L + sierras en el paso
    [_B(0,2),_B(0,1),_B(0),_B(1),_B(2),_B(3),_S(5)],
    # Sierra entre torres
    [_B(0),_B(0,1),_S(2),_B(4),_B(4,1)],
    # Combinado complejo
    [_B(0),_S(1),_B(2),_S(3),_B(4)],
    # Monedas difíciles de alcanzar
    [_B(0),_B(0,1),_M(0,3),_S(3)],
]


def seleccionar_patron(velocidad):
    if velocidad < 9.5:
        return random.choice(EASY)
    elif velocidad < 13.0:
        return random.choice(NORMAL)
    else:
        return random.choice(HARD)


def spawn_patron(patron, y_suelo):
    obstaculos = []; monedas = []
    for c in patron:
        x   = ANCHO + c['col'] * _G
        row = c['row']
        if   c['tipo'] == 'B': obstaculos.append(Caja(x,    y_suelo, row))
        elif c['tipo'] == 'S': obstaculos.append(Sierra(x,  y_suelo, row))
        elif c['tipo'] == 'M': monedas.append(   Refresco(x, y_suelo, row))
    return obstaculos, monedas
