# ============================================
# ui.py  —  Liquid Glass UI
# ============================================
import pygame, os, math
from config import *


def _fuente(path, size):
    if os.path.exists(path):
        try:   return pygame.font.Font(path, size)
        except Exception as e: print(f"Warn fuente {size}px: {e}")
    return pygame.font.Font(None, size)


# ══════════════════════════════════════════════
#  PRIMITIVAS GLASS
# ══════════════════════════════════════════════

def glass_fill(surf, rect, tint=(120,160,255), fill_a=22, border_a=65):
    """Panel de vidrio esmerilado."""
    r = pygame.Rect(rect)
    # Relleno semitransparente
    s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
    s.fill((*tint, fill_a))
    surf.blit(s, r.topleft)
    # Borde brillante
    bs = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
    pygame.draw.rect(bs, (220, 235, 255, border_a), (0, 0, r.w, r.h), 1)
    surf.blit(bs, r.topleft)
    # Resalte superior (highlight)
    hs = pygame.Surface((r.w - 4, 2), pygame.SRCALPHA)
    hs.fill((255, 255, 255, 38))
    surf.blit(hs, (r.x+2, r.y+2))


def glass_button(surf, fuente, texto, rect,
                 tint=(80,120,240), fill_a=32, border_a=85, ct=None):
    """Botón glass con texto centrado."""
    ct = ct or (240, 248, 255)
    glass_fill(surf, rect, tint, fill_a, border_a)
    t = fuente.render(texto, True, ct)
    surf.blit(t, (rect.centerx - t.get_width()//2,
                  rect.centery - t.get_height()//2))
    return pygame.Rect(rect)


def glow_line(surf, p1, p2, color, alpha=60, thickness=2):
    """Línea con suave glow."""
    s = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
    pygame.draw.line(s, (*color, alpha), p1, p2, thickness)
    surf.blit(s, (0, 0))


def draw_gradient_overlay(surf, top_col, bot_col, alpha_top=200, alpha_bot=240):
    """Overlay degradado para fondos de menú."""
    w, h = surf.get_size()
    for y in range(h):
        t     = y / h
        r     = int(top_col[0]*(1-t) + bot_col[0]*t)
        g_c   = int(top_col[1]*(1-t) + bot_col[1]*t)
        b     = int(top_col[2]*(1-t) + bot_col[2]*t)
        alpha = int(alpha_top*(1-t) + alpha_bot*t)
        s = pygame.Surface((w, 1), pygame.SRCALPHA)
        s.fill((r, g_c, b, alpha))
        surf.blit(s, (0, y))


class UI:
    _BW = 260; _BH = 54; _GAP = 12

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

        # Refresco HUD (tamaño fijo, NUNCA cambia con OBJ_SIZE)
        self.img_ref   = None
        self.img_ref_s = None
        try:
            raw = pygame.image.load("assets/refresco.png").convert_alpha()
            self.img_ref   = pygame.transform.scale(raw, (30, 30))
            self.img_ref_s = pygame.transform.scale(raw, (18, 18))
        except: pass

    # ── Helpers ─────────────────────────────────────────────────

    def _overlay(self, pantalla):
        draw_gradient_overlay(pantalla,
                              (10, 15, 35), (5, 8, 22),
                              alpha_top=185, alpha_bot=230)

    def _draw_ref(self, pantalla, cantidad, x, y, fuente=None, small=False):
        f   = fuente or self.f_mediana
        img = self.img_ref_s if small else self.img_ref
        sz  = 18 if small else 30
        if img:
            pantalla.blit(img, (x, y + (f.size("0")[1]-sz)//2))
            t = f.render(str(cantidad), True, (255, 215, 60))
            pantalla.blit(t, (x + sz + 5, y))
        else:
            t = f.render(str(cantidad), True, (255, 215, 60))
            pantalla.blit(t, (x, y))

    def _columna(self, pantalla, items, cx, y0,
                 bw=None, bh=None, gap=None):
        bw  = bw  or self._BW
        bh  = bh  or self._BH
        gap = gap or self._GAP
        rects = []
        for i, item in enumerate(items):
            texto = item[0]
            tint  = item[1] if len(item)>1 else (80,120,240)
            ct    = item[2] if len(item)>2 else (240,248,255)
            r = pygame.Rect(cx-bw//2, y0+i*(bh+gap), bw, bh)
            glass_button(pantalla, self.f_pequena, texto, r, tint=tint, ct=ct)
            rects.append(r)
        return rects

    # ── MENU PRINCIPAL ──────────────────────────────────────────
    def menu(self, pantalla, refrescos, stickman,
             skin_actual=0, skins_desbloqueadas=None):
        if skins_desbloqueadas is None:
            skins_desbloqueadas = {0:True,1:False,2:False}

        self._overlay(pantalla)

        # Línea horizontal decorativa
        glow_line(pantalla, (60, SUELO_Y-2), (ANCHO-60, SUELO_Y-2),
                  GLASS_CYAN, alpha=50, thickness=1)

        # Logo / título
        if self.logo:
            pantalla.blit(self.logo, (65, 48))
        else:
            t = self.f_titulo.render("CHANDE-RUN", True, (255, 215, 60))
            pantalla.blit(t, (65, 55))

        # Refrescos arriba derecha
        self._draw_ref(pantalla, refrescos, ANCHO-185, 28)

        # ── Personaje en X_INICIO (misma posición que jugando) ──
        ox, oy = stickman.x, stickman.y
        stickman.x = X_INICIO; stickman.y = SUELO_Y
        stickman.set_animacion("idle")
        stickman.dibujar(pantalla)
        stickman.x, stickman.y = ox, oy

        # Nombre skin + selector
        nombre = NOMBRE_SKIN.get(skin_actual, "?")
        lock   = not skins_desbloqueadas.get(skin_actual, False)
        label  = f"[L] {nombre}" if lock else nombre

        ts = self.f_mini.render(label, True, (140, 200, 255))
        ty = SUELO_Y + 10
        pantalla.blit(ts, (X_INICIO - ts.get_width()//2, ty))

        ay    = ty + ts.get_height() + 7
        r_izq = pygame.Rect(X_INICIO-60, ay, 46, 30)
        r_der = pygame.Rect(X_INICIO+14, ay, 46, 30)
        glass_button(pantalla, self.f_pequena, "<", r_izq,
                     tint=(60,90,180), fill_a=28)
        glass_button(pantalla, self.f_pequena, ">", r_der,
                     tint=(60,90,180), fill_a=28)

        # Botones derecha — glass con tints distintos
        bx = ANCHO - 200
        rects = self._columna(pantalla, [
            ("JUGAR",   (40, 160, 80),  (200, 255, 220)),
            ("TIENDA",  (60, 100, 220), (200, 225, 255)),
            ("SALIR",   (180, 40, 40),  (255, 180, 180)),
        ], bx, 320)

        return {'jugar':rects[0], 'tienda':rects[1], 'salir':rects[2],
                'skin_izq':r_izq, 'skin_der':r_der}

    # ── HUD ─────────────────────────────────────────────────────
    def hud(self, pantalla, puntuacion, refrescos):
        self._draw_ref(pantalla, refrescos, 22, 22)
        t = self.f_mediana.render(str(puntuacion), True, (240, 248, 255))
        pantalla.blit(t, (ANCHO - t.get_width() - 22, 22))

    # ── PAUSA ────────────────────────────────────────────────────
    def pausa(self, pantalla):
        self._overlay(pantalla)
        t = self.f_grande.render("PAUSA", True, (240, 248, 255))
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 155))
        glow_line(pantalla, (100,215),(ANCHO-100,215),GLASS_CYAN,alpha=45)
        rects = self._columna(pantalla, [
            ("CONTINUAR",  (40,160,80),  (200,255,220)),
            ("MENU",       (60,100,220), (200,225,255)),
            ("SALIR",      (180,40,40),  (255,180,180)),
        ], ANCHO//2, 270)
        return {'continuar':rects[0], 'menu':rects[1], 'salir':rects[2]}

    # ── TIENDA ──────────────────────────────────────────────────
    def tienda(self, pantalla, refrescos, stickman,
               skins_desbloqueadas=None, tiene_segundo_intento=False):
        if skins_desbloqueadas is None:
            skins_desbloqueadas = {0:True,1:False,2:False}

        self._overlay(pantalla)

        # Título
        t = self.f_grande.render("TIENDA", True, (255, 215, 60))
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 20))

        # Saldo — ícono SEPARADO del texto, nunca dentro de un botón
        self._draw_ref(pantalla, refrescos, ANCHO//2 - 52, 78)

        glow_line(pantalla, (70,120),(ANCHO-70,120), GLASS_CYAN, alpha=40)

        # Sub-título skins
        ts = self.f_mini.render("S  K  I  N  S", True, (120, 190, 255))
        pantalla.blit(ts, (ANCHO//2 - ts.get_width()//2, 128))

        # ── 3 previews animados ─────────────────────────────────
        N        = 3
        CARD_W   = 120     # ancho del preview
        CARD_GAP = 90      # espacio entre cards
        TOTAL_W  = N * CARD_W + (N-1) * CARD_GAP   # = 480
        x_start  = ANCHO//2 - TOTAL_W//2            # = 400
        y_card   = 148
        tick     = pygame.time.get_ticks()
        botones  = {}

        for idx in range(N):
            cxs     = x_start + idx * (CARD_W + CARD_GAP)
            desbloq = skins_desbloqueadas.get(idx, False)
            nombre  = NOMBRE_SKIN.get(idx, f"Skin {idx}")
            precio  = PRECIO_SKIN.get(idx, 0)

            # Marco glass del card
            marco = pygame.Rect(cxs - 6, y_card - 4, CARD_W + 12, CARD_W + 12)
            if desbloq:
                glass_fill(pantalla, marco, tint=(40,160,60), fill_a=20, border_a=100)
            else:
                glass_fill(pantalla, marco, tint=(80,100,200), fill_a=15, border_a=65)

            # Sprite animado (spin)
            frame = stickman.get_frame_preview(idx, "spin", tick, CARD_W)
            if frame:
                pantalla.blit(frame, (cxs, y_card))
            else:
                cc = (220,180,140) if idx==0 else (80,140,220) if idx==1 else (200,80,200)
                pygame.draw.rect(pantalla, cc, (cxs,y_card,CARD_W,CARD_W))

            # Nombre (con espacio generoso arriba del precio)
            tn = self.f_mini.render(nombre, True, (220, 235, 255))
            ty_n = y_card + CARD_W + 10
            pantalla.blit(tn, (cxs + CARD_W//2 - tn.get_width()//2, ty_n))

            # Botón de compra
            by_btn = ty_n + tn.get_height() + 10
            bw_btn = CARD_W + 12
            r_btn  = pygame.Rect(cxs - 6, by_btn, bw_btn, 38)

            if desbloq:
                glass_button(pantalla, self.f_mini, "TUYA", r_btn,
                             tint=(30,130,50), fill_a=35, border_a=110,
                             ct=(120, 255, 140))
            else:
                # Botón con precio en texto ASCII puro
                glass_button(pantalla, self.f_mini, str(precio), r_btn,
                             tint=(80,120,200), fill_a=28, border_a=80,
                             ct=(255, 215, 60))
                # Ícono refresco a la DERECHA del botón (completamente fuera)
                if self.img_ref_s:
                    rx = r_btn.right + 6
                    ry = r_btn.centery - 9
                    pantalla.blit(self.img_ref_s, (rx, ry))

            botones[f'skin_{idx}'] = r_btn

        # ── PowerUps ────────────────────────────────────────────
        y_sep = y_card + CARD_W + 80
        glow_line(pantalla, (70, y_sep), (ANCHO-70, y_sep), GLASS_CYAN, alpha=40)

        tpu = self.f_mini.render("P O W E R  U P S", True, (120, 190, 255))
        pantalla.blit(tpu, (ANCHO//2 - tpu.get_width()//2, y_sep + 8))

        y_pu  = y_sep + 36
        r_pu  = pygame.Rect(ANCHO//2 - 190, y_pu, 380, 50)

        if tiene_segundo_intento:
            glass_button(pantalla, self.f_pequena,
                         "Segundo Intento  ACTIVO", r_pu,
                         tint=(30,130,50), fill_a=35, border_a=110,
                         ct=(120, 255, 140))
        else:
            # Precio como texto ASCII puro, ícono fuera
            glass_button(pantalla, self.f_pequena,
                         f"Segundo Intento   {PRECIO_SEGUNDO_INTENTO}",
                         r_pu, tint=(60, 80, 180), fill_a=28, ct=(240,248,255))
            if self.img_ref_s:
                pantalla.blit(self.img_ref_s, (r_pu.right + 6, r_pu.centery - 9))

        botones['segundo_intento'] = r_pu

        # Volver
        r_vol = pygame.Rect(ANCHO//2 - 95, y_pu + 65, 190, 46)
        glass_button(pantalla, self.f_pequena, "VOLVER", r_vol,
                     tint=(160, 35, 35), fill_a=35, ct=(255, 160, 160))
        botones['volver'] = r_vol

        return botones

    # ── GAME OVER ────────────────────────────────────────────────
    def game_over(self, pantalla, puntuacion=0):
        self._overlay(pantalla)

        # Título con glow rojo
        t = self.f_grande.render("GAME OVER", True, (255, 80, 80))
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 195))
        # Sombra/glow
        ts = self.f_grande.render("GAME OVER", True, (180, 20, 20))
        s  = ts.copy(); s.set_alpha(40)
        pantalla.blit(s, (ANCHO//2 - ts.get_width()//2 + 2, 197))

        p = self.f_mediana.render(f"Puntuacion: {puntuacion}", True, (200, 220, 255))
        pantalla.blit(p, (ANCHO//2 - p.get_width()//2, 278))

        glow_line(pantalla, (200,330),(ANCHO-200,330), GLASS_CYAN, alpha=35)

        rects = self._columna(pantalla, [
            ("REINTENTAR", (40,160,80),  (200,255,220)),
            ("MENU",       (60,100,220), (200,225,255)),
        ], ANCHO//2, 355)
        return {'reintentar':rects[0], 'menu':rects[1]}
