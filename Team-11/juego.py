#PYGAME ES LA LIBRERÍA QUE VAMOS A UTILIZAR
import pygame
import game_logic
#INICIALIZAR PYGAME
pygame.init()
#DESACTIVAR LA VISUALIZACIÓN DEL MOUSE
pygame.mouse.set_visible(False)
#INICIAR LA PANTALLA DEL JUEGO
screen = pygame.display.set_mode((game_logic.ANCHO_VENTANA, game_logic.ALTO_VENTANA))
#EL NOMBRE DEL JUEGO
pygame.display.set_caption("Juego del equipo 11")
#FUNCIÓN PARA ACTUALIZAR LOS TICKS DE LA PANTALLA
clock = pygame.time.Clock()
#CREAR LAS FUENTES DEL TEXTO
font_titulo, font_boton, font_grande, font_pequeña = game_logic.create_fonts()
#BOTON EN EL MENU PARA INICIAR EL JUEGO
boton_iniciar = pygame.Rect(game_logic.BOTON_X, game_logic.BOTON_Y, 
                           game_logic.ANCHO_BOTON, game_logic.ALTO_BOTON)
#BOTON DE ATACAR
boton_atacar_rect = pygame.Rect(game_logic.BOTON_ATACAR_X, game_logic.BOTON_ATACAR_Y_NORMAL,
                               game_logic.ANCHO_BOTON_ATACAR, game_logic.ALTO_BOTON_ATACAR)

#VARIABLES FUNCIONALES
Run = True
menu_state = True
player_hp = game_logic.MAX_HP_JUGADOR
boss_hp = game_logic.MAX_HP_JEFE
current_turn = "player"
boss_attack_timer = 0
last_player_attack_time = 0
victory_start_time = 0

#BUCLE PRINCIPAL
while Run:
    #REVISAR CADA EVENTO DENTRO DEL JUEGO
    for event in pygame.event.get():
        #SI EL JUGADOR PRESIONA LA X O ALT+F4 CERRAR EL JUEGO
        if event.type == pygame.QUIT:
            Run = False
        #PRESIONAR ENTER PARA EMPEZAR EL JUEGO
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if menu_state == True:
                menu_state = False
                player_hp, boss_hp, current_turn, boss_attack_timer, last_player_attack_time = game_logic.reset_game()
            #PRESIONAR ENTER PARA ATACAR
            elif menu_state == False and current_turn == "player":
                current_time = pygame.time.get_ticks()
                if current_time - last_player_attack_time >= game_logic.PLAYER_ATTACK_COOLDOWN:
                    boss_hp = game_logic.player_attack(boss_hp)
                    current_turn = "boss"
                    boss_attack_timer = current_time
                    last_player_attack_time = current_time
    #MOSTRAR EL MENU EN LA PANTALLA
    if menu_state == True:
        game_logic.draw_menu(screen, font_titulo, font_boton, boton_iniciar)
    #MOSTRAR LA PELEA EN PANTALLA
    elif menu_state == False:
        game_logic.draw_battle(screen, font_boton, font_pequeña, boton_atacar_rect,
                              player_hp, boss_hp, current_turn, boss_attack_timer)
        #ATAQUE DEL JEFE
        if current_turn == "boss":
            if pygame.time.get_ticks() - boss_attack_timer >= game_logic.TIEMPO_ESPERA_JEFE:
                player_hp = game_logic.boss_attack(player_hp)
                current_turn = "player"
        #MUERTE DEL JEFE
        if boss_hp <= 0:
            menu_state = "victory"
            victory_start_time = pygame.time.get_ticks()
    #MENSAJE DE VICTORIA
    elif menu_state == "victory":
        if game_logic.draw_victory(screen, font_grande, victory_start_time):
            menu_state = True
            player_hp, boss_hp, current_turn, boss_attack_timer, last_player_attack_time = game_logic.reset_game()
    #ACTUALIZAR LA FRECUENCIA DE LOS FOTOGRAMAS
    pygame.display.flip()
    clock.tick(game_logic.FPS)
#CERRAR EL JUEGO
pygame.quit()