# Chat Cliente-Servidor en Python
Este proyecto implementa un sistema de chat básico utilizando sockets TCP y hilos (threading) en Python.
Permite que múltiples clientes se conecten a un servidor, envíen mensajes y reciban mensajes de otros clientes en tiempo real.

---

## 🚀 Funcionamiento
Servidor
Crea un socket TCP (AF_INET, SOCK_STREAM) y lo asocia a una dirección IP y puerto (por defecto 127.0.0.1:7777).

Escucha conexiones entrantes y, por cada cliente, lanza un hilo que maneja su comunicación.

Mantiene una lista de clientes conectados.

Difunde (broadcast) los mensajes recibidos a todos los demás clientes.

Maneja desconexiones voluntarias (salir) e inesperadas (cierre abrupto).

Se puede apagar con Ctrl+C, cerrando todas las conexiones activas.

Cliente
Crea un socket TCP y se conecta al servidor en la IP y puerto configurados.

Utiliza dos hilos:

Envío: lee mensajes desde la entrada estándar (stdin) y los envía al servidor.

Recepción: escucha mensajes del servidor y los muestra en la salida estándar (stdout).

Comando especial: escribir salir cierra la conexión y termina el cliente.

Detecta si el servidor se apaga y muestra un mensaje de desconexión.

---

## ⚙️ Características
Comunicación en tiempo real entre múltiples clientes.

Manejo de errores y desconexiones.

Broadcast de mensajes a todos los clientes conectados.

Uso de hilos para concurrencia en cliente y servidor.

Compatible con cualquier puerto >1023 (por defecto 7777).

---

## ▶️ Ejecución  

### 1️⃣ Iniciar el servidor  
```bash
python server.py
```

### 2️⃣ Iniciar los clientes (en diferentes terminales)
```bash
python client.py
```

### 3️⃣ Enviar mensajes
Cada cliente puede escribir y enviar mensajes que serán recibidos por todos los demás.
Para salir:
```bash
salir
```

---
## 🧩 Tecnologías utilizadas
- Python 3.11

- Módulos estándar: socket, threading, sys

- Modelo: TCP (Orientado a conexión)
