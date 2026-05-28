import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 5000))

mensaje = client.recv(1024).decode()
print(mensaje)

jugada = input("Elige piedra, papel o tijera: ")

client.send(jugada.encode())

resultado = client.recv(1024).decode()

print("Resultado:", resultado)

client.close()