import socket
from game_logic import ganador

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 5000))
server.listen(2)

print("Servidor iniciado...")
print("Esperando jugadores...")

cliente1, direccion1 = server.accept()
print("Jugador 1 conectado")

cliente1.send("Conectado como Jugador 1".encode())

cliente2, direccion2 = server.accept()
print("Jugador 2 conectado")

cliente2.send("Conectado como Jugador 2".encode())

jugada1 = cliente1.recv(1024).decode().lower()
jugada2 = cliente2.recv(1024).decode().lower()

resultado = ganador(jugada1, jugada2)

cliente1.send(resultado.encode())
cliente2.send(resultado.encode())

cliente1.close()
cliente2.close()

server.close()