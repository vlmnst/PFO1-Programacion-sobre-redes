> ⚠️ **Nota importante:** Mis pruebas locales las hice utilizando el puerto `5001`, ya que en macOS el puerto `5000` está reservado por defecto por el sistema operativo para el servicio nativo del "Receptor de AirPlay" (Control Center), lo que genera conflictos de red y deja las conexiones colgadas. De todas maneras, subo el proyecto respetando lo que se solicita en el PFO, dejando configurado el puerto en `5000`.

# Chat Cliente-Servidor TCP con SQLite

Sistema de mensajería modular en Python basado en sockets TCP y con persistencia de datos en SQLite.

---

## 📁 Estructura del Proyecto

```text
.
├── servidor.py                 # Punto de entrada principal del servidor
├── cliente.py                  # Punto de entrada principal del cliente
├── resources/
│   ├── common_var.py          # Constantes y configuraciones compartidas (HOST, PORT)
│   └── functions_server.py    # Funciones de sockets y operaciones de SQLite
└── database/
    ├── messages.sql           # Script de creación de la tabla en SQLite
    └── chat.db                # Base de datos SQLite (se genera automáticamente)
```

---

## Cómo Ejecutar el Proyecto

### Paso 1: Iniciar el Servidor

Abre una terminal en la carpeta raíz del proyecto y ejecuta:

```bash
python3 servidor.py
```

- El servidor verificará o creará la base de datos `database/chat.db` ejecutando `database/messages.sql`.
- Quedará a la espera de conexiones en `localhost:5000`.

### Paso 2: Iniciar el Cliente

Abre una **segunda terminal** (sin cerrar la del servidor) en la misma carpeta y ejecuta:

```bash
python3 cliente.py
```

- Se conectará inmediatamente al servidor.
- Verás la consola lista con el prompt `> ` para comenzar a enviar mensajes.

---

## 💬 Comandos e Interacción

| Entrada             | Acción                                                                     |
| :------------------ | :------------------------------------------------------------------------- |
| `<cualquier texto>` | Envía el mensaje al servidor y lo guarda en la base de datos `chat.db`.    |
| `éxito`             | Desconecta únicamente a ese cliente sin apagar el servidor.                |
| `/shutdown`         | Apaga el servidor de forma limpia, guarda cambios y libera el puerto 5000. |

---

## 🛠️ Comandos Útiles de Mantenimiento

- **Ver los mensajes almacenados en SQLite:**

  ```bash
  sqlite3 database/chat.db "SELECT * FROM messages;"
  ```

- **Borrar la base de datos para empezar de cero:**

  ```bash
  rm database/chat.db
  ```

- **Liberar el puerto 5000 en caso de bloqueo:**
  ```bash
  kill -9 $(lsof -t -i:5000) 2>/dev/null || echo "Puerto libre"
  ```
