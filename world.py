# ============================================
# world.py
# ============================================
import pygame, math, os, random
from config import *


def _load_img(path, size):
    if os.path.exists(path):
        try:
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), (size, size))
        except Exception as e:
            print(f"Warn {path}: {e}")
    return None


# ── FONDO PARALLAX ───────────────────────────────────────────────

class Fondo:
    # Colores del suelo
    GROUND_MAIN  = ( 42,  40,  36)
    GROUND_MID   = ( 52,  50,  44)
    GROUND_EDGE  = (130, 120, 100)
    GROUND_TILE  = ( 62,  58,  50)
    SPEED_LINE   = ( 80,  74,  62)
    TILE_W       = 80

    def __init__(self, archivo="assets/fondo.jpg"):
        self._off_bg    = 0.0
        self._off_mid   = 0.0
        self._off_tile  = 0.0

        self._img = None
        if os.path.exists(archivo):
            try:
                img = pygame.image.load(archivo)
                img = img.convert_alpha() if archivo.endswith('.png') else img.convert()
                self._img = pygame.transform.scale(img, (ANCHO, ALTO))
                print("OK Fondo")
            except Exception as e:
                print(f"Warn fondo: {e}")
        if not self._img:
            s = pygame.Surface((ANCHO, ALTO)); s.fill((40, 55, 90))
            self._img = s

        self._mid = self._gen_mid()

    def _gen_mid(self):
        s   = pygame.Surface((ANCHO*2, ALTO), pygame.SRCALPHA)
        rng = random.Random(42)
        for _ in range(22):
            x = rng.randint(0, ANCHO*2)
            y = rng.randint(20, SUELO_Y - 50)
            w = rng.randint(80, 280); h = rng.randint(12, 40)
            a = rng.randint(8, 22)
            sf = pygame.Surface((w, h), pygame.SRCALPHA)
            sf.fill((255, 255, 255, a)); s.blit(sf, (x, y))
        return s

    def update(self, vel):
        self._off_bg   = (self._off_bg   + vel * 0.10) % ANCHO
        self._off_mid  = (self._off_mid  + vel * 0.30) % (ANCHO*2)
        self._off_tile = (self._off_tile + vel * 0.92) % self.TILE_W

    def dibujar(self, pantalla):
        # Fondo
        ox = int(self._off_bg)
        pantalla.blit(self._img, (-ox, 0))
        pantalla.blit(self._img, (ANCHO - ox, 0))

        # Capa media parallax
        ox2 = int(self._off_mid)
        pantalla.blit(self._mid, (-ox2, 0))
        pantalla.blit(self._mid, (ANCHO*2 - ox2, 0))

        self._dibujar_suelo(pantalla)

    def _dibujar_suelo(self, pantalla):
        gh = ALTO - SUELO_Y

        # ── Capa 1: relleno principal ────────────────────────────
        pygame.draw.rect(pantalla, self.GROUND_MAIN, (0, SUELO_Y, ANCHO, gh))

        # ── Capa 2: borde superior (plataforma gruesa) ───────────
        # Línea de resalte principal (brillante)
        pygame.draw.line(pantalla, self.GROUND_EDGE,
                         (0, SUELO_Y), (ANCHO, SUELO_Y), 3)
        # Línea de profundidad (más oscura, 4px abajo)
        pygame.draw.line(pantalla, self.GROUND_TILE,
                         (0, SUELO_Y + 4), (ANCHO, SUELO_Y + 4), 2)

        # ── Capa 3: líneas de velocidad verticales ───────────────
        tw = self.TILE_W
        off = int(self._off_tile)
        for i in range(-1, ANCHO // tw + 2):
            x = i * tw - off
            # Línea larga
            pygame.draw.line(pantalla, self.SPEED_LINE,
                             (x, SUELO_Y + 8), (x + 44, SUELO_Y + 8), 2)
            # Línea corta (segunda banda)
            pygame.draw.line(pantalla, self.SPEED_LINE,
                             (x + 18, SUELO_Y + 18), (x + 42, SUELO_Y + 18), 1)
            # Punto de acento
            if i % 2 == 0:
                pygame.draw.line(pantalla, self.GROUND_EDGE,
                                 (x, SUELO_Y + 26), (x + 20, SUELO_Y + 26), 1)

        # ── Capa 4: rejilla horizontal (filas) ───────────────────
        for row_y in range(SUELO_Y + 12, ALTO, 16):
            pygame.draw.line(pantalla, self.GROUND_MID,
                             (0, row_y), (ANCHO, row_y), 1)


# ── REFRESCO ─────────────────────────────────────────────────────

class Refresco:
    def __init__(self, x, y_suelo, row=0):
        self.x = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.valor   = REFRESCO_VALOR_BASE
        self._img    = _load_img("assets/refresco.png", OBJ_SIZE)

    def update(self, v): self.x -= v

    def dibujar(self, pantalla):
        y = self._y_base - OBJ_SIZE
        if self._img:
            pantalla.blit(self._img, (int(self.x), y))
        else:
            bx=int(self.x); s=OBJ_SIZE
            pygame.draw.rect(pantalla,(180,50,50),(bx+s//4,y+4,s//2,s-8))
            pygame.draw.rect(pantalla,(220,80,80),(bx+s//4+3,y+7,s//2-6,8))
            pygame.draw.rect(pantalla,BLANCO,     (bx+s//4,y+4,s//2,s-8),2)

    def get_rect(self):
        return pygame.Rect(int(self.x)+(OBJ_SIZE-OBJ_HB_W)//2,
                           self._y_base-OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ── SIERRA ───────────────────────────────────────────────────────

class Sierra:
    def __init__(self, x, y_suelo, row=0):
        self.x = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.angulo  = 0.0
        self._img    = _load_img("assets/sierra.png", OBJ_SIZE)

    def update(self, v):
        self.x -= v; self.angulo = (self.angulo + 5) % 360

    def dibujar(self, pantalla):
        y = self._y_base - OBJ_SIZE
        if self._img:
            rot = pygame.transform.rotate(self._img, -self.angulo)
            ox  = (rot.get_width()-OBJ_SIZE)//2
            oy  = (rot.get_height()-OBJ_SIZE)//2
            pantalla.blit(rot, (int(self.x)-ox, y-oy))
        else:
            cx=int(self.x)+OBJ_SIZE//2; cy=y+OBJ_SIZE//2; r=OBJ_SIZE//2-4
            pygame.draw.circle(pantalla,GRIS,(cx,cy),r)
            for i in range(10):
                a=math.radians(self.angulo+i*36)
                dx=cx+math.cos(a)*(r+7); dy=cy+math.sin(a)*(r+7)
                pygame.draw.polygon(pantalla,GRIS_OSCURO,[
                    (int(cx+math.cos(a-.22)*r),int(cy+math.sin(a-.22)*r)),
                    (int(cx+math.cos(a+.22)*r),int(cy+math.sin(a+.22)*r)),
                    (int(dx),int(dy))])

    def get_rect(self):
        return pygame.Rect(int(self.x)+(OBJ_SIZE-OBJ_HB_W)//2,
                           self._y_base-OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ── CAJA ─────────────────────────────────────────────────────────

class Caja:
    def __init__(self, x, y_suelo, row=0):
        self.x = float(x)
        self._y_base = y_suelo - row * OBJ_SIZE
        self.row  = row
        self._img = _load_img("assets/caja.png", OBJ_SIZE)

    def update(self, v): self.x -= v

    def dibujar(self, pantalla):
        y=self._y_base-OBJ_SIZE; bx=int(self.x); s=OBJ_SIZE
        if self._img:
            pantalla.blit(self._img,(bx,y))
        else:
            pygame.draw.rect(pantalla,MARRON,      (bx,y,s,s))
            pygame.draw.rect(pantalla,(100,60,20), (bx,y,s,s),3)
            pygame.draw.line(pantalla,(100,60,20),(bx+4,y+4),(bx+s-4,y+s-4),2)
            pygame.draw.line(pantalla,(100,60,20),(bx+s-4,y+4),(bx+4,y+s-4),2)
            pygame.draw.rect(pantalla,(180,110,50),(bx+4,y+4,s-8,s-8),1)

    def get_rect(self):
        return pygame.Rect(int(self.x)+(OBJ_SIZE-OBJ_HB_W)//2,
                           self._y_base-OBJ_HB_H, OBJ_HB_W, OBJ_HB_H)


# ══════════════════════════════════════════════════════════════════
#  SISTEMA DE SETS / PATRONES
#
#  Un "set" es una lista de celdas:
#    _B(col, row) = Caja
#    _S(col, row) = Sierra
#    _M(col, row) = Moneda/refresco (row=1 = a 1 bloque del suelo)
#
#  col : columna 0..N  (0=primer objeto a la derecha del borde)
#  row : 0=suelo, 1=sobre 1 caja, 2=sobre 2 cajas, etc.
#
#  MECÁNICAS:
#    • Caja row=0   → saltar encima o saltar por encima
#    • Caja row≥1   → plataforma flotante: saltar encima o agacharse por debajo
#    • Sierra       → siempre letal, solo esquivar
#    • "Corredor"   → patrón vacío con solo 1 caja para no aburrirse
# ══════════════════════════════════════════════════════════════════

def _B(c,r=0): return {'t':'B','c':c,'r':r}
def _S(c,r=0): return {'t':'S','c':c,'r':r}
def _M(c,r=1): return {'t':'M','c':c,'r':r}

_G = OBJ_SIZE + 2    # paso entre columnas (px)

# ══════════════════════════════════
#  POOLS POR DIFICULTAD
# ══════════════════════════════════

# ─── INTRO (score 0-800) ──── una sola caja / sierra, muy espaciado
INTRO = [
    [_S(0)],
    [_B(0)],
    [_S(0)],
    [_B(0)],
    [_B(0),_B(1)],
    [_S(0),_M(2)],
    [_B(0),_M(0,2)],
]

# ─── EASY (score 800-2500) ─── pares y torres pequeñas
EASY = [
    [_S(0),_S(1)],
    [_B(0),_B(1)],
    [_B(0),_B(0,1)],                  # torre 2
    [_S(0),_M(2)],
    [_B(0),_M(1),_S(3)],
    [_S(0),_S(2)],
    [_B(0),_S(2),_M(4)],
    [_M(0),_B(2),_M(4)],
    [_B(0),_B(1),_M(1,2)],
    [_S(0),_S(1),_S(2)],              # 3 sierras fila (img original)
]

# ─── NORMAL (score 2500-6000)
NORMAL = EASY + [
    # Torre 3
    [_B(0),_B(0,1),_B(0,2)],
    # Fila 3
    [_B(0),_B(1),_B(2)],
    # Sierra entre cajas
    [_B(0),_S(1),_B(2)],
    # 2 sierras elevadas (agacharse)
    [_S(0,1),_S(1,1)],
    # L pequeña
    [_B(0),_B(0,1),_B(1)],
    # Torre + sierra encima
    [_B(0),_B(0,1),_B(0,2),_S(0,3)],
    # Monedas arco
    [_M(0),_M(1,2),_M(2)],
    # Escalera corta
    [_B(0),_B(1),_B(1,1)],
    # Fila flotante baja (pasar debajo agachado)
    [_B(0,1),_B(1,1),_B(2,1)],
    # Sierras alternadas
    [_S(0),_S(2),_S(4)],
    # Combo tierra+aire
    [_B(0),_S(2,1),_B(4)],
]

# ─── HARD (score 6000-12000) ─── sets inspirados en las fotos
HARD = NORMAL + [
    # ── Fila de 5 (foto 3 horizontal) ─────────────────────────
    [_B(0),_B(1),_B(2),_B(3),_B(4)],

    # ── Torre 4 (foto 1 — jugador pasa agachado debajo) ───────
    # El jugador puede agacharse y pasar si la caja inferior está en row=1
    [_B(0,1),_B(0,2),_B(0,3),_B(0,4)],

    # ── Torre 4 en suelo (foto 1 — saltar encima) ─────────────
    [_B(0),_B(0,1),_B(0,2),_B(0,3)],

    # ── L GRANDE (foto 4) ─────────────────────────────────────
    #  □
    #  □
    #  □
    #  □ □ □ □
    [_B(0,3),_B(0,2),_B(0,1),_B(0),_B(1),_B(2),_B(3)],

    # ── DOBLE PLATAFORMA ESCALONADA (foto 2) ──────────────────
    #  Plataforma baja row=1 (3 cajas) + plataforma alta row=2 (4 cajas)
    #  El jugador puede correr debajo, saltar entre plataformas
    [_B(0,1),_B(1,1),_B(2,1),  _B(4,2),_B(5,2),_B(6,2),_B(7,2)],

    # ── TORRE + SIERRA ENCIMA (foto 3) ────────────────────────
    [_B(0),_B(0,1),_B(0,2),_S(0,3)],

    # ── L INVERTIDA ───────────────────────────────────────────
    [_B(0),_B(1),_B(2),_B(3),_B(3,1),_B(3,2),_B(3,3)],

    # ── ARCO (foto 14 original) ───────────────────────────────
    [_B(0),_B(0,1),_B(1,2),_B(2,2),_B(3,2),_B(4,1),_B(4)],

    # ── Escalera ascendente ───────────────────────────────────
    [_B(0),_B(1),_B(1,1),_B(2,1),_B(2,2)],

    # ── Escalera descendente ──────────────────────────────────
    [_B(0,2),_B(0,1),_B(1,1),_B(1),_B(2)],

    # ── 2 sierras apiladas (combo mortal) ─────────────────────
    [_S(0),_S(0,1)],

    # ── Plataforma flotante + sierra abajo ────────────────────
    [_B(0,2),_B(1,2),_B(2,2), _S(1)],

    # ── Fila alta + combo ─────────────────────────────────────
    [_B(0,2),_B(1,2),_B(2,2), _S(4), _S(4,1)],
]

# ─── EXTREME (score 12000+)
EXTREME = HARD + [
    # ── L grande + sierras ────────────────────────────────────
    [_B(0,3),_B(0,2),_B(0,1),_B(0),_B(1),_B(2),_B(3),_S(5),_S(5,1)],

    # ── Torre 4 + fila + monedas bonus ────────────────────────
    [_B(0),_B(0,1),_B(0,2),_B(0,3),_B(1),_B(2),_M(1,4)],

    # ── Zig-zag sierras ───────────────────────────────────────
    [_S(0),_S(1,1),_S(2),_S(3,1),_S(4)],

    # ── Combo máximo: L + sierra + plataforma ─────────────────
    [_B(0,2),_B(0,1),_B(0),_B(1),_B(2), _S(4), _B(6,1),_B(7,1)],

    # ── Doble torre con gap ───────────────────────────────────
    [_B(0),_B(0,1),_B(0,2), _B(4),_B(4,1),_B(4,2)],
]

# ─── CORREDOR (aparece ocasionalmente para dar respiro) ───────────
CORREDOR = [
    [_B(0)],
    [_S(0)],
    [_M(0),_M(1)],
    [_B(0),_M(1,2)],
    [],   # completamente vacío (rarísimo)
]


# ── Función principal de selección ───────────────────────────────
#
#  En TODAS las franjas hay un 10% de EXTREME y 15% de HARD como
#  sorpresa (el "spike" de dificultad pedido).
#  El 20% de NORMAL también aparece en franjas bajas para dar variedad.
#  El resto del porcentaje lo ocupa el pool propio de cada franja.
#
#  Tabla de probabilidades por franja:
#
#  score       CORREDOR  EXTREME  HARD   NORMAL  propio
#  ─────────── ────────  ───────  ─────  ──────  ──────
#  0 – 800       8 %      10 %    15 %   20 %    47 % INTRO
#  800 – 2500    8 %      10 %    15 %   20 %    47 % EASY
#  2500 – 6000   8 %      10 %    15 %   20 %    47 % NORMAL
#  6000 – 9000   8 %      10 %    15 %    —      67 % HARD
#  9000+         8 %      10 %     —      —      82 % EXTREME

def seleccionar_patron(score):
    # ── Corredor de descanso (8 %) ───────────────────────────────
    if random.random() < 0.08:
        return random.choice(CORREDOR)

    r = random.random()

    # ── Spikes universales (siempre disponibles) ─────────────────
    if r < 0.10:                      # 10 % → EXTREME
        return random.choice(EXTREME)
    if r < 0.25:                      # 15 % → HARD
        return random.choice(HARD)

    # ── 20 % → NORMAL (aplica a todas las franjas bajas) ─────────
    if r < 0.45 and score < 6000:
        return random.choice(NORMAL)

    # ── Pool propio de la franja ──────────────────────────────────
    if score < 800:
        return random.choice(INTRO)
    elif score < 2500:
        return random.choice(EASY)
    elif score < 6000:
        return random.choice(NORMAL)
    elif score < 9000:
        return random.choice(HARD)
    else:
        return random.choice(EXTREME)


def spawn_patron(patron, y_suelo):
    obs = []; mon = []
    for c in patron:
        x   = ANCHO + c['c'] * _G
        row = c['r']
        if   c['t'] == 'B': obs.append(Caja(x,     y_suelo, row))
        elif c['t'] == 'S': obs.append(Sierra(x,   y_suelo, row))
        elif c['t'] == 'M': mon.append(Refresco(x, y_suelo, row))
    return obs, mon


def spawn_gap(score):
    """Devuelve (min_frames, max_frames) para el gap de spawn."""
    if   score < 1000:  return 120, 160
    elif score < 3000:  return 100, 140
    elif score < 6000:  return  85, 120
    elif score < 10000: return  70, 100
    else:               return  58,  85
