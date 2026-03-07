# ============================================
# config.py
# ============================================

TITULO = "Chande-Run"
ANCHO  = 1280
ALTO   = 720
FPS    = 60

# ─────────────────────────────────────────────────────────────────
#  TAMAÑOS
#  PLAYER_SIZE : sprite del personaje (px)
#  OBJ_SIZE    : cajas / sierras / refrescos
#  SUELO_Y     : posición Y de los PIES del jugador
#
#  ► Para bajar el personaje 1 píxel: aumenta SUELO_Y en 1.
#    Ejemplo: SUELO_Y = 572  →  personaje 7px más abajo que 565
#    La línea del suelo se dibuja exactamente en SUELO_Y,
#    así que subir SUELO_Y acerca los pies a esa línea.
# ─────────────────────────────────────────────────────────────────
PLAYER_SIZE = 100
OBJ_SIZE    = 60
SUELO_Y     = 560     # ← sube este valor para bajar el personaje

# Hitbox jugador
HITBOX_W = int(PLAYER_SIZE * 0.48)
HITBOX_H = int(PLAYER_SIZE * 0.78)

# Hitbox objetos
OBJ_HB_W = int(OBJ_SIZE * 0.60)
OBJ_HB_H = int(OBJ_SIZE * 0.68)

# ─── Física ──────────────────────────────────────────────────────
GRAVEDAD        = 0.65
VEL_SALTO       = -17.5
VEL_SALTO_CORTE = -8.0

# Movimiento lateral
VEL_LATERAL = 2.8
X_MIN       = 140
X_MAX       = 360
X_INICIO    = 240

# ─── Velocidad ───────────────────────────────────────────────────
VELOCIDAD_BASE = 7.0
VEL_MAX        = 18.0
AUMENTO_VEL    = 0.3
INTERVALO_VEL  = 500

# ─── Spawn ───────────────────────────────────────────────────────
# Ajustado dinámicamente por puntuación en main.py
DIST_MIN_BASE = 100
DIST_MAX_BASE = 155

# ─── Assets ──────────────────────────────────────────────────────
FUENTE_TTF = "assets/font.ttf"

# ─── Skins ─────────────────────────────────────────────────────────
#  Chande (0): *_sheet.png   ← sin sufijo
#  Pelo   (1): *_sheet2.png
#  Arube  (2): *_sheet3.png
NOMBRE_SKIN = {0: "Chande", 1: "Pelo", 2: "Arube"}
PRECIO_SKIN = {0: 0,        1: 150,    2: 800}

# ─── PowerUps ────────────────────────────────────────────────────
PRECIO_SEGUNDO_INTENTO = 700

# ─── Coleccionables ──────────────────────────────────────────────
REFRESCO_VALOR_BASE = 1

# ─── Colores base ────────────────────────────────────────────────
BLANCO      = (255, 255, 255)
NEGRO       = (  0,   0,   0)
ROJO        = (220,  50,  50)
DORADO      = (255, 210,   0)
GRIS        = (160, 160, 160)
GRIS_OSCURO = ( 60,  60,  60)
MARRON      = (160,  90,  40)
AZUL        = ( 60, 140, 220)
VERDE       = ( 50, 200,  80)

# ─── Paleta Glass UI ─────────────────────────────────────────────
# Tints para los paneles de vidrio
GLASS_BLUE    = (100, 160, 255)
GLASS_DARK    = ( 20,  30,  60)
GLASS_CYAN    = (  0, 210, 255)
GLASS_GREEN   = ( 40, 220, 100)
GLASS_RED     = (220,  60,  60)
GLASS_GOLD    = (255, 200,  60)
GLASS_PURPLE  = (160,  80, 255)
GLASS_WHITE   = (220, 235, 255)

# ─── Logros ──────────────────────────────────────────────────────
LOGROS = {
    'primer_paso':   {'nombre': 'Primer Paso',   'refrescos':  5},
    'maratonista':   {'nombre': 'Maratonista',   'refrescos': 30},
    'saltarin':      {'nombre': 'Saltarin',      'refrescos': 20},
    'coleccionista': {'nombre': 'Coleccionista', 'refrescos': 25},
    'esquivador':    {'nombre': 'Esquivador',    'refrescos': 15},
    'veloz':         {'nombre': 'Veloz',         'refrescos': 20},
}
