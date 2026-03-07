# ============================================
# ui.py  —  Pixel-art UI
# ============================================
import pygame
import os
from config import *


def _fuente(path, size):
    if os.path.exists(path):
        try:   return pygame.font.Font(path, size)
        except Exception as e: print(f"Warn fuente {size}px: {e}")
    return pygame.font.Font(None, size)


def px_rect(surf, color, rect, borde=None, g=2):
    pygame.draw.rect(surf, color, rect)
    if borde: pygame.draw.rect(surf, borde, rect, g)


def px_boton(surf, fuente, texto, rect,
             color=None, borde=None, ct=None):
    bg = color or UI_PANEL
    bd = borde or UI_BORDE
    c  = ct    or UI_TEXTO
    pygame.draw.rect(surf, bg, rect)
    pygame.draw.rect(surf, bd, rect, 2)
    pygame.draw.rect(surf, bd, rect.inflate(-4,-4), 1)
    t = fuente.render(texto, True, c)
    surf.blit(t, (rect.centerx - t.get_width()//2,
                  rect.centery - t.get_height()//2))
    return rect


class UI:
    _BW = 250; _BH = 52; _GAP = 10

    def __init__(self):
        self.f_titulo  = _fuente(FUENTE_TTF, 68)
        self.f_grande  = _fuente(FUENTE_TTF, 50)
        self.f_mediana = _fuente(FUENTE_TTF, 34)
        self.f_pequena = _fuente(FUENTE_TTF, 26)
        self.f_mini    = _fuente(FUENTE_TTF, 20)

        self.logo = None
        try:
            img = pygame.image.load("assets/logo.png").convert_alpha()
            w=340; h=int(img.get_height()*w/img.get_width())
            self.logo = pygame.transform.scale(img,(w,h))
        except: pass

        # Sprite refresco para HUD — cargado a tamaño fijo
        self.img_ref = None
        try:
            img = pygame.image.load("assets/refresco.png").convert_alpha()
            self.img_ref = pygame.transform.scale(img, (30, 30))
        except: pass

    # ── Helpers ─────────────────────────────────────────────────

    def _overlay(self, pantalla, alpha=200):
        s = pygame.Surface((ANCHO,ALTO), pygame.SRCALPHA)
        s.fill((0,0,12,alpha)); pantalla.blit(s,(0,0))

    def _draw_refrescos(self, pantalla, cantidad, x, y, f=None):
        """Dibuja sprite + número. Usa fallback ASCII si no hay imagen."""
        f = f or self.f_mediana
        if self.img_ref:
            pantalla.blit(self.img_ref, (x, y+2))
            t = f.render(str(cantidad), True, DORADO)
            pantalla.blit(t, (x+36, y))
        else:
            t = f.render(f"[{cantidad}]", True, DORADO)
            pantalla.blit(t, (x, y))

    def _columna(self, pantalla, items, cx, y0):
        rects = []
        for i, item in enumerate(items):
            texto=item[0]; cbg=item[1] if len(item)>1 else UI_PANEL
            cbd=item[2] if len(item)>2 else UI_BORDE
            ct=item[3] if len(item)>3 else UI_TEXTO
            r = pygame.Rect(cx-self._BW//2, y0+i*(self._BH+self._GAP),
                            self._BW, self._BH)
            px_boton(pantalla, self.f_pequena, texto, r,
                     color=cbg, borde=cbd, ct=ct)
            rects.append(r)
        return rects

    # ── MENU ────────────────────────────────────────────────────
    def menu(self, pantalla, refrescos, stickman,
             skin_actual=0, skins_desbloqueadas=None):
        if skins_desbloqueadas is None:
            skins_desbloqueadas = {0:True,1:False}

        self._overlay(pantalla, 170)

        # Logo
        if self.logo:
            pantalla.blit(self.logo, (70,50))
        else:
            t = self.f_titulo.render("CHANDE-RUN", True, DORADO)
            pantalla.blit(t, (70,60))

        # Refrescos arriba derecha
        self._draw_refrescos(pantalla, refrescos, ANCHO-175, 26)

        # ── Personaje en X_INICIO (misma posición que al correr) ──
        ox, oy = stickman.x, stickman.y
        stickman.x = X_INICIO
        stickman.y = SUELO_Y
        stickman.set_animacion("idle")
        stickman.dibujar(pantalla)
        stickman.x, stickman.y = ox, oy

        # Nombre skin
        nombre = NOMBRE_SKIN.get(skin_actual, "?")
        lock   = not skins_desbloqueadas.get(skin_actual, False)
        label  = f"[L] {nombre}" if lock else nombre
        t_s = self.f_mini.render(label, True, UI_ACENTO)
        ty  = SUELO_Y + 10
        pantalla.blit(t_s, (X_INICIO - t_s.get_width()//2, ty))

        # Flechas selector
        ay = ty + t_s.get_height() + 6
        r_izq = pygame.Rect(X_INICIO-58, ay, 44, 30)
        r_der = pygame.Rect(X_INICIO+14, ay, 44, 30)
        px_boton(pantalla, self.f_pequena, "<", r_izq)
        px_boton(pantalla, self.f_pequena, ">", r_der)

        # Botones derecha
        bx = ANCHO - 190
        rects = self._columna(pantalla, [
            ("JUGAR",),
            ("TIENDA",),
            ("SALIR", (55,18,18), UI_ROJO, (255,110,110)),
        ], bx, 330)

        return {'jugar':rects[0],'tienda':rects[1],'salir':rects[2],
                'skin_izq':r_izq,'skin_der':r_der}

    # ── HUD ─────────────────────────────────────────────────────
    def hud(self, pantalla, puntuacion, refrescos):
        self._draw_refrescos(pantalla, refrescos, 22, 22)
        t = self.f_mediana.render(str(puntuacion), True, BLANCO)
        pantalla.blit(t, (ANCHO - t.get_width() - 22, 22))

    # ── PAUSA ────────────────────────────────────────────────────
    def pausa(self, pantalla):
        self._overlay(pantalla, 210)
        t = self.f_grande.render("PAUSA", True, BLANCO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 170))
        cx = ANCHO//2
        rects = self._columna(pantalla, [
            ("CONTINUAR",),
            ("MENU PRINCIPAL",),
            ("SALIR", (55,18,18), UI_ROJO, (255,110,110)),
        ], cx, 295)
        return {'continuar':rects[0],'menu':rects[1],'salir':rects[2]}

    # ── TIENDA ──────────────────────────────────────────────────
    def tienda(self, pantalla, refrescos, stickman,
               skins_desbloqueadas=None, tiene_segundo_intento=False):
        if skins_desbloqueadas is None:
            skins_desbloqueadas = {0:True,1:False}

        self._overlay(pantalla, 235)

        # Título
        t = self.f_grande.render("TIENDA", True, DORADO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 28))

        # Saldo
        self._draw_refrescos(pantalla, refrescos, ANCHO//2 - 55, 86)

        # Separador
        pygame.draw.line(pantalla, UI_BORDE, (80,128), (ANCHO-80,128), 2)

        # Sub-título skins
        ts = self.f_mini.render("SKINS", True, UI_ACENTO)
        pantalla.blit(ts, (ANCHO//2 - ts.get_width()//2, 135))

        # ── Previews de skins ───────────────────────────────────
        prev_sz = 108
        cx0 = ANCHO//2 - prev_sz - 50
        cx1 = ANCHO//2 + 50
        y_p = 155
        botones = {}

        for idx, cxs in ((0,cx0),(1,cx1)):
            desbloq = skins_desbloqueadas.get(idx, False)
            nombre  = NOMBRE_SKIN.get(idx, f"Skin {idx+1}")
            precio  = 0 if idx==0 else PRECIO_SKIN_2

            # Marco
            marco = pygame.Rect(cxs-4, y_p-4, prev_sz+8, prev_sz+8)
            col_m = UI_BORDE_DORADO if desbloq else UI_BORDE
            pygame.draw.rect(pantalla, UI_PANEL2, marco)
            pygame.draw.rect(pantalla, col_m, marco, 2)

            # Sprite preview
            frame = stickman.get_frame_preview(idx, "idle", prev_sz)
            if frame:
                pantalla.blit(frame, (cxs, y_p))
            else:
                cc = (220,180,140) if idx==0 else (80,140,220)
                pygame.draw.rect(pantalla, cc, (cxs, y_p, prev_sz, prev_sz))
                pygame.draw.rect(pantalla, NEGRO, (cxs, y_p, prev_sz, prev_sz), 2)

            # Nombre
            tn = self.f_mini.render(nombre, True, BLANCO)
            pantalla.blit(tn, (cxs+prev_sz//2 - tn.get_width()//2,
                               y_p + prev_sz + 6))

            # Botón
            bw_b = prev_sz+16; by_b = y_p+prev_sz+28
            r_b  = pygame.Rect(cxs-8, by_b, bw_b, 40)
            if desbloq:
                px_boton(pantalla, self.f_mini, "TUYA", r_b,
                         color=(15,45,15), borde=(35,130,35), ct=(70,210,70))
            else:
                px_boton(pantalla, self.f_mini, f"{precio}", r_b,
                         color=UI_PANEL, borde=UI_BORDE_DORADO, ct=DORADO)
                # ícono refresco junto al precio
                if self.img_ref:
                    ri = pygame.transform.scale(self.img_ref, (18,18))
                    pantalla.blit(ri, (r_b.x+5, r_b.centery-9))
            botones[f'skin_{idx}'] = r_b

        # Separador
        y_s2 = y_p + prev_sz + 82
        pygame.draw.line(pantalla, UI_BORDE, (80,y_s2), (ANCHO-80,y_s2), 2)

        # PowerUps
        tpu = self.f_mini.render("POWER-UPS", True, UI_ACENTO)
        pantalla.blit(tpu, (ANCHO//2 - tpu.get_width()//2, y_s2+7))

        y_pu = y_s2 + 36
        r_pu = pygame.Rect(ANCHO//2-185, y_pu, 370, 50)
        if tiene_segundo_intento:
            px_boton(pantalla, self.f_pequena,
                     "Segundo Intento  - ACTIVO", r_pu,
                     color=(15,45,15), borde=(35,130,35), ct=(70,210,70))
        else:
            px_boton(pantalla, self.f_pequena,
                     f"Segundo Intento  {PRECIO_SEGUNDO_INTENTO}", r_pu,
                     color=UI_PANEL, borde=UI_BORDE, ct=UI_TEXTO)
            if self.img_ref:
                ri = pygame.transform.scale(self.img_ref,(20,20))
                pantalla.blit(ri, (r_pu.right - 95, r_pu.centery-10))
        botones['segundo_intento'] = r_pu

        # Volver
        r_vol = pygame.Rect(ANCHO//2-95, y_pu+68, 190, 46)
        px_boton(pantalla, self.f_pequena, "VOLVER", r_vol,
                 color=(45,15,15), borde=UI_ROJO, ct=(255,100,100))
        botones['volver'] = r_vol

        return botones

    # ── GAME OVER ────────────────────────────────────────────────
    def game_over(self, pantalla, puntuacion=0):
        self._overlay(pantalla, 215)
        t = self.f_grande.render("GAME OVER", True, ROJO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 200))
        p = self.f_mediana.render(f"Puntuacion: {puntuacion}", True, BLANCO)
        pantalla.blit(p, (ANCHO//2 - p.get_width()//2, 280))
        cx = ANCHO//2
        rects = self._columna(pantalla, [
            ("REINTENTAR",),
            ("MENU PRINCIPAL",),
        ], cx, 360)
        return {'reintentar':rects[0],'menu':rects[1]}
