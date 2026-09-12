import datetime
import sqlite3
import socket

from resources.functions_server import crear_tabla_mensajes, inicializar_socket, insertar_mensaje


crear_tabla_mensajes()
server_socket = inicializar_socket()
servidor_corriendo = True
while servidor_corriendo:
    client_socket, client_address = server_socket.accept()
    print(f'Conexión establecida desde {client_address}')

    while True:
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            print(f"Cliente {client_address} finalizó la sesión.")
            break

        # Intercepta el comando de apagado
        if data.strip() == "/shutdown":
            print(f"Comando /shutdown recibido desde {client_address}. Apagando servidor...")
            
            # Responde al cliente antes de cortar
            respuesta = "Servidor apagándose de manera ordenada..."
            client_socket.sendall(respuesta.encode('utf-8'))
            
            # Rompe ambos bucles
            servidor_corriendo = False
            break
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Mensaje recibido: {timestamp}')

        insertar_mensaje(data, client_address[0])

        respuesta = f"Mensaje recibido: {timestamp}"
        client_socket.sendall(respuesta.encode('utf-8'))

    client_socket.close()
    if not servidor_corriendo:
        print("Servidor apagado.")
        server_socket.close()
        break