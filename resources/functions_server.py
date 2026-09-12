import resources.common_var as common
import sqlite3
import socket
def conexion_base_datos():
    conexion = sqlite3.connect('database/chat.db')
    return conexion

def inicializar_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reutiliza el puerto de inmediato al reiniciar el script
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((common.HOST, common.PORT))
    except OSError:
        print(f"No se pudo iniciar el servidor. El puerto {common.PORT} ya está en uso.")
        exit(1)

    server_socket.listen(5)
    return server_socket

def insertar_mensaje(mensaje, ip_cliente):
    conexion = conexion_base_datos()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO messages (contenido, ip_client) VALUES (?,?)", (mensaje, ip_cliente))
    conexion.commit()
    conexion.close()


def crear_tabla_mensajes():
    conexion = conexion_base_datos()
    cursor = conexion.cursor()
    with open('database/messages.sql', 'r') as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    conexion.commit()
    conexion.close()
