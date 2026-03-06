# ============================================
# MAIN.PY - BUCLE PRINCIPAL CON DEBUG
# ============================================
import pygame
import sys
import random
import json
import os
import traceback

try:
    from config import *
    from world import FondoPersonalizado, Refresco, Sierra, Caja
    from systems import SistemaRefrescos, SistemaLogros, Tienda
    from player import Stickman
    from ui import UI
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de que todos los archivos .py están en la carpeta.")
    input("Presiona Enter para salir...")
    sys.exit(1)

class Juego:
    def __init__(self):
        try:
            pygame.init()
            self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
            pygame.display.set_caption(TITULO)
            self.reloj = pygame.time.Clock()
            
            print("Inicializando fondo...")
            self.fondo = FondoPersonalizado("assets/fondo.jpg")
            
            print("Inicializando jugador...")
            self.stickman = Stickman(300, SUELO_Y)
            
            print("Inicializando sistemas...")
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
            self.contadores = {'s': 0, 'c': 0, 'r': 0}
            
            print("Cargando progreso...")
            self.cargar()
            self.logros.actualizar('primer_paso')
            print("✅ Juego inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error en __init__: {e}")
            traceback.print_exc()
            input("Presiona Enter para salir...")
            pygame.quit()
            sys.exit(1)

    def cargar(self):
        try:
            if os.path.exists('data/save.json'):
                with open('data/save.json', 'r') as f:
                    d = json.load(f)
                    self.refrescos_sys.refrescos = d.get('refrescos', 0)
                    self.refrescos_sys.refrescos_totales = d.get('totales', 0)
        except Exception as e:
            print(f"⚠️ Error cargando progreso: {e}")

    def guardar(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/save.json', 'w') as f:
                json.dump({
                    'refrescos': self.refrescos_sys.refrescos,
                    'totales': self.refrescos_sys.refrescos_totales
                }, f)
        except Exception as e:
            print(f"⚠️ Error guardando progreso: {e}")

    def reiniciar(self):
        self.stickman = Stickman(300, SUELO_Y)
        self.puntuacion = 0
        self.velocidad = VELOCIDAD_BASE
        self.sierras.clear()
        self.cajas.clear()
        self.refrescos_lista.clear()
        self.contadores = {'s': 0, 'c': 0, 'r': 0}

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
                        self.stickman.finalizar_carga()
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        self.stickman.agachar(False)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = e.pos
                    if ANCHO - 120 <= mx <= ANCHO - 20 and ALTO - 70 <= my <= ALTO - 20:
                        self.estado = "PAUSA"
            elif self.estado == "PAUSA":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.estado = "JUGANDO"
                    elif e.key == pygame.K_q:
                        self.estado = "MENU"
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

    def actualizar(self):
        if self.estado != "JUGANDO":
            return
        try:
            self.fondo.update(self.velocidad)
            self.stickman.update()
            self.puntuacion += 1

            # Generar refrescos
            self.contadores['r'] += 1
            if self.contadores['r'] > random.randint(180, 300):
                nuevo = Refresco(ANCHO, SUELO_Y)
                # evitar spawn sobre otros objetos
                valido = True
                for obs in self.sierras + self.cajas:
                    if nuevo.get_rect().colliderect(obs.get_rect()):
                        valido = False
                        break
                if valido:
                    self.refrescos_lista.append(nuevo)
                    self.contadores['r'] = 0

            # Generar sierras
            self.contadores['s'] += 1
            if self.contadores['s'] > random.randint(120, 200):
                self.sierras.append(Sierra(ANCHO, SUELO_Y))
                self.contadores['s'] = 0

            # Generar cajas
            self.contadores['c'] += 1
            if self.contadores['c'] > random.randint(150, 250):
                self.cajas.append(Caja(ANCHO, SUELO_Y))
                self.contadores['c'] = 0

            # Mover y limpiar objetos
            for lista in [self.refrescos_lista, self.sierras, self.cajas]:
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

            # Cajas (muerte solo si choca de frente)
            for c in self.cajas[:]:
                if rect_jug.colliderect(c.get_rect()):
                    if rect_jug.bottom <= c.get_rect().top + 15:
                        # pasa por encima
                        pass
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

        except Exception as e:
            print(f"❌ Error en actualizar: {e}")
            traceback.print_exc()
            input("Presiona Enter para continuar...")

    def dibujar(self):
        try:
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
                self.ui.menu(self.pantalla, self.refrescos_sys.refrescos)
            elif self.estado == "PAUSA":
                for r in self.refrescos_lista:
                    r.dibujar(self.pantalla)
                for s in self.sierras:
                    s.dibujar(self.pantalla)
                for c in self.cajas:
                    c.dibujar(self.pantalla)
                self.stickman.dibujar(self.pantalla)
                self.ui.hud(self.pantalla, self.puntuacion, self.refrescos_sys.refrescos)
                self.ui.pausa(self.pantalla)
            elif self.estado == "TIENDA":
                self.ui.tienda(self.pantalla, self.refrescos_sys.refrescos)
            elif self.estado == "GAME_OVER":
                self.ui.game_over(self.pantalla)
            pygame.display.flip()
        except Exception as e:
            print(f"❌ Error en dibujar: {e}")
            traceback.print_exc()
            input("Presiona Enter para continuar...")

    def ejecutar(self):
        try:
            while True:
                self.manejar_eventos()
                self.actualizar()
                self.dibujar()
                self.reloj.tick(FPS)
        except Exception as e:
            print(f"❌ Error en bucle principal: {e}")
            traceback.print_exc()
            input("Presiona Enter para salir...")
            pygame.quit()
            sys.exit(1)

if __name__ == "__main__":
    try:
        juego = Juego()
        juego.ejecutar()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")
        pygame.quit()
        sys.exit(1)