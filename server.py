import socket
import threading
import time
import random
from game_logic import Obstaculo, Nitro, Carro

RESET_IP = 'localhost'
PUERTO = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((RESET_IP, PUERTO))
server.listen(2)

print("Servidor iniciado. Esperando a los 2 jugadores...")

clientes = []
teclas_jugadores = {0: "NONE", 1: "NONE"}

ALTO = 600
CAR_W, CAR_H = 46, 84
CARRIL1_IZQ, CARRIL1_DER = 183, 442
CARRIL2_IZQ, CARRIL2_DER = 458, 725

j1 = Carro(CARRIL1_IZQ + (CARRIL_ANCHO := (CARRIL1_DER - CARRIL1_IZQ) - CAR_W) // 2, ALTO - CAR_H - 30, (230,30,30), (150,0,0), CARRIL1_IZQ, CARRIL1_DER)
j2 = Carro(CARRIL2_IZQ + ((CARRIL2_DER - CARRIL2_IZQ) - CAR_W) // 2, ALTO - CAR_H - 30, (0,100,255), (0,50,160), CARRIL2_IZQ, CARRIL2_DER)

estado = "menu"
vel_actual = 4.0
tiempo_inicio = 0
DURACION = 60
tiempo_restante = 60.0
spawn_timer = 0
obstaculos = []
nitros = []
score1 = 0
score2 = 0
nitro_activo = False
nitro_timer = 0
ganador = ""

def manejar_cliente(conn, jugador_id):
    global teclas_jugadores
    try:
        conn.send(str(jugador_id).encode('utf-8'))
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            teclas_jugadores[jugador_id] = data
    except:
        pass
    finally:
        print(f"Jugador {jugador_id + 1} se ha desconectado.")
        if conn in clientes:
            clientes.remove(conn)
        conn.close()

def bucle_logica_juego():
    global estado, tiempo_inicio, tiempo_restante, vel_actual, spawn_timer, ganador
    global score1, score2, nitro_activo, nitro_timer, obstaculos, nitros

    while True:
        time.sleep(1/60)
        if len(clientes) < 2:
            continue

        if estado == "menu":
            if teclas_jugadores[0] == "START":
                obstaculos.clear()
                nitros.clear()
                j1.vivo = True; j2.vivo = True
                j1.x = CARRIL1_IZQ + (259 - CAR_W) // 2
                j2.x = CARRIL2_IZQ + (259 - CAR_W) // 2
                score1 = 0; score2 = 0
                vel_actual = 4.0
                nitro_activo = False; nitro_timer = 0
                tiempo_inicio = time.time()
                estado = "jugando"
                teclas_jugadores[0] = "NONE"

        elif estado == "jugando":
            tiempo_seg = time.time() - tiempo_inicio
            tiempo_restante = max(0.0, DURACION - tiempo_seg)
            vel_actual = 4.0 + (tiempo_seg * 0.18)

            usando_nitro = False
            if nitro_activo and nitro_timer > 0:
                if "Z" in teclas_jugadores[0] or "Z" in teclas_jugadores[1]:
                    usando_nitro = True
                    nitro_timer -= 1
                    # FIX: apagar nitro cuando se agota el timer
                    if nitro_timer <= 0:
                        nitro_activo = False

            velocidad_render = vel_actual + 8 if usando_nitro else vel_actual

            if j1.vivo:
                if "A" in teclas_jugadores[0]: j1.mover(-1)
                if "D" in teclas_jugadores[0]: j1.mover(1)
            if j2.vivo:
                if "LEFT" in teclas_jugadores[1]: j2.mover(-1)
                if "RIGHT" in teclas_jugadores[1]: j2.mover(1)

            spawn_timer += 1
            intervalo_spawn = max(35, 85 - int(tiempo_seg * 0.7))
            if spawn_timer >= intervalo_spawn:
                spawn_timer = 0
                obstaculos.append(Obstaculo(random.choice([1, 2])))
                if random.random() < 0.25:
                    nitros.append(Nitro())

            for obs in obstaculos[:]:
                obs.mover(velocidad_render)
                if j1.vivo and j1.rect_col().colliderect(obs.rect_col()):
                    j1.vivo = False; j1.explotar()
                if j2.vivo and j2.rect_col().colliderect(obs.rect_col()):
                    j2.vivo = False; j2.explotar()
                if obs.fuera():
                    if obs.carril == 1 and j1.vivo: score1 += 1
                    if obs.carril == 2 and j2.vivo: score2 += 1
                    obstaculos.remove(obs)

            for nitro in nitros[:]:
                nitro.mover(velocidad_render)
                if j1.vivo and j1.rect_col().colliderect(nitro.rect_col()):
                    nitro_activo = True; nitro_timer = 180
                    nitros.remove(nitro)
                elif j2.vivo and j2.rect_col().colliderect(nitro.rect_col()):
                    nitro_activo = True; nitro_timer = 180
                    nitros.remove(nitro)
                elif nitro.fuera():
                    nitros.remove(nitro)

            if tiempo_restante <= 0 or (not j1.vivo and not j2.vivo):
                if j1.vivo and j2.vivo:
                    ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
                elif j1.vivo and not j2.vivo: ganador = "¡JUGADOR 1 GANA!"
                elif j2.vivo and not j1.vivo: ganador = "¡JUGADOR 2 GANA!"
                else:
                    ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
                estado = "fin"

        elif estado == "fin":
            if teclas_jugadores[0] == "RESET" or teclas_jugadores[1] == "RESET":
                estado = "menu"
                teclas_jugadores[0] = "NONE"; teclas_jugadores[1] = "NONE"

        # FIX: obs_string ahora incluye x para que el cliente no regenere posición aleatoria
        obs_string = "/".join([f"{o.carril}:{o.x}:{o.y}" for o in obstaculos]) if obstaculos else "NONE"
        nitros_string = "/".join([f"{n.x}:{n.y}" for n in nitros]) if nitros else "NONE"

        paquete = f"{estado},{tiempo_restante:.1f},{vel_actual:.2f},{j1.x},{int(j1.vivo)},{j2.x},{int(j2.vivo)},{score1},{score2},{int(nitro_activo)},{nitro_timer},{ganador},{obs_string},{nitros_string}"

        for c in clientes[:]:
            try:
                c.send((paquete + "\n").encode('utf-8'))
            except:
                pass

threading.Thread(target=bucle_logica_juego, daemon=True).start()

while True:
    try:
        conn, addr = server.accept()
        if len(clientes) < 2:
            jugador_id = len(clientes)
            clientes.append(conn)
            print(f"Jugador {jugador_id + 1} conectado desde {addr}")
            threading.Thread(target=manejar_cliente, args=(conn, jugador_id), daemon=True).start()
        else:
            conn.close()
    except:
        break