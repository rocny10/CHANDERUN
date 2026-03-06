# ============================================
# systems.py - COMPLETO
# ============================================
import pygame
from config import *

class SistemaRefrescos:
    def __init__(self):
        self.refrescos = 0
        self.refrescos_totales = 0
    def añadir(self, cantidad):
        self.refrescos += cantidad
        self.refrescos_totales += cantidad
    def gastar(self, cantidad):
        if self.refrescos >= cantidad:
            self.refrescos -= cantidad
            return True
        return False
    def dibujar(self, pantalla, x, y):
        fuente = pygame.font.Font(None,30)
        texto = fuente.render(f"🥤 {self.refrescos}", True, DORADO)
        pantalla.blit(texto, (x,y))

class SistemaLogros:
    def __init__(self):
        self.logros = {}
        for key in LOGROS:
            self.logros[key] = {'completado': False, 'progreso': 0, 'objetivo': self._objetivo(key)}
        self.notificaciones = []
    def _objetivo(self, key):
        obs = {'primer_paso':1,'maratonista':2000,'saltarin':150,'coleccionista':200,
               'esquivador':100,'noctambulo':1,'millonario':2000,'veloz':1}
        return obs.get(key,1)
    def actualizar(self, key, inc=1):
        if key in self.logros and not self.logros[key]['completado']:
            self.logros[key]['progreso'] += inc
            if self.logros[key]['progreso'] >= self.logros[key]['objetivo']:
                self.logros[key]['completado'] = True
                self.notificaciones.append({'logro':key, 'tiempo':pygame.time.get_ticks()})
                return True
        return False
    def obtener_recompensa(self, key):
        return LOGROS[key]['refrescos']
    def dibujar_notificaciones(self, pantalla):
        ahora = pygame.time.get_ticks()
        for n in self.notificaciones[:]:
            if ahora - n['tiempo'] < 3000:
                key = n['logro']
                f = pygame.font.Font(None,24)
                t = f.render(f"🏆 {LOGROS[key]['nombre']} +{LOGROS[key]['refrescos']}🥤", True, DORADO)
                pantalla.blit(t, (ANCHO//2-150,100))
            else:
                self.notificaciones.remove(n)

class Tienda:
    def __init__(self, sistema_refrescos):
        self.sis_ref = sistema_refrescos
        self.powerups = []
    def comprar(self, nombre):
        precio = PRECIO_POWERUPS.get(nombre,0)
        if self.sis_ref.gastar(precio):
            self.powerups.append(nombre)
            return True
        return False
    def usar(self, nombre):
        if nombre in self.powerups:
            self.powerups.remove(nombre)
            return True
        return False
    def tiene(self, nombre):
        return nombre in self.powerups