# ============================================
# config.py
# ============================================

TITULO = "Chande-Run"
ANCHO  = 1280
ALTO   = 720
FPS    = 60

# ─────────────────────────────────────────────────────────────────
#  TAMAÑOS  ← cambia estos valores de forma independiente
#
#  PLAYER_SIZE : tamaño del sprite del PERSONAJE (px)
#                64 = pequeño | 80 = normal | 96 = grande
#
#  OBJ_SIZE    : tamaño de OBJETOS (cajas, sierras, refrescos)
#                Independiente del personaje
#
#  SUELO_Y     : posición Y de los pies del personaje
# ─────────────────────────────────────────────────────────────────
PLAYER_SIZE = 80
OBJ_SIZE    = 72
SUELO_Y     = 565

# Alias — NO tocar
SPRITE_SIZE = PLAYER_SIZE          # compatibilidad interna del jugador

# Hitbox jugador (más pequeña que el sprite para colisiones justas)
HITBOX_W = int(PLAYER_SIZE * 0.50)
HITBOX_H = int(PLAYER_SIZE * 0.80)

# Hitbox objetos
OBJ_HB_W = int(OBJ_SIZE * 0.62)
OBJ_HB_H = int(OBJ_SIZE * 0.70)

# ─── Física ──────────────────────────────────────────────────────
GRAVEDAD        = 0.65
VEL_SALTO       = -17.5
VEL_SALTO_CORTE = -8.0

# Movimiento lateral
VEL_LATERAL = 2.8
X_MIN       = 160
X_MAX       = 360
X_INICIO    = 240

# ─── Velocidad ───────────────────────────────────────────────────
VELOCIDAD_BASE = 7.0
VEL_MAX        = 18.0
AUMENTO_VEL    = 0.4
INTERVALO_VEL  = 600

# ─── Spawn ───────────────────────────────────────────────────────
DIST_MIN_PATRON = 95
DIST_MAX_PATRON = 170

# ─── Assets ──────────────────────────────────────────────────────
FUENTE_TTF = "assets/font.ttf"

# ─── Skins ───────────────────────────────────────────────────────
NOMBRE_SKIN  = {0: "Chande", 1: "Pelo"}
PRECIO_SKIN_2 = 150

# ─── PowerUps ────────────────────────────────────────────────────
PRECIO_SEGUNDO_INTENTO = 700

# ─── Coleccionables ──────────────────────────────────────────────
REFRESCO_VALOR_BASE = 1

# ─── Colores ─────────────────────────────────────────────────────
BLANCO      = (255, 255, 255)
NEGRO       = (  0,   0,   0)
ROJO        = (220,  50,  50)
DORADO      = (255, 210,   0)
GRIS        = (160, 160, 160)
GRIS_OSCURO = ( 60,  60,  60)
MARRON      = (160,  90,  40)
AZUL        = ( 60, 140, 220)
VERDE       = ( 50, 200,  80)
NARANJA     = (230, 130,  30)

# UI pixel-art
UI_FONDO        = (  8,   8,  20)
UI_PANEL        = ( 16,  16,  36)
UI_PANEL2       = ( 24,  24,  52)
UI_BORDE        = ( 70,  70, 130)
UI_BORDE_DORADO = (190, 150,   0)
UI_TEXTO        = (200, 200, 220)
UI_ACENTO       = ( 80, 170, 255)
UI_ROJO         = (160,  35,  35)

# ─── Logros ──────────────────────────────────────────────────────
LOGROS = {
    'primer_paso':   {'nombre': 'Primer Paso',   'refrescos':  5},
    'maratonista':   {'nombre': 'Maratonista',   'refrescos': 30},
    'saltarin':      {'nombre': 'Saltarin',      'refrescos': 20},
    'coleccionista': {'nombre': 'Coleccionista', 'refrescos': 25},
    'esquivador':    {'nombre': 'Esquivador',    'refrescos': 15},
    'veloz':         {'nombre': 'Veloz',         'refrescos': 20},
}
