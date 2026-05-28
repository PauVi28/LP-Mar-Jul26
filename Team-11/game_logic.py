import pygame

#CONSTANTES

# Ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# Botón Iniciar
ANCHO_BOTON = 300
ALTO_BOTON = 80
BOTON_X = ANCHO_VENTANA // 2 - ANCHO_BOTON // 2
BOTON_Y = ALTO_VENTANA // 2 + 50

# Personaje
ANCHO_PERSONAJE = 40
ALTO_PERSONAJE = 80
PERSONAJE_X_INICIAL = 140
PERSONAJE_Y_INICIAL = ALTO_VENTANA // 2 - 48
# Jefe
ANCHO_JEFE = 55
ALTO_JEFE = 120
JEFE_X_INICIAL = ANCHO_VENTANA - ANCHO_JEFE - 160
JEFE_Y_INICIAL = PERSONAJE_Y_INICIAL + ALTO_PERSONAJE - ALTO_JEFE

# Barra inferior
ANCHO_BARRA = ANCHO_VENTANA
ALTO_BARRA = 90
BARRA_Y = ALTO_VENTANA - ALTO_BARRA

# Botón Atacar
ANCHO_BOTON_ATACAR = 220
ALTO_BOTON_ATACAR = 50
BOTON_ATACAR_X = 60       
BOTON_ATACAR_Y_NORMAL = BARRA_Y + 20
BUTTON_ANIMATION_DURATION = 400

# Vida
MAX_HP_JUGADOR = 100
MAX_HP_JEFE = 120
ANCHO_BARRA_VIDA = 220
ALTO_BARRA_VIDA = 25
JUGADOR_HP_X = 80
JUGADOR_HP_Y = 40
JEFE_HP_X = ANCHO_VENTANA - 300
JEFE_HP_Y = 40

# Cooldowns
TIEMPO_ESPERA_JEFE = 2000
PLAYER_ATTACK_COOLDOWN = 2700
VICTORY_DURATION = 3500

#FUNCIONES

# Fuentes de texto
def create_fonts():
    font_titulo = pygame.font.SysFont("Arial", 80, bold=True)
    font_boton  = pygame.font.SysFont("Arial", 50)
    font_grande = pygame.font.SysFont("Arial", 65, bold=True)
    font_pequeña = pygame.font.SysFont("Arial", 30)
    return font_titulo, font_boton, font_grande, font_pequeña
# Animar el botón de ataque
def get_atacar_button_animation(current_turn, boss_attack_timer):
    current_time = pygame.time.get_ticks()
    if current_turn == "player":
        return BOTON_ATACAR_Y_NORMAL, 255
    else:
        elapsed = current_time - boss_attack_timer
        progress = min(1.0, elapsed / BUTTON_ANIMATION_DURATION)
        y_offset = int(35 * progress)
        alpha = int(255 * (1 - progress))
        current_y = BOTON_ATACAR_Y_NORMAL + y_offset
        return current_y, alpha
# Mostrar el menu en pantalla
def draw_menu(screen, font_titulo, font_boton, boton_iniciar):
    screen.fill((20, 20, 40))
    titulo = font_titulo.render("JUEGO EQUIPO 11", True, (255, 255, 100))
    screen.blit(titulo, (ANCHO_VENTANA//2 - titulo.get_width()//2, 120))

    pygame.draw.rect(screen, (0, 200, 0), boton_iniciar, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), boton_iniciar, width=8, border_radius=12)

    texto_iniciar = font_boton.render("INICIAR", True, (255, 255, 255))
    screen.blit(texto_iniciar, 
                (boton_iniciar.centerx - texto_iniciar.get_width()//2,
                 boton_iniciar.centery - texto_iniciar.get_height()//2))
# Mostrar la batalla en pantalla
def draw_battle(screen, font_boton, font_pequeña, boton_atacar_rect, 
                player_hp, boss_hp, current_turn, boss_attack_timer):
    screen.fill((30, 30, 50))

    # Personajes
    pygame.draw.rect(screen, (255, 0, 0), 
                    (PERSONAJE_X_INICIAL, PERSONAJE_Y_INICIAL, ANCHO_PERSONAJE, ALTO_PERSONAJE))
    pygame.draw.rect(screen, (150, 0, 150), 
                    (JEFE_X_INICIAL, JEFE_Y_INICIAL, ANCHO_JEFE, ALTO_JEFE))

    # Barras de vida
    pygame.draw.rect(screen, (80, 80, 80), (JUGADOR_HP_X, JUGADOR_HP_Y, ANCHO_BARRA_VIDA, ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (0, 220, 0), 
                    (JUGADOR_HP_X, JUGADOR_HP_Y, ANCHO_BARRA_VIDA * (player_hp / MAX_HP_JUGADOR), ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (80, 80, 80), (JEFE_HP_X, JEFE_HP_Y, ANCHO_BARRA_VIDA, ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (220, 0, 0), 
                    (JEFE_HP_X, JEFE_HP_Y, ANCHO_BARRA_VIDA * (boss_hp / MAX_HP_JEFE), ALTO_BARRA_VIDA))

    # Barra inferior
    pygame.draw.rect(screen, (20, 20, 30), (0, BARRA_Y, ANCHO_BARRA, ALTO_BARRA))

    # Botón de atacar
    current_y, alpha = get_atacar_button_animation(current_turn, boss_attack_timer)
    boton_atacar_rect.y = current_y

    color_fondo = (180, 0, 0) if alpha > 100 else (100, 0, 0)
    pygame.draw.rect(screen, color_fondo, boton_atacar_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), boton_atacar_rect, width=8, border_radius=12)

    texto_atacar = font_boton.render("ATACAR", True, (255, 255, 255))
    texto_atacar.set_alpha(alpha)
    screen.blit(texto_atacar, 
                (boton_atacar_rect.centerx - texto_atacar.get_width()//2,
                 boton_atacar_rect.centery - texto_atacar.get_height()//2))

    # Texto de turno
    if current_turn == "player":
        turno_texto = font_pequeña.render("TU TURNO - Presiona ENTER para atacar", True, (255, 255, 100))
    else:
        turno_texto = font_pequeña.render("TURNO DEL JEFE", True, (255, 100, 100))
    screen.blit(turno_texto, (ANCHO_VENTANA//2 - turno_texto.get_width()//2, 15))
# Texto de victoria
def draw_victory(screen, font_grande, victory_start_time):
    screen.fill((30, 30, 50))
    pygame.draw.rect(screen, (255, 0, 0), 
                    (PERSONAJE_X_INICIAL, PERSONAJE_Y_INICIAL, ANCHO_PERSONAJE, ALTO_PERSONAJE))
    pygame.draw.rect(screen, (150, 0, 150), 
                    (JEFE_X_INICIAL, JEFE_Y_INICIAL, ANCHO_JEFE, ALTO_JEFE))

    tiempo = pygame.time.get_ticks() - victory_start_time
    alpha = max(0, 255 - int((tiempo / VICTORY_DURATION) * 255))
    
    texto_victoria = font_grande.render("JEFE DERROTADO", True, (255, 255, 100))
    texto_victoria.set_alpha(alpha)
    screen.blit(texto_victoria, (ANCHO_VENTANA//2 - texto_victoria.get_width()//2, 200))

    return tiempo >= VICTORY_DURATION
# Ataque del jugador
def player_attack(boss_hp):
    boss_hp -= 20
    if boss_hp < 0: boss_hp = 0
    return boss_hp
# Ataque del jefe
def boss_attack(player_hp):
    player_hp -= 15
    if player_hp < 0: player_hp = 0
    return player_hp
# Resetear el juego
def reset_game():
    return (MAX_HP_JUGADOR, MAX_HP_JEFE, "player", 0, 0)