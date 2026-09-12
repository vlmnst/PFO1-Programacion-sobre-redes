import socket

import resources.common_var as common


# Configuración y conexión del socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((common.HOST, common.PORT))
    print("Conectado al servidor. Escribe tu mensaje (o 'éxito' para salir):")

    while True:
        mensaje = input("> ")

        # Condición para finalizar la comunicación
        if mensaje.strip().lower() == "éxito":
            print("Finalizando conexión...")
            cliente.close()
            break

        # Evita enviar entradas vacías
        if not mensaje.strip():
            continue

        try:
            # Envío de datos
            cliente.sendall(mensaje.encode('utf-8'))

            # Recepción de la respuesta
            respuesta = cliente.recv(1024).decode('utf-8')

            # Caso 1: Cierre intencional / limpio
            # Ocurre si el servidor finalizó su proceso o cerró el socket de forma ordenada (.close())
            if not respuesta:
                print("El servidor cerró la conexión de manera ordenada.")
                break

            print(f"{respuesta}")

        except (ConnectionResetError, BrokenPipeError):
            # Caso 2: Cierre abrupto / caída no planificada
            # Ocurre si el proceso del servidor colapsó, se cerró forzosamente (kill -9) o se interrumpió la red
            print("Error: Se perdió la conexión inesperadamente con el servidor (posible caída del proceso).")
            break

except ConnectionRefusedError:
    print("Error: No se pudo conectar al servidor. Verifica que esté en ejecución.")
finally:
    cliente.close()