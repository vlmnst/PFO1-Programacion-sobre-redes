import datetime
import sqlite3
import socket

def conexion_base_datos():
    conexion = sqlite3.connect('database/chat.db')
    return conexion

def inicializar_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', 5001))
    except OSError:
        print("No se pudo iniciar el servidor. El puerto 5001 ya está en uso.")
        exit(1)

    server_socket.listen(5)
    return server_socket

def insertar_mensaje(mensaje, ip_cliente, timestamp):
    conexion = conexion_base_datos()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO messages (message, ip_client, timestamp) VALUES (?, ?, ?)", (mensaje, ip_cliente, timestamp))
    conexion.commit()
    conexion.close()

server_socket = inicializar_socket()

def crear_tabla_mensajes():
    conexion = conexion_base_datos()
    cursor = conexion.cursor()
    with open('database/messages.sql', 'r') as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    conexion.commit()
    conexion.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f'Conexión establecida desde {client_address}')

    while True:
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            print(f"Cliente {client_address} finalizó la sesión.")
            break

        print(f'Mensaje recibido: {data}')

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insertar_mensaje(data, client_address[0], timestamp)

        respuesta = f"Mensaje recibido: {timestamp}"
        client_socket.sendall(respuesta.encode('utf-8'))

    client_socket.close()
    