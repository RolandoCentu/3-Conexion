import socket
import threading
import sys

# Configuracion
host = '127.0.0.1' 
port = 7777

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print('--- CONECTADO AL SERVIDOR ---')
except ConnectionRefusedError:
    print("[ERROR] No se pudo conectar con el SERVIDOR.")
    sys.exit()

def enviar_mensaje(sock):
    while True:
        try:
            mensaje = input(">> ")
            if mensaje:
                sock.send(mensaje.encode('utf-8'))
                
                if mensaje.lower() == 'salir':
                    print('[BYE] Cerrando conexion...')
                    sock.close()
                    break
            else:
                print('[i] El mensaje esta vacio')
        except (EOFError, KeyboardInterrupt, OSError):
            break

def recibir_mensaje(sock):
    while True:
        try:
            # Recibir datos
            response = sock.recv(2048).decode('utf-8')
            if response:
                # El \r limpia la línea actual para que el mensaje entrante no se mezcle con ">>"
                print(f"\r[MENSAJE] {response}\n>> ", end="", flush=True)
            else:
                # Si recv devuelve nada, el servidor cerró la conexión
                print("\n[BYE] Servidor desconectado.")
                break
        except (ConnectionError, OSError):
            break
    
    print("\n[INFO] Presiona ENTER para salir.")
    sock.close()

thread_envio = threading.Thread(target=enviar_mensaje, args=(client_socket,), daemon=True)
thread_recepcion = threading.Thread(target=recibir_mensaje, args=(client_socket,), daemon=True)

thread_envio.start()
thread_recepcion.start()

# Mantener el programa vivo mientras los hilos trabajan
try:
    while thread_envio.is_alive() and thread_recepcion.is_alive():
        thread_envio.join(1)
except KeyboardInterrupt:
    print("\n[SALIENDO]")
