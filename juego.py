#juego.py
import pygame
import sys
import random

from game_logic import Particula, Obstaculo, Nitro, Carro

pygame.init()

# ── Pantalla ─────────────────────────────────────────────
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("FuriosCar2D - Modo Local")
reloj = pygame.time.Clock()

# ── Colores ──────────────────────────────────────────────
NEGRO        = (0,   0,   0)
BLANCO       = (255, 255, 255)
GRIS         = (65,  65,  65)
GRIS_OSCURO  = (20,  20,  20)
GRIS_MED     = (100, 100, 100)
ROJO         = (230, 30,  30)
ROJO_OSC     = (150, 0,   0)
AZUL         = (0,   100, 255)
AZUL_OSC     = (0,   50,  160)
VERDE        = (0,   220, 80)
AMARILLO     = (255, 220, 0)
NARANJA      = (255, 140, 0)
CELESTE      = (100, 200, 255)

# ── Fuentes ──────────────────────────────────────────────
fuente_hud    = pygame.font.SysFont("Arial", 26, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 54, bold=True)
fuente_med    = pygame.font.SysFont("Arial", 30, bold=True)
fuente_peq    = pygame.font.SysFont("Arial", 20)

# ── Pista ────────────────────────────────────────────────
PISTA_IZQ   = 175   
PISTA_DER   = 725   
PISTA_ANCHO = PISTA_DER - PISTA_IZQ   
MITAD       = (PISTA_IZQ + PISTA_DER) // 2  

CARRIL1_IZQ = PISTA_IZQ + 8
CARRIL1_DER = MITAD - 8
CARRIL2_IZQ = MITAD + 8
CARRIL2_DER = PISTA_DER - 8
CARRIL_ANCHO = CARRIL1_DER - CARRIL1_IZQ   
BARANDA_W   = 22

DURACION    = 60   
VEL_BASE    = 4    
CAR_W, CAR_H = 46, 84

road_offset      = 0    
baranda_offset   = 0    
STRIPE_SPACE     = 55   

MENU    = "menu"
JUGANDO = "jugando"
FIN     = "fin"

estado          = MENU
ganador          = ""
j1 = j2          = None
obstaculos      = []
tiempo_inicio   = 0
spawn_timer      = 0
vel_actual      = VEL_BASE
score1 = score2 = 0     
particles_fondo = []    
nitros = []
nitro_activo = False
nitro_timer = 0

def reset():
    global j1, j2, obstaculos, tiempo_inicio, road_offset
    global spawn_timer, vel_actual, ganador, score1, score2, particles_fondo
    global nitros, nitro_activo, nitro_timer

    j1 = Carro(CARRIL1_IZQ + (CARRIL_ANCHO - CAR_W) // 2, ALTO - CAR_H - 30, ROJO, ROJO_OSC, CARRIL1_IZQ, CARRIL1_DER)
    j2 = Carro(CARRIL2_IZQ + (CARRIL_ANCHO - CAR_W) // 2, ALTO - CAR_H - 30, AZUL, AZUL_OSC, CARRIL2_IZQ, CARRIL2_DER)
    obstaculos      = []
    road_offset     = 0
    spawn_timer      = 0
    vel_actual      = VEL_BASE
    ganador          = ""
    score1          = 0
    score2          = 0
    particles_fondo = []
    nitros = []
    nitro_activo = False
    nitro_timer = 0

reset()

def dibujar_pista(vel):
    global road_offset, baranda_offset
    road_offset    = (road_offset    + vel) % STRIPE_SPACE
    baranda_offset = (baranda_offset + vel) % 50

    pygame.draw.rect(pantalla, GRIS, (PISTA_IZQ, 0, PISTA_ANCHO, ALTO))
    pygame.draw.rect(pantalla, (55, 55, 55), (PISTA_IZQ, 0, 12, ALTO))
    pygame.draw.rect(pantalla, (55, 55, 55), (PISTA_DER - 12, 0, 12, ALTO))
    pygame.draw.rect(pantalla, BLANCO, (PISTA_IZQ - BARANDA_W, 0, BARANDA_W, ALTO))
    pygame.draw.rect(pantalla, BLANCO, (PISTA_DER, 0, BARANDA_W, ALTO))

    for i in range(-1, ALTO // 50 + 2):
        yo = i * 50 + int(baranda_offset)
        pygame.draw.rect(pantalla, NEGRO, (PISTA_IZQ - BARANDA_W, yo, BARANDA_W, 14))
        pygame.draw.rect(pantalla, NEGRO, (PISTA_DER, yo, BARANDA_W, 14))

    for i in range(-1, ALTO // STRIPE_SPACE + 2):
        yo = i * STRIPE_SPACE + int(road_offset)
        pygame.draw.rect(pantalla, BLANCO, (MITAD - 4, yo, 8, 32))

    pygame.draw.rect(pantalla, (90, 90, 90), (MITAD - 1, 0, 2, ALTO))

def dibujar_hud(tiempo_restante, j1_vivo, j2_vivo):
    seg = int(tiempo_restante)
    pygame.draw.rect(pantalla, (10, 10, 10), (0, 0, ANCHO, 52))
    pygame.draw.line(pantalla, AMARILLO, (0, 52), (ANCHO, 52), 2)

    col_t = VERDE if seg > 15 else (AMARILLO if seg > 5 else ROJO)
    timer_txt = fuente_med.render(f"⏱  {seg:02d}s", True, col_t)
    pantalla.blit(timer_txt, (ANCHO//2 - timer_txt.get_width()//2, 10))

    col1 = ROJO if j1_vivo else GRIS_MED
    t1   = fuente_hud.render(f"J1  {score1} obs", True, col1)
    pantalla.blit(t1, (20, 13))
    if not j1_vivo:
        pantalla.blit(fuente_peq.render("ELIMINADO", True, ROJO), (20, 36))

    col2 = AZUL if j2_vivo else GRIS_MED
    t2   = fuente_hud.render(f"J2  {score2} obs", True, col2)
    pantalla.blit(t2, (ANCHO - t2.get_width() - 20, 13))
    if not j2_vivo:
        ex = fuente_peq.render("ELIMINADO", True, ROJO)
        pantalla.blit(ex, (ANCHO - ex.get_width() - 20, 36))

def dibujar_menu():
    pantalla.fill(GRIS_OSCURO)
    dibujar_pista(3)
    ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 170))
    pantalla.blit(ov, (0, 0))

    t = fuente_grande.render("FURIOSCAR 2D", True, ROJO)
    sombra = fuente_grande.render("FURIOSCAR 2D", True, (80, 0, 0))
    pantalla.blit(sombra, (ANCHO//2 - t.get_width()//2 + 3, 108))
    pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 105))

    sub = fuente_med.render("¡Esquiva los obstáculos por 60 segundos!", True, AMARILLO)
    pantalla.blit(sub, (ANCHO//2 - sub.get_width()//2, 180))

    pygame.draw.rect(pantalla, (30, 30, 30), (220, 240, 460, 160), border_radius=12)
    pygame.draw.rect(pantalla, GRIS_MED,    (220, 240, 460, 160), 2, border_radius=12)

    lineas = [
        ("Jugador 1 (ROJO) — carril izquierdo: A / D",  ROJO),
        ("Jugador 2 (AZUL) — carril derecho:   ← / →", AZUL),
        ("Esquiva los coches que vienen de frente.",     BLANCO),
        ("Gana quien sobreviva más tiempo.",             VERDE),
    ]
    for i, (txt, col) in enumerate(lineas):
        pantalla.blit(fuente_peq.render(txt, True, col), (240, 255 + i * 33))

    boton = fuente_med.render("▶️  PRESIONA  ESPACIO", True, NEGRO)
    bw, bh = boton.get_width() + 40, boton.get_height() + 16
    bx = ANCHO//2 - bw//2
    pygame.draw.rect(pantalla, AMARILLO, (bx, 425, bw, bh), border_radius=10)
    pantalla.blit(boton, (bx+20, 433))

def dibujar_fin():
    pantalla.fill(GRIS_OSCURO)
    dibujar_pista(0)
    ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 180))
    pantalla.blit(ov, (0, 0))

    color_g = AMARILLO if "EMPATE" in ganador else VERDE
    t = fuente_grande.render(ganador, True, color_g)
    pantalla.blit(fuente_grande.render(ganador, True, (0, 0, 0)), (ANCHO//2 - t.get_width()//2 + 3, 203))
    pantalla.blit(t,      (ANCHO//2 - t.get_width()//2,     200))

    s1 = fuente_med.render(f"Jugador 1 esquivó {score1} coches", True, ROJO)
    s2 = fuente_med.render(f"Jugador 2 esquivó {score2} coches", True, AZUL)
    pantalla.blit(s1, (ANCHO//2 - s1.get_width()//2, 285))
    pantalla.blit(s2, (ANCHO//2 - s2.get_width()//2, 325))

    r = fuente_med.render("R  →  Menú principal", True, BLANCO)
    pygame.draw.rect(pantalla, (30,30,30), (ANCHO//2 - r.get_width()//2 - 20, 395, r.get_width()+40, r.get_height()+16), border_radius=8)
    pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 403))

# ─── BUCLE PRINCIPAL ──────────────────────────────────────
while True:
    reloj.tick(60)
    pantalla.fill(GRIS_OSCURO)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            if estado == MENU and ev.key == pygame.K_SPACE:
                reset()
                tiempo_inicio = pygame.time.get_ticks()
                estado = JUGANDO
            if estado == FIN and ev.key == pygame.K_r:
                estado = MENU

    if estado == MENU:
        dibujar_menu()
    elif estado == JUGANDO:
        tiempo_ms      = pygame.time.get_ticks() - tiempo_inicio
        tiempo_seg     = tiempo_ms / 1000.0
        tiempo_restante = max(0.0, DURACION - tiempo_seg)
        vel_actual = VEL_BASE + (tiempo_seg * 0.18)

        usando_nitro = False
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_z] and nitro_activo and nitro_timer > 0:
            usando_nitro = True
            nitro_timer -= 1

        velocidad_render = vel_actual + 8 if usando_nitro else vel_actual
        dibujar_pista(velocidad_render)

        spawn_timer += 1
        intervalo_spawn = max(35, 85 - int(tiempo_seg * 0.7))
        if spawn_timer >= intervalo_spawn:
            spawn_timer = 0
            obstaculos.append(Obstaculo(random.choice([1, 2])))
            if random.random() < 0.25:
                nitros.append(Nitro())

        for obs in obstaculos[:]:
            obs.mover(velocidad_render)
            obs.dibujar(pantalla)
            if j1.vivo and j1.rect_col().colliderect(obs.rect_col()):
                j1.vivo = False
                j1.explotar()
            if j2.vivo and j2.rect_col().colliderect(obs.rect_col()):
                j2.vivo = False
                j2.explotar()
            if obs.fuera():
                obstaculos.remove(obs)
                if obs.carril == 1 and j1.vivo: score1 += 1
                if obs.carril == 2 and j2.vivo: score2 += 1

        for nitro in nitros[:]:
            nitro.mover(velocidad_render)
            nitro.dibujar(pantalla)
            if j1.vivo and j1.rect_col().colliderect(nitro.rect_col()):
                nitro_activo = True
                nitro_timer = 180
                nitros.remove(nitro)
            elif j2.vivo and j2.rect_col().colliderect(nitro.rect_col()):
                nitro_activo = True
                nitro_timer = 180
                nitros.remove(nitro)
            elif nitro.fuera():
                nitros.remove(nitro)

        if j1.vivo and random.random() < 0.4:
            particles_fondo.append(Particula(int(j1.x+10), int(j1.y+CAR_H+2), (160,160,160)))
            particles_fondo.append(Particula(int(j1.x+CAR_W-10), int(j1.y+CAR_H+2), (160,160,160)))
        if j2.vivo and random.random() < 0.4:
            particles_fondo.append(Particula(int(j2.x+10), int(j2.y+CAR_H+2), (160,160,160)))
            particles_fondo.append(Particula(int(j2.x+CAR_W-10), int(j2.y+CAR_H+2), (160,160,160)))

        for p in particles_fondo[:]:
            p.actualizar()
            p.dibujar(pantalla)
            if p.vida <= 0: particles_fondo.remove(p)

        teclas = pygame.key.get_pressed()
        if j1.vivo:
            if teclas[pygame.K_a]: j1.mover(-1)
            if teclas[pygame.K_d]: j1.mover(1)
        if j2.vivo:
            if teclas[pygame.K_LEFT]: j2.mover(-1)
            if teclas[pygame.K_RIGHT]: j2.mover(1)

        j1.dibujar(pantalla)
        j2.dibujar(pantalla)
        j1.actualizar_particulas()
        j2.actualizar_particulas()

        dibujar_hud(tiempo_restante, j1.vivo, j2.vivo)

        vel_pct = min(1.0, (vel_actual - VEL_BASE) / 6)
        pygame.draw.rect(pantalla, (40,40,40), (ANCHO//2-100//2, 56, 100, 6))
        pygame.draw.rect(pantalla, NARANJA,    (ANCHO//2-100//2, 56, int(100*vel_pct), 6))

        if nitro_activo:
            pygame.draw.rect(pantalla, (40,40,40), (20, 60, 140, 12))
            pygame.draw.rect(pantalla, CELESTE, (20, 60, int((nitro_timer / 180) * 140), 12))
            pantalla.blit(fuente_peq.render("NITRO (Z)", True, BLANCO), (20, 75))

        if tiempo_restante <= 0 or (not j1.vivo and not j2.vivo):
            if j1.vivo and j2.vivo:
                ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
            elif j1.vivo and not j2.vivo: ganador = "¡JUGADOR 1 GANA!"
            elif j2.vivo and not j1.vivo: ganador = "¡JUGADOR 2 GANA!"
            else:
                ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
            estado = FIN

    elif estado == FIN:
        dibujar_fin()

    pygame.display.update()