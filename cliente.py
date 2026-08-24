import socket

HOST = 'localhost'
PORT = 5001

# Configuración y conexión del socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORT))
    print("Conectado al servidor. Escribe tu mensaje (o 'éxito' para salir):")

    while True:
        mensaje = input("> ")

        # Condición para finalizar la comunicación
        if mensaje.strip().lower() == "éxito":
            print("Finalizando conexión...")
            break

        # Evita enviar entradas vacías
        if not mensaje.strip():
            continue

        # Envío de datos codificados en UTF-8
        cliente.sendall(mensaje.encode('utf-8'))

        # Recepción y muestra de la confirmación con timestamp
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f"Respuesta del servidor: {respuesta}")

except ConnectionRefusedError:
    print("Error: No se pudo conectar al servidor. Verifica que esté en ejecución.")
finally:
    cliente.close()