# ============================================
# CONFIG.PY - CONFIGURACIÓN PRINCIPAL
# ============================================

import pygame

# Pantalla
ANCHO = 1920
ALTO = 1080
FPS = 60
SUELO_Y = 920          # Ajustado para que los sprites de 64px apoyen bien
TITULO = "Chande-Run"

# Colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,50,50)
VERDE = (50,255,50)
AZUL = (50,50,255)
AMARILLO = (255,255,50)
MORADO = (150,50,255)
NARANJA = (255,150,50)
CELESTE = (50,200,255)
ROSA = (255,100,200)
MARRON = (139,69,19)
GRIS = (128,128,128)
GRIS_OSCURO = (64,64,64)
DORADO = (255,215,0)
PLATA = (192,192,192)

# Física (ajustada para sprites de 64px)
GRAVEDAD = 0.6
VEL_SALTO_MIN = -12
VEL_SALTO_MAX = -22
VELOCIDAD_BASE = 6
VEL_MAX = 20

# Tamaños de sprites (todos 64x64)
SPRITE_SIZE = 64

# Economía
REFRESCO_VALOR_BASE = 1
PRECIO_POWERUPS = {'segundo_intento': 50}

# Logros (solo recompensa en refrescos)
LOGROS = {
    'primer_paso': {'nombre': 'Primer Paso', 'desc': 'Juega tu primera partida', 'refrescos': 10},
    'maratonista': {'nombre': 'Maratonista', 'desc': 'Corre 2000 puntos', 'refrescos': 50},
    'saltarin': {'nombre': 'Saltarín', 'desc': 'Salta 150 veces', 'refrescos': 30},
    'coleccionista': {'nombre': 'Coleccionista', 'desc': 'Consigue 200 refrescos', 'refrescos': 100},
    'esquivador': {'nombre': 'Esquivador', 'desc': 'Esquiva 100 obstáculos seguidos', 'refrescos': 200},
    'noctambulo': {'nombre': 'Noctámbulo', 'desc': 'Juega de noche', 'refrescos': 20},
    'millonario': {'nombre': 'Millonario', 'desc': 'Consigue 2000 refrescos', 'refrescos': 500},
    'veloz': {'nombre': 'Veloz', 'desc': 'Alcanza velocidad 20', 'refrescos': 150}
}