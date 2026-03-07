# ============================================
# systems.py
# ============================================
import pygame
from config import *


class SistemaRefrescos:
    def __init__(self):
        self.refrescos = 0; self.refrescos_totales = 0

    def añadir(self, n): self.refrescos += n; self.refrescos_totales += n

    def gastar(self, n):
        if self.refrescos >= n: self.refrescos -= n; return True
        return False


class SistemaLogros:
    _OBJ = {'primer_paso':1,'maratonista':2000,'saltarin':150,
            'coleccionista':200,'esquivador':100,'veloz':1}

    def __init__(self):
        self.logros = {k: {'completado':False,'progreso':0,
                           'objetivo':self._OBJ.get(k,1)} for k in LOGROS}
        self.notifs = []

    def actualizar(self, key, inc=1):
        l = self.logros.get(key)
        if l and not l['completado']:
            l['progreso'] += inc
            if l['progreso'] >= l['objetivo']:
                l['completado'] = True
                self.notifs.append({'logro':key,'tiempo':pygame.time.get_ticks()})
                return True
        return False

    def dibujar_notificaciones(self, pantalla, fuente):
        ahora = pygame.time.get_ticks()
        for n in self.notifs[:]:
            if ahora - n['tiempo'] < 3000:
                key = n['logro']
                txt = fuente.render(
                    f"* {LOGROS[key]['nombre']}  +{LOGROS[key]['refrescos']}",
                    True, DORADO)
                x = ANCHO//2 - txt.get_width()//2
                pygame.draw.rect(pantalla, UI_PANEL,
                                 (x-12,90,txt.get_width()+24,txt.get_height()+8))
                pygame.draw.rect(pantalla, UI_BORDE_DORADO,
                                 (x-12,90,txt.get_width()+24,txt.get_height()+8), 2)
                pantalla.blit(txt, (x,94))
            else:
                self.notifs.remove(n)
