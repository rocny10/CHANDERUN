# ============================================
# main.py
# ============================================
import pygame
import sys
import random
import json
import os

from config  import *
from world   import Fondo, Refresco, Sierra, Caja, seleccionar_patron, spawn_patron
from systems import SistemaRefrescos, SistemaLogros
from player  import Stickman
from ui      import UI


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO,ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()

        self.refrescos_sys = SistemaRefrescos()
        self.logros        = SistemaLogros()
        self.ui            = UI()
        self.fondo         = Fondo("assets/fondo.jpg")

        self.skin_actual         = 0
        self.skins_desbloqueadas = {0:True, 1:False}

        self.stickman = Stickman(X_INICIO, SUELO_Y, skin=self.skin_actual)

        self.tiene_segundo_intento = False
        self._invencible_hasta     = 0

        self.estado     = "MENU"
        self.puntuacion = 0
        self.velocidad  = VELOCIDAD_BASE

        self.obstaculos: list = []
        self.monedas:    list = []
        self._frames_spawn    = DIST_MIN_PATRON
        self._botones: dict   = {}

        self._cargar()
        self.logros.actualizar('primer_paso')

    # ── Guardado ─────────────────────────────────────────────────
    def _cargar(self):
        try:
            if os.path.exists('data/save.json'):
                with open('data/save.json') as f:
                    d = json.load(f)
                self.refrescos_sys.refrescos         = d.get('refrescos', 0)
                self.refrescos_sys.refrescos_totales = d.get('totales',   0)
                self.skin_actual = int(d.get('skin', 0))
                sk = d.get('skins_desbloqueadas', {})
                self.skins_desbloqueadas = {
                    0: True,
                    1: bool(sk.get('1', False) or sk.get(1, False)),
                }
                self.stickman.skin = self.skin_actual
        except Exception as e:
            print(f"Warn cargar: {e}")

    def _guardar(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/save.json','w') as f:
                json.dump({'refrescos':self.refrescos_sys.refrescos,
                           'totales':self.refrescos_sys.refrescos_totales,
                           'skin':self.skin_actual,
                           'skins_desbloqueadas':{'0':True,'1':self.skins_desbloqueadas.get(1,False)}},f)
        except Exception as e:
            print(f"Warn guardar: {e}")

    def _salir(self):
        self._guardar(); pygame.quit(); sys.exit()

    # ── Reinicio ─────────────────────────────────────────────────
    def _reiniciar(self):
        tenia = self.tiene_segundo_intento
        self.stickman    = Stickman(X_INICIO, SUELO_Y, skin=self.skin_actual)
        self.puntuacion  = 0
        self.velocidad   = VELOCIDAD_BASE
        self.obstaculos.clear(); self.monedas.clear()
        self._frames_spawn     = DIST_MIN_PATRON
        self._invencible_hasta = 0
        self.tiene_segundo_intento = tenia

    def _ir_a_jugar(self):
        self._reiniciar()
        self.stickman.set_animacion("run")
        self.estado = "JUGANDO"

    # ── Skins ─────────────────────────────────────────────────────
    def _cambiar_skin(self, delta):
        nueva = (self.skin_actual + delta) % len(self.stickman._skins)
        self.skin_actual = nueva
        self.stickman.skin = nueva

    def _comprar_skin(self, idx):
        if self.skins_desbloqueadas.get(idx, False): return
        precio = PRECIO_SKIN_2 if idx==1 else 0
        if precio==0 or self.refrescos_sys.gastar(precio):
            self.skins_desbloqueadas[idx] = True
            print(f"OK Skin {NOMBRE_SKIN.get(idx,'?')} desbloqueada")

    def _comprar_segundo_intento(self):
        if self.tiene_segundo_intento: return
        if self.refrescos_sys.gastar(PRECIO_SEGUNDO_INTENTO):
            self.tiene_segundo_intento = True
            print("OK Segundo intento activado")

    # ── Spawn ─────────────────────────────────────────────────────
    def _tick_spawn(self):
        self._frames_spawn -= 1
        if self._frames_spawn > 0: return
        obs, mon = spawn_patron(seleccionar_patron(self.velocidad), SUELO_Y)
        self.obstaculos.extend(obs); self.monedas.extend(mon)
        self._frames_spawn = random.randint(DIST_MIN_PATRON, DIST_MAX_PATRON)

    # ── Colisiones ────────────────────────────────────────────────
    def _golpe_caja(self, caja):
        """True=muere  False=aterriza encima."""
        rect_j = self.stickman.get_rect()
        rect_c = caja.get_rect()
        prev_b = rect_j.bottom - self.stickman.vel_y
        if self.stickman.vel_y >= 0 and prev_b <= rect_c.top + 8:
            self.stickman.y        = rect_c.top
            self.stickman.vel_y    = 0
            self.stickman.en_suelo = True
            return False
        return True

    def _usar_segundo_intento(self, obs):
        if not self.tiene_segundo_intento: return False
        self.tiene_segundo_intento = False
        self.stickman.x = X_INICIO; self.stickman.y = SUELO_Y
        self.stickman.vel_y = 0; self.stickman.en_suelo = True
        self._invencible_hasta = pygame.time.get_ticks() + 1500
        if obs in self.obstaculos: self.obstaculos.remove(obs)
        print("! Segundo intento usado")
        return True

    def _colisiones(self):
        ahora  = pygame.time.get_ticks()
        rect_j = self.stickman.get_rect()

        for m in self.monedas[:]:
            if rect_j.colliderect(m.get_rect()):
                self.refrescos_sys.añadir(m.valor)
                self.monedas.remove(m)
                self.logros.actualizar('coleccionista')

        if ahora < self._invencible_hasta: return

        for obs in self.obstaculos[:]:
            if not rect_j.colliderect(obs.get_rect()): continue
            muere = self._golpe_caja(obs) if isinstance(obs, Caja) else True
            if muere:
                if not self._usar_segundo_intento(obs):
                    self.estado = "GAME_OVER"
            return

    # ── Eventos ───────────────────────────────────────────────────
    def _eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self._salir()

            # MENU
            if self.estado == "MENU":
                if e.type == pygame.KEYDOWN:
                    if   e.key == pygame.K_SPACE: self._ir_a_jugar()
                    elif e.key == pygame.K_t:     self.estado = "TIENDA"
                    elif e.key == pygame.K_ESCAPE:self._salir()
                    elif e.key == pygame.K_LEFT:  self._cambiar_skin(-1)
                    elif e.key == pygame.K_RIGHT: self._cambiar_skin(1)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    b=self._botones; p=e.pos
                    if   b.get('jugar')    and b['jugar'].collidepoint(p):    self._ir_a_jugar()
                    elif b.get('tienda')   and b['tienda'].collidepoint(p):   self.estado="TIENDA"
                    elif b.get('salir')    and b['salir'].collidepoint(p):    self._salir()
                    elif b.get('skin_izq') and b['skin_izq'].collidepoint(p): self._cambiar_skin(-1)
                    elif b.get('skin_der') and b['skin_der'].collidepoint(p): self._cambiar_skin(1)

            # JUGANDO
            elif self.estado == "JUGANDO":
                if e.type == pygame.KEYDOWN:
                    if   e.key == pygame.K_SPACE:                    self.stickman.saltar()
                    elif e.key in (pygame.K_DOWN, pygame.K_s):       self.stickman.agachar(True)
                    elif e.key == pygame.K_ESCAPE:                   self.estado="PAUSA"
                    elif e.key in (pygame.K_LEFT,  pygame.K_a):     self.stickman.mov_izq=True
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):     self.stickman.mov_der=True
                elif e.type == pygame.KEYUP:
                    if   e.key == pygame.K_SPACE:                    self.stickman.soltar_salto()
                    elif e.key in (pygame.K_DOWN, pygame.K_s):       self.stickman.agachar(False)
                    elif e.key in (pygame.K_LEFT,  pygame.K_a):     self.stickman.mov_izq=False
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):     self.stickman.mov_der=False

            # PAUSA
            elif self.estado == "PAUSA":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: self.estado="JUGANDO"
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    b=self._botones; p=e.pos
                    if   b.get('continuar') and b['continuar'].collidepoint(p): self.estado="JUGANDO"
                    elif b.get('menu')      and b['menu'].collidepoint(p):      self.estado="MENU"
                    elif b.get('salir')     and b['salir'].collidepoint(p):     self._salir()

            # TIENDA
            elif self.estado == "TIENDA":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: self.estado="MENU"
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    b=self._botones; p=e.pos
                    if   b.get('skin_0')          and b['skin_0'].collidepoint(p):          self._comprar_skin(0)
                    elif b.get('skin_1')          and b['skin_1'].collidepoint(p):          self._comprar_skin(1)
                    elif b.get('segundo_intento') and b['segundo_intento'].collidepoint(p): self._comprar_segundo_intento()
                    elif b.get('volver')          and b['volver'].collidepoint(p):          self.estado="MENU"

            # GAME OVER
            elif self.estado == "GAME_OVER":
                if e.type == pygame.KEYDOWN:
                    if   e.key == pygame.K_r:      self._ir_a_jugar()
                    elif e.key == pygame.K_ESCAPE: self.estado="MENU"
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    b=self._botones; p=e.pos
                    if   b.get('reintentar') and b['reintentar'].collidepoint(p): self._ir_a_jugar()
                    elif b.get('menu')       and b['menu'].collidepoint(p):       self.estado="MENU"

    # ── Actualizar ────────────────────────────────────────────────
    def _actualizar(self):
        if self.estado == "MENU":
            self.stickman.set_animacion("idle")
            self.stickman.avanzar_frame()
            return
        if self.estado != "JUGANDO": return

        self.fondo.update(self.velocidad)
        self.stickman.update(jugando=True)
        self.puntuacion += 1

        umbral = -(OBJ_SIZE * 4)
        for lst in (self.obstaculos, self.monedas):
            for obj in lst[:]:
                obj.update(self.velocidad)
                if obj.x < umbral: lst.remove(obj)

        self._tick_spawn()
        self._colisiones()

        if self.puntuacion % INTERVALO_VEL == 0 and self.velocidad < VEL_MAX:
            self.velocidad += AUMENTO_VEL

        if self.puntuacion >= 2000:  self.logros.actualizar('maratonista')
        if self.velocidad >= VEL_MAX: self.logros.actualizar('veloz')
        if self.stickman.saltos_totales >= 150: self.logros.actualizar('saltarin')

    # ── Dibujar ───────────────────────────────────────────────────
    def _dibujar_mundo(self):
        for obj in self.obstaculos: obj.dibujar(self.pantalla)
        for m   in self.monedas:   m.dibujar(self.pantalla)
        ahora = pygame.time.get_ticks()
        if ahora < self._invencible_hasta:
            alpha = 255 if (ahora//100)%2==0 else 80
            self.stickman.dibujar(self.pantalla, alpha)
        else:
            self.stickman.dibujar(self.pantalla)

    def _dibujar(self):
        self.fondo.dibujar(self.pantalla)

        if self.estado == "JUGANDO":
            self._dibujar_mundo()
            self.ui.hud(self.pantalla, self.puntuacion,
                        self.refrescos_sys.refrescos)
            self.logros.dibujar_notificaciones(self.pantalla, self.ui.f_pequena)
            if self.tiene_segundo_intento:
                t = self.ui.f_mini.render("SI activo", True, DORADO)
                self.pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 22))

        elif self.estado == "MENU":
            self._botones = self.ui.menu(
                self.pantalla, self.refrescos_sys.refrescos,
                self.stickman, self.skin_actual, self.skins_desbloqueadas)

        elif self.estado == "PAUSA":
            self._dibujar_mundo()
            self.ui.hud(self.pantalla, self.puntuacion,
                        self.refrescos_sys.refrescos)
            self._botones = self.ui.pausa(self.pantalla)

        elif self.estado == "TIENDA":
            self._botones = self.ui.tienda(
                self.pantalla, self.refrescos_sys.refrescos,
                self.stickman, self.skins_desbloqueadas,
                self.tiene_segundo_intento)

        elif self.estado == "GAME_OVER":
            self._dibujar_mundo()
            self._botones = self.ui.game_over(self.pantalla, self.puntuacion)

        pygame.display.flip()

    # ── Bucle ─────────────────────────────────────────────────────
    def ejecutar(self):
        while True:
            self._eventos()
            self._actualizar()
            self._dibujar()
            self.reloj.tick(FPS)


if __name__ == "__main__":
    Juego().ejecutar()
