import pygame
import sys
import socket
import threading
import random
from game_logic import Particula, Obstaculo, Nitro, Carro

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("FuriosCar2D - Modo Red")
reloj = pygame.time.Clock()

NEGRO, BLANCO, GRIS, GRIS_OSCURO, GRIS_MED = (0,0,0), (255,255,255), (65,65,65), (20,20,20), (100,100,100)
ROJO, ROJO_OSC, AZUL, AZUL_OSC, VERDE, AMARILLO, NARANJA, CELESTE = (230,30,30), (150,0,0), (0,100,255), (0,50,160), (0,220,80), (255,220,0), (255,140,0), (100,200,255)

fuente_hud = pygame.font.SysFont("Arial", 26, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 54, bold=True)
fuente_med = pygame.font.SysFont("Arial", 30, bold=True)
fuente_peq = pygame.font.SysFont("Arial", 20)

PISTA_IZQ, PISTA_DER, BARANDA_W, STRIPE_SPACE = 175, 725, 22, 55
PISTA_ANCHO = PISTA_DER - PISTA_IZQ
MITAD = (PISTA_IZQ + PISTA_DER) // 2
CARRIL1_IZQ, CARRIL1_DER = PISTA_IZQ + 8, MITAD - 8
CARRIL2_IZQ, CARRIL2_DER = MITAD + 8, PISTA_DER - 8
CAR_W, CAR_H = 46, 84

road_offset = 0
baranda_offset = 0
particles_fondo = []

datos_servidor = "menu,60.0,4.0,0,1,0,1,0,0,0,0,,NONE,NONE"

j1 = Carro(0, ALTO - CAR_H - 30, ROJO, ROJO_OSC, CARRIL1_IZQ, CARRIL1_DER)
j2 = Carro(0, ALTO - CAR_H - 30, AZUL, AZUL_OSC, CARRIL2_IZQ, CARRIL2_DER)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
mi_id = int(client_socket.recv(1024).decode('utf-8'))
print(f"Conectado como el Jugador {mi_id + 1}")

def recibir_datos():
    global datos_servidor
    buffer = ""
    while True:
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data: break
            buffer += data
            if "\n" in buffer:
                lineas = buffer.split("\n")
                datos_servidor = lineas[-2]
                buffer = lineas[-1]
        except:
            break

threading.Thread(target=recibir_datos, daemon=True).start()

def dibujar_pista(vel):
    global road_offset, baranda_offset
    road_offset = (road_offset + vel) % STRIPE_SPACE
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

def dibujar_hud(tiempo_restante, score1, score2, j1_vivo, j2_vivo):
    seg = int(float(tiempo_restante))
    pygame.draw.rect(pantalla, (10, 10, 10), (0, 0, ANCHO, 52))
    pygame.draw.line(pantalla, AMARILLO, (0, 52), (ANCHO, 52), 2)
    col_t = VERDE if seg > 15 else (AMARILLO if seg > 5 else ROJO)
    timer_txt = fuente_med.render(f"⏱  {seg:02d}s", True, col_t)
    pantalla.blit(timer_txt, (ANCHO//2 - timer_txt.get_width()//2, 10))

    t1 = fuente_hud.render(f"J1  {score1} obs", True, ROJO if j1_vivo else GRIS_MED)
    pantalla.blit(t1, (20, 13))
    if not j1_vivo: pantalla.blit(fuente_peq.render("ELIMINADO", True, ROJO), (20, 36))

    t2 = fuente_hud.render(f"J2  {score2} obs", True, AZUL if j2_vivo else GRIS_MED)
    pantalla.blit(t2, (ANCHO - t2.get_width() - 20, 13))
    if not j2_vivo: pantalla.blit(fuente_peq.render("ELIMINADO", True, ROJO), (ANCHO - 130, 36))

while True:
    reloj.tick(60)
    pantalla.fill(GRIS_OSCURO)

    try:
        partes = datos_servidor.split(",")
        estado_net = partes[0]
        tiempo_net = partes[1]
        vel_net = float(partes[2])
        j1.x = float(partes[3])
        was_vivo1 = j1.vivo; j1.vivo = bool(int(partes[4]))
        j2.x = float(partes[5])
        was_vivo2 = j2.vivo; j2.vivo = bool(int(partes[6]))
        score1_net = int(partes[7])
        score2_net = int(partes[8])
        nitro_act_net = bool(int(partes[9]))
        nitro_time_net = int(partes[10])
        ganador_net = partes[11]
        obs_string = partes[12]
        nitros_string = partes[13]

        if was_vivo1 and not j1.vivo: j1.explotar()
        if was_vivo2 and not j2.vivo: j2.explotar()
    except:
        continue

    teclas = pygame.key.get_pressed()
    string_envio = "NONE"

    if estado_net == "menu":
        if mi_id == 0 and teclas[pygame.K_SPACE]: string_envio = "START"
    elif estado_net == "jugando":
        inputs = []
        if mi_id == 0:
            if teclas[pygame.K_a]: inputs.append("A")
            if teclas[pygame.K_d]: inputs.append("D")
        else:
            if teclas[pygame.K_LEFT]: inputs.append("LEFT")
            if teclas[pygame.K_RIGHT]: inputs.append("RIGHT")
        if teclas[pygame.K_z]: inputs.append("Z")
        if inputs: string_envio = "+".join(inputs)
    elif estado_net == "fin":
        if teclas[pygame.K_r]: string_envio = "RESET"

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    try:
        client_socket.send(string_envio.encode('utf-8'))
    except:
        pass

    if estado_net == "menu":
        dibujar_pista(3)
        ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA); ov.fill((0, 0, 0, 170)); pantalla.blit(ov, (0, 0))
        t = fuente_grande.render("FURIOSCAR 2D (RED)", True, ROJO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 105))

        txt_rol = f"Eres el JUGADOR {mi_id + 1}"
        render_rol = fuente_med.render(txt_rol, True, ROJO if mi_id == 0 else AZUL)
        pantalla.blit(render_rol, (ANCHO//2 - render_rol.get_width()//2, 180))

        sub = fuente_med.render("Esperando al rival para iniciar...", True, AMARILLO)
        pantalla.blit(sub, (ANCHO//2 - sub.get_width()//2, 240))
        if mi_id == 0:
            boton = fuente_med.render("PRESIONA ESPACIO PARA ARRANCAR", True, NEGRO)
            pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2-boton.get_width()//2-20, 425, boton.get_width()+40, 50), border_radius=10)
            pantalla.blit(boton, (ANCHO//2-boton.get_width()//2, 433))

    elif estado_net == "jugando":
        dibujar_pista(vel_net)

        # FIX: ahora se parsea carril:x:y en lugar de carril:y
        if obs_string != "NONE":
            for obs_data in obs_string.split("/"):
                carril_o, x_o, y_o = map(float, obs_data.split(":"))
                obs_temp = Obstaculo(int(carril_o))
                obs_temp.x = x_o   # posición x fija del servidor, no aleatoria
                obs_temp.y = y_o
                obs_temp.dibujar(pantalla)

        if nitros_string != "NONE":
            for nitro_data in nitros_string.split("/"):
                x_n, y_n = map(float, nitro_data.split(":"))
                nitro_temp = Nitro()
                nitro_temp.x = x_n; nitro_temp.y = y_n
                nitro_temp.dibujar(pantalla)

        if j1.vivo and random.random() < 0.2:
            particles_fondo.append(Particula(int(j1.x+10), int(j1.y+CAR_H+2), (160,160,160)))
        if j2.vivo and random.random() < 0.2:
            particles_fondo.append(Particula(int(j2.x+10), int(j2.y+CAR_H+2), (160,160,160)))

        for p in particles_fondo[:]:
            p.actualizar(); p.dibujar(pantalla)
            if p.vida <= 0: particles_fondo.remove(p)

        j1.actualizar_particulas(); j2.actualizar_particulas()
        j1.dibujar(pantalla); j2.dibujar(pantalla)
        dibujar_hud(tiempo_net, score1_net, score2_net, j1.vivo, j2.vivo)

        if nitro_act_net:
            pygame.draw.rect(pantalla, (40,40,40), (20, 60, 140, 12))
            pygame.draw.rect(pantalla, CELESTE, (20, 60, int((nitro_time_net / 180) * 140), 12))

    elif estado_net == "fin":
        dibujar_pista(0)
        ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA); ov.fill((0, 0, 0, 180)); pantalla.blit(ov, (0, 0))
        t = fuente_grande.render(ganador_net, True, AMARILLO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 200))
        r = fuente_med.render("R  →  Regresar al Menú", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 400))

    pygame.display.update()