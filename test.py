import pygame
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Prueba")
reloj = pygame.time.Clock()

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    pantalla.fill((255,255,255))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()