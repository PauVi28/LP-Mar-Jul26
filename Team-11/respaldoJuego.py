#RESPALDO POR SI EL CODIGO SE VA A LA CACA

#PYGAME ES LA LIBRERIA QUE UTILIZAMOS
import pygame
import game_logic
#INICIALIZAR LA LIBRERIA PYGAME
pygame.init()
#ABRIR VENTANA
screen=pygame.display.set_mode((game_logic.ANCHO_VENTANA,game_logic.ALTO_VENTANA))
pygame.display.set_caption("Juego del equipo 11")
clock = pygame.time.Clock()
Run = True
#PANTALLA DE INICIO (Menu)
MenuTime = True
    #TITULO
font_titulo = pygame.font.SysFont("Arial", 80, bold=True)
font_boton  = pygame.font.SysFont("Arial", 50)
    #BOTON
boton = pygame.Rect(game_logic.BOTON_X, game_logic.BOTON_Y, game_logic.ANCHO_BOTON, game_logic.ALTO_BOTON)
#BUCLE PRINCIPAL
while Run:
    for event in pygame.event.get():
        #CERRAR EL JUEGO SI EL USUARIO CLICKEA X O ALT+F4
        if event.type == pygame.QUIT:
            Run=False
        #CLICK IZQUIERDO EN MENU CIERRA EL MENU
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if MenuTime == True and boton.collidepoint(event.pos):
                MenuTime = False
#EN EL MENU
    if MenuTime == True:
        #COLOR DEL FONDO
        screen.fill((20,20,40))
        #TITULO
        titulo = font_titulo.render("JUEGO EQUIPO 11", True, (255,255,100))
        screen.blit(titulo, (game_logic.ANCHO_VENTANA//2 - titulo.get_width()//2, 120))
        #BOTON
        pygame.draw.rect(screen, (0,200,0), boton, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton, width=6, border_radius=12)
        #TEXTO DEL BOTON
        texto_boton = font_boton.render("INICIAR", True, (255, 255, 255))
        screen.blit(texto_boton, 
                    (boton.centerx - texto_boton.get_width()//2,
                     boton.centery - texto_boton.get_height()//2))    
#FUERA DEL MENU
    elif MenuTime == False:
        screen.fill((30, 30, 50))
        #PERSONAJE
        pygame.draw.rect(screen, (255, 0, 0), 
                        (game_logic.PERSONAJE_X_INICIAL, 
                         game_logic.PERSONAJE_Y_INICIAL, 
                         game_logic.ANCHO_PERSONAJE, 
                         game_logic.ALTO_PERSONAJE))
        #JEFE
        pygame.draw.rect(screen, (150, 0, 150), 
                        (game_logic.JEFE_X_INICIAL, 
                         game_logic.JEFE_Y_INICIAL, 
                         game_logic.ANCHO_JEFE, 
                         game_logic.ALTO_JEFE))
        #BARRA DE ACCIONES
        pygame.draw.rect(screen, (20, 20, 30), 
                        (0, game_logic.BARRA_Y, game_logic.ANCHO_BARRA, game_logic.ALTO_BARRA))
        #BOTON ATACAR
        boton_atacar_rect = pygame.Rect(game_logic.BOTON_ATACAR_X, 
                                        game_logic.BOTON_ATACAR_Y, 
                                        game_logic.ANCHO_BOTON_ATACAR, 
                                        game_logic.ALTO_BOTON_ATACAR)

        pygame.draw.rect(screen, (180, 0, 0), boton_atacar_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_atacar_rect, width=6, border_radius=12)

        texto_atacar = font_boton.render("ATACAR", True, (255, 255, 255))
        screen.blit(texto_atacar, 
                    (boton_atacar_rect.centerx - texto_atacar.get_width()//2,
                     boton_atacar_rect.centery - texto_atacar.get_height()//2))
#ACTUALIZAR FOTOGRAMAS
    pygame.display.flip()
    clock.tick(game_logic.FPS)
#CERRAR EL JUEGO
pygame.quit()