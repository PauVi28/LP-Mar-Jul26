import pygame

pygame.font.init()

fuente_titulo = pygame.font.SysFont("arial", 52)
fuente_menu = pygame.font.SysFont("arial", 28)

COLOR_FONDO = (18, 18, 28)
COLOR_TEXTO = (240, 240, 240)
COLOR_CARTA = (230, 220, 200)

def mostrar_menu(pantalla):
    titulo = fuente_titulo.render("40 ECUADOR", True,COLOR_TEXTO)
    pantalla.blit(titulo, (450, 80))
    opciones = ["1. Modo Local","2. Multijugador LAN","3. Configuracion","4. Salir"]
    
    y = 250

    for opcion in opciones:
        texto = fuente_menu.render(opcion,True,COLOR_TEXTO)
        pantalla.blit(texto, (520, y))
        y += 60

    dibujar_cartas_demo(pantalla)

def dibujar_cartas_demo(pantalla):
    for i in range(5):
        x = 300 + (i * 140)
        pygame.draw.rect(pantalla,COLOR_CARTA,(x, 500, 100, 150),border_radius=12)

        pygame.draw.rect(pantalla,(0, 0, 0),(x, 500, 100, 150),3,border_radius=12)
