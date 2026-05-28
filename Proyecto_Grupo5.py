import random

cartas = [1,2,3,4,5,6,7,8,9,10,10,10,10]

def repartir_carta():
    return random.choice(cartas)

def calcular_puntaje(mano):
    return sum(mano)

def mostrar_mano(jugador, mano):
    print(f"{jugador}: {mano} -> Total: {calcular_puntaje(mano)}")

def iniciar_juego():
    jugador = [repartir_carta(), repartir_carta()]
    dealer = [repartir_carta()]

    while True:
        mostrar_mano("Jugador", jugador)
        mostrar_mano("Dealer", dealer)

        if calcular_puntaje(jugador) > 21:
            print("Perdiste.")
            break

        opcion = input("¿Pedir carta? (s/n): ")

        if opcion.lower() == 's':
            jugador.append(repartir_carta())
        else:
            break

    while calcular_puntaje(dealer) < 17:
        dealer.append(repartir_carta())

    print("\nResultado final")
    mostrar_mano("Jugador", jugador)
    mostrar_mano("Dealer", dealer)

    if calcular_puntaje(dealer) > 21 or calcular_puntaje(jugador) > calcular_puntaje(dealer):
        print("Ganaste!")
    elif calcular_puntaje(jugador) == calcular_puntaje(dealer):
        print("Empate.")
    else:
        print("Dealer gana.")

if __name__ == "__main__":
    iniciar_juego()

import socket

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Servidor BlackJack iniciado...")

conn, addr = server.accept()

print(f"Jugador conectado desde {addr}")

conn.send("Bienvenido al BlackJack Multijugador".encode())

conn.close()

import socket

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

mensaje = client.recv(1024).decode()

print(mensaje)

client.close()