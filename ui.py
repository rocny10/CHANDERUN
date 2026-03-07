# ============================================
# ui.py - VERSIÓN FINAL
# ============================================
import pygame
import os
from config import *

class UI:
    def __init__(self):
        if os.path.exists(FUENTE_TTF):
            self.fuente_grande = pygame.font.Font(FUENTE_TTF, 80)
            self.fuente_mediana = pygame.font.Font(FUENTE_TTF, 48)
            self.fuente_pequena = pygame.font.Font(FUENTE_TTF, 36)
            print("✅ Fuente personalizada cargada")
        else:
            self.fuente_grande = pygame.font.Font(None, 80)
            self.fuente_mediana = pygame.font.Font(None, 48)
            self.fuente_pequena = pygame.font.Font(None, 36)

        self.logo = None
        try:
            logo_img = pygame.image.load("assets/logo.png").convert_alpha()
            logo_ancho = 400
            logo_alto = int(logo_img.get_height() * (logo_ancho / logo_img.get_width()))
            self.logo = pygame.transform.scale(logo_img, (logo_ancho, logo_alto))
            print("✅ Logo cargado")
        except:
            print("⚠️ No se encontró assets/logo.png, usando texto")

    def desenfocar(self, pantalla, factor=6):
        tamaño_peq = (ANCHO // factor, ALTO // factor)
        superficie_peq = pygame.transform.smoothscale(pantalla, tamaño_peq)
        superficie_grande = pygame.transform.smoothscale(superficie_peq, (ANCHO, ALTO))
        return superficie_grande

    def dibujar_boton(self, pantalla, texto, rect, es_salir=False):
        color = (150,50,50) if es_salir else (60,60,80)
        borde = (255,100,100) if es_salir else (180,180,220)
        pygame.draw.rect(pantalla, color, rect, border_radius=15)
        pygame.draw.rect(pantalla, borde, rect, 4, border_radius=15)

        sup = self.fuente_pequena.render(texto, True, BLANCO)
        x = rect.centerx - sup.get_width()//2
        y = rect.centery - sup.get_height()//2
        pantalla.blit(sup, (x, y))

    def menu(self, pantalla, refrescos, stickman):
        x_original = stickman.x
        y_original = stickman.y
        
        fondo_actual = pantalla.copy()
        fondo_desenfocado = self.desenfocar(fondo_actual)
        pantalla.blit(fondo_desenfocado, (0,0))
        
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 180))
        pantalla.blit(overlay, (0,0))

        # LOGO A LA IZQUIERDA
        if self.logo:
            x_logo = 100
            y_logo = 80
            pantalla.blit(self.logo, (x_logo, y_logo))
        else:
            titulo = self.fuente_grande.render("Chande-Run", True, DORADO)
            pantalla.blit(titulo, (100, 100))

        # Mostrar refrescos arriba derecha
        texto_refrescos = self.fuente_mediana.render(f"🥤 {refrescos}", True, DORADO)
        pantalla.blit(texto_refrescos, (ANCHO - 150, 50))

        # PERSONAJE EN IDLE
        stickman.x = 500
        stickman.y = SUELO_Y
        stickman.set_animacion("idle")
        stickman.dibujar(pantalla)

        # BOTONES A LA DERECHA
        boton_ancho = 300
        boton_alto = 70
        espacio = 25
        x_botones = ANCHO - 450
        y_inicio = 350

        boton_jugar = pygame.Rect(x_botones, y_inicio, boton_ancho, boton_alto)
        boton_tienda = pygame.Rect(x_botones, y_inicio + boton_alto + espacio, boton_ancho, boton_alto)
        boton_salir = pygame.Rect(x_botones, y_inicio + (boton_alto + espacio) * 2, boton_ancho, boton_alto)

        self.dibujar_boton(pantalla, "JUGAR (ESPACIO)", boton_jugar)
        self.dibujar_boton(pantalla, "TIENDA (T)", boton_tienda)
        self.dibujar_boton(pantalla, "SALIR (ESC)", boton_salir, es_salir=True)

        stickman.x = x_original
        stickman.y = y_original

        return boton_jugar, boton_tienda, boton_salir

    def hud(self, pantalla, puntuacion, refrescos):
        r = self.fuente_mediana.render(f"🥤 {refrescos}", True, DORADO)
        pantalla.blit(r, (30, 30))
        p = self.fuente_mediana.render(f"{puntuacion}", True, BLANCO)
        pantalla.blit(p, (ANCHO - 150, 30))

    def pausa(self, pantalla):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        pantalla.blit(overlay, (0,0))

        t = self.fuente_grande.render("PAUSA", True, BLANCO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 200))

        centro_x = ANCHO // 2
        boton_ancho = 300
        boton_alto = 70
        espacio = 20
        y_inicio = 350

        boton_cont = pygame.Rect(centro_x - boton_ancho//2, y_inicio, boton_ancho, boton_alto)
        boton_menu = pygame.Rect(centro_x - boton_ancho//2, y_inicio + boton_alto + espacio, boton_ancho, boton_alto)
        boton_salir = pygame.Rect(centro_x - boton_ancho//2, y_inicio + (boton_alto + espacio) * 2, boton_ancho, boton_alto)

        self.dibujar_boton(pantalla, "Continuar", boton_cont)
        self.dibujar_boton(pantalla, "Menú Principal", boton_menu)
        self.dibujar_boton(pantalla, "Salir del Juego", boton_salir, es_salir=True)

        return boton_cont, boton_menu, boton_salir

    def tienda(self, pantalla, refrescos):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 230))
        pantalla.blit(overlay, (0,0))

        t = self.fuente_grande.render("TIENDA", True, DORADO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 100))

        r = self.fuente_mediana.render(f"Tienes: 🥤 {refrescos}", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 200))

        y = 300
        for pu, precio in PRECIO_POWERUPS.items():
            nom = pu.replace('_',' ').title()
            txt = self.fuente_mediana.render(f"{nom} : {precio} 🥤", True, BLANCO)
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
            y += 80

        inst = self.fuente_pequena.render("1 - Comprar   ESC - Volver", True, BLANCO)
        pantalla.blit(inst, (ANCHO//2 - inst.get_width()//2, ALTO - 100))

    def game_over(self, pantalla):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        pantalla.blit(overlay, (0,0))

        t = self.fuente_grande.render("GAME OVER", True, ROJO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 250))

        r = self.fuente_pequena.render("R - Reintentar   ESC - Menú", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 400))