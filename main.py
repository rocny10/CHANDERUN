# ============================================
# main.py - VERSIÓN CORREGIDA CON MÉTODO EJECUTAR
# ============================================
import pygame
import sys
import random
import json
import os
from config import *
from world import FondoPersonalizado, Refresco, Sierra, Caja
from systems import SistemaRefrescos, SistemaLogros, Tienda
from player import Stickman
from ui import UI

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()

        self.fondo = FondoPersonalizado("assets/fondo.jpg")
        self.stickman = Stickman(300, SUELO_Y)
        self.refrescos_sys = SistemaRefrescos()
        self.logros = SistemaLogros()
        self.tienda = Tienda(self.refrescos_sys)
        self.ui = UI()

        self.estado = "MENU"
        self.puntuacion = 0
        self.velocidad = VELOCIDAD_BASE

        self.sierras = []
        self.cajas = []
        self.refrescos_lista = []

        self.contadores = {'sierra': 0, 'caja': 0, 'refresco': 0}
        self.botones_pausa = None
        self.botones_menu = None
        
        self.tiempo_menu = 0

        self.cargar()
        self.logros.actualizar('primer_paso')

    def cargar(self):
        try:
            if os.path.exists('data/save.json'):
                with open('data/save.json', 'r') as f:
                    d = json.load(f)
                    self.refrescos_sys.refrescos = d.get('refrescos', 0)
                    self.refrescos_sys.refrescos_totales = d.get('totales', 0)
        except:
            pass

    def guardar(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/save.json', 'w') as f:
                json.dump({
                    'refrescos': self.refrescos_sys.refrescos,
                    'totales': self.refrescos_sys.refrescos_totales
                }, f)
        except:
            pass

    def reiniciar(self):
        self.stickman = Stickman(300, SUELO_Y)
        self.puntuacion = 0
        self.velocidad = VELOCIDAD_BASE
        self.sierras.clear()
        self.cajas.clear()
        self.refrescos_lista.clear()
        self.contadores = {'sierra': 0, 'caja': 0, 'refresco': 0}

    def manejar_eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.guardar()
                pygame.quit()
                sys.exit()

            if self.estado == "MENU":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.estado = "JUGANDO"
                        self.reiniciar()
                    elif e.key == pygame.K_t:
                        self.estado = "TIENDA"
                    elif e.key == pygame.K_ESCAPE:
                        self.guardar()
                        pygame.quit()
                        sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and self.botones_menu:
                    mx, my = e.pos
                    jugar, tienda, salir = self.botones_menu
                    if jugar.collidepoint(mx, my):
                        self.estado = "JUGANDO"
                        self.reiniciar()
                    elif tienda.collidepoint(mx, my):
                        self.estado = "TIENDA"
                    elif salir.collidepoint(mx, my):
                        self.guardar()
                        pygame.quit()
                        sys.exit()

            elif self.estado == "JUGANDO":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.stickman.iniciar_carga()
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        self.stickman.agachar(True)
                    elif e.key == pygame.K_ESCAPE:
                        self.estado = "PAUSA"
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE:
                        self.stickman.ejecutar_salto()
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        self.stickman.agachar(False)

            elif self.estado == "PAUSA":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.estado = "JUGANDO"
                elif e.type == pygame.MOUSEBUTTONDOWN and self.botones_pausa:
                    mx, my = e.pos
                    cont, menu, salir = self.botones_pausa
                    if cont.collidepoint(mx, my):
                        self.estado = "JUGANDO"
                    elif menu.collidepoint(mx, my):
                        self.estado = "MENU"
                    elif salir.collidepoint(mx, my):
                        self.guardar()
                        pygame.quit()
                        sys.exit()

            elif self.estado == "TIENDA":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.estado = "MENU"
                    elif e.key == pygame.K_1:
                        if self.tienda.comprar('segundo_intento'):
                            self.stickman.aplicar_powerup('segundo_intento')

            elif self.estado == "GAME_OVER":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.estado = "JUGANDO"
                        self.reiniciar()
                    elif e.key == pygame.K_ESCAPE:
                        self.estado = "MENU"

    def posicion_valida(self, nuevo_rect, listas):
        for lst in listas:
            for obj in lst:
                if nuevo_rect.colliderect(obj.get_rect()):
                    return False
        return True

    def actualizar(self):
        if self.estado == "MENU":
            self.tiempo_menu += 1
            if self.tiempo_menu > 60:
                self.tiempo_menu = 0
            # Actualizar animación del stickman en menú
            self.stickman.actualizar_animacion()
            return

        if self.estado != "JUGANDO":
            return

        self.fondo.update(self.velocidad)
        self.stickman.update()
        self.puntuacion += 1

        # Cambio de animación según estado
        if not self.stickman.en_suelo:
            self.stickman.set_animacion("jump")
        else:
            self.stickman.set_animacion("idle")

        # Generar sierras
        if random.random() < PROB_SIERRA and self.contadores['sierra'] > 40:
            nueva = Sierra(ANCHO, SUELO_Y)
            if self.posicion_valida(nueva.get_rect(), [self.sierras, self.cajas]):
                self.sierras.append(nueva)
                self.contadores['sierra'] = 0
        else:
            self.contadores['sierra'] += 1

        # Generar cajas
        if random.random() < PROB_CAJA and self.contadores['caja'] > 30:
            nueva = Caja(ANCHO, SUELO_Y)
            if self.posicion_valida(nueva.get_rect(), [self.sierras, self.cajas]):
                self.cajas.append(nueva)
                self.contadores['caja'] = 0
        else:
            self.contadores['caja'] += 1

        # Generar refrescos
        if random.random() < PROB_REFRESCO and self.contadores['refresco'] > 20:
            nuevo = Refresco(ANCHO, SUELO_Y)
            if self.posicion_valida(nuevo.get_rect(), [self.sierras, self.cajas, self.refrescos_lista]):
                self.refrescos_lista.append(nuevo)
                self.contadores['refresco'] = 0
        else:
            self.contadores['refresco'] += 1

        # Mover y limpiar
        for lista in [self.sierras, self.cajas, self.refrescos_lista]:
            for obj in lista[:]:
                obj.update(self.velocidad)
                if obj.x < -200:
                    lista.remove(obj)

        # Colisiones
        rect_jug = self.stickman.get_rect()

        # Refrescos
        for r in self.refrescos_lista[:]:
            if rect_jug.colliderect(r.get_rect()):
                self.refrescos_sys.añadir(r.valor)
                self.refrescos_lista.remove(r)
                self.logros.actualizar('coleccionista', self.refrescos_sys.refrescos_totales)

        # Sierras
        for s in self.sierras[:]:
            if rect_jug.colliderect(s.get_rect()):
                if self.stickman.tiene_powerup('segundo_intento'):
                    self.stickman.usar_powerup('segundo_intento')
                    self.stickman.x, self.stickman.y = 300, SUELO_Y
                    self.sierras.remove(s)
                else:
                    self.estado = "GAME_OVER"
                break

        # Cajas
        for c in self.cajas[:]:
            if rect_jug.colliderect(c.get_rect()):
                if self.stickman.vel_y >= 0 and rect_jug.bottom <= c.get_rect().top + 20:
                    self.stickman.y = c.get_rect().top + rect_jug.height
                    self.stickman.vel_y = 0
                    self.stickman.en_suelo = True
                else:
                    if self.stickman.tiene_powerup('segundo_intento'):
                        self.stickman.usar_powerup('segundo_intento')
                        self.stickman.x, self.stickman.y = 300, SUELO_Y
                        self.cajas.remove(c)
                    else:
                        self.estado = "GAME_OVER"
                    break

        # Logros
        if self.puntuacion >= 2000:
            self.logros.actualizar('maratonista')
        if self.velocidad >= 20:
            self.logros.actualizar('veloz')
        if self.stickman.saltos_totales >= 150:
            self.logros.actualizar('saltarin')

        # Aumentar velocidad
        if self.puntuacion % 500 == 0 and self.velocidad < VEL_MAX:
            self.velocidad += 0.5

    def dibujar(self):
        self.fondo.dibujar(self.pantalla)

        if self.estado == "JUGANDO":
            for r in self.refrescos_lista:
                r.dibujar(self.pantalla)
            for s in self.sierras:
                s.dibujar(self.pantalla)
            for c in self.cajas:
                c.dibujar(self.pantalla)
            self.stickman.dibujar(self.pantalla)
            self.ui.hud(self.pantalla, self.puntuacion, self.refrescos_sys.refrescos)
            self.logros.dibujar_notificaciones(self.pantalla)

        elif self.estado == "MENU":
            self.botones_menu = self.ui.menu(self.pantalla, self.refrescos_sys.refrescos, self.stickman)

        elif self.estado == "PAUSA":
            for r in self.refrescos_lista:
                r.dibujar(self.pantalla)
            for s in self.sierras:
                s.dibujar(self.pantalla)
            for c in self.cajas:
                c.dibujar(self.pantalla)
            self.stickman.dibujar(self.pantalla)
            self.ui.hud(self.pantalla, self.puntuacion, self.refrescos_sys.refrescos)
            self.botones_pausa = self.ui.pausa(self.pantalla)

        elif self.estado == "TIENDA":
            self.ui.tienda(self.pantalla, self.refrescos_sys.refrescos)

        elif self.estado == "GAME_OVER":
            self.ui.game_over(self.pantalla)

        pygame.display.flip()

    def ejecutar(self):
        while True:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
    