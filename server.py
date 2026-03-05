import socket
import threading
import sys

# --- CONFIGURACIÓN ---
HOST = '127.0.0.1'
PORT = 7777
lista_de_clientes = []
# Un Lock para asegurar que dos hilos no modifiquen la lista al mismo tiempo
lista_lock = threading.Lock() 

# --- LÓGICA DE MANEJO DE CLIENTES ---
def handle_clients(cliente_socket, addr):
    """Función que corre en un hilo separado para cada cliente."""
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    
    connected = True
    while connected:
        try:
            # Recibimos datos
            data = cliente_socket.recv(2048)
            
            # Si recv no devuelve nada, el cliente cerró el socket
            if not data:
                break
                
            mensaje = data.decode('utf-8')
            
            # Opción de salida voluntaria
            if mensaje.lower() == 'salir':
                print(f"[DESCONEXIÓN] {addr} solicitó salir.")
                break

            print(f'[MENSAJE] {addr}: {mensaje}')

            # DIFUSIÓN (BROADCAST) a todos los demás
            # Usamos lista_de_clientes[:] (una copia) para iterar con seguridad
            with lista_lock:
                for cliente, c_addr in lista_de_clientes[:]:
                    if cliente != cliente_socket:
                        try:
                            cliente.send(f'{addr}: {mensaje}'.encode('utf-8'))
                        except (ConnectionResetError, OSError):
                            # Si falla el envío, el cliente ya no está
                            if (cliente, c_addr) in lista_de_clientes:
                                lista_de_clientes.remove((cliente, c_addr))

        except (ConnectionResetError, ConnectionAbortedError):
            print(f"[!] Conexión perdida forzosamente con {addr}")
            break
        except Exception as e:
            print(f"[!] Error inesperado con {addr}: {e}")
            break

    # --- LIMPIEZA AL SALIR DEL BUCLE ---
    with lista_lock:
        try:
            if (cliente_socket, addr) in lista_de_clientes:
                lista_de_clientes.remove((cliente_socket, addr))
        except ValueError:
            pass
            
    cliente_socket.close()
    print(f'[i] Cliente {addr} fuera. Total conectados: {len(lista_de_clientes)}')

# --- INICIO DEL SERVIDOR ---
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitir reutilizar el puerto inmediatamente después de cerrar el server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
    except socket.error as e:
        print(f"[ERROR] No se pudo vincular el puerto {PORT}: {e}")
        return

    server.listen()
    # Timeout para que el accept() no bloquee el KeyboardInterrupt (Ctrl+C)
    server.settimeout(1.0)
    
    print(f"---[SERVER ONLINE EN {HOST}:{PORT}]---")
    print("¡Esperando conexiones! (Presiona Ctrl+C para apagar el server)")

    try:
        while True:
            try:
                cliente, direccion = server.accept()
                
                with lista_lock:
                    lista_de_clientes.append((cliente, direccion))
                
                # Crear y lanzar el hilo
                thread = threading.Thread(target=handle_clients, args=(cliente, direccion), daemon=True)
                thread.start()
                
                print(f"[SISTEMA] Clientes totales: {len(lista_de_clientes)}")
                
            except socket.timeout:
                continue # El timeout permite que el bucle revise el KeyboardInterrupt
                
    except KeyboardInterrupt:
        print('\n[APAGANDO] Cerrando servidor y clientes...')
    finally:
        # Cerrar todos los sockets de clientes
        with lista_lock:
            for c_sock, _ in lista_de_clientes:
                try:
                    c_sock.close()
                except:
                    pass
        server.close()
        print('[OFFLINE] Servidor detenido.')

if __name__ == "__main__":
    start_server()
