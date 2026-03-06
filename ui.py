# ============================================
# ui.py
# ============================================
import pygame
from config import *

class UI:
    def __init__(self):
        self.fg = pygame.font.Font(None,72)
        self.fm = pygame.font.Font(None,48)
        self.fp = pygame.font.Font(None,36)
        self.fs = pygame.font.Font(None,24)
    def menu(self, pantalla, refrescos):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0,0,30,200))
        pantalla.blit(overlay, (0,0))
        t = self.fg.render("Chande-Run", True, DORADO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 150))
        r = self.fm.render(f"🥤 {refrescos}", True, BLANCO)
        pantalla.blit(r, (50,50))
        ops = [("ESPACIO - Jugar", ALTO-150), ("T - Tienda", ALTO-100), ("ESC - Salir", ALTO-50)]
        for txt,y in ops:
            s = self.fp.render(txt, True, BLANCO)
            pantalla.blit(s, (ANCHO//2 - s.get_width()//2, y))
    def hud(self, pantalla, puntuacion, refrescos):
        r = self.fm.render(f"🥤 {refrescos}", True, DORADO)
        pantalla.blit(r, (30,30))
        p = self.fm.render(f"{puntuacion}", True, BLANCO)
        pantalla.blit(p, (ANCHO-150,30))
        # botón salir
        boton = pygame.Rect(ANCHO-120, ALTO-70, 100,50)
        pygame.draw.rect(pantalla, GRIS_OSCURO, boton)
        pygame.draw.rect(pantalla, BLANCO, boton, 3)
        txt = self.fp.render("SALIR", True, ROJO)
        pantalla.blit(txt, (ANCHO-100, ALTO-60))
        return boton
    def pausa(self, pantalla):
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        pantalla.blit(s, (0,0))
        t = self.fg.render("PAUSA", True, BLANCO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 300))
        c = self.fp.render("ESC - Continuar    Q - Salir al menú", True, BLANCO)
        pantalla.blit(c, (ANCHO//2 - c.get_width()//2, 400))
    def tienda(self, pantalla, refrescos):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0,0,30,200))
        pantalla.blit(overlay, (0,0))
        t = self.fg.render("TIENDA", True, DORADO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 100))
        r = self.fm.render(f"Tienes: 🥤 {refrescos}", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 200))
        y = 300
        for pu, precio in PRECIO_POWERUPS.items():
            nom = pu.replace('_',' ').title()
            txt = self.fm.render(f"{nom} : {precio} 🥤", True, BLANCO)
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
            y += 80
        inst = self.fp.render("1 - Comprar   ESC - Volver", True, BLANCO)
        pantalla.blit(inst, (ANCHO//2 - inst.get_width()//2, ALTO-100))
    def game_over(self, pantalla):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        pantalla.blit(overlay, (0,0))
        t = self.fg.render("GAME OVER", True, ROJO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 250))
        r = self.fp.render("R - Reintentar   ESC - Menú", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 400))