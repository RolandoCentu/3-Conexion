## DESDE EL SERVIDOR

import socket
import threading        # threading ayuda implementar concurrencia a traves de hilos. Permite ejecutar multiples tareas simultaneamente dentro de un mismo programa.

# Se crea el socket del servidor
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 7777
socket_server.bind((host, port))

socket_server.listen()
socket_server.settimeout(1.0)
print("---[SERVER ONLINE]---")
print(" ¡Esperando conexiones! ")

lista_de_clientes = []

#### Funcion manejar cliente:
def handle_clients(cliente_socket, addr):
    connected = True
    # Mientras el cliente este conectado
    while connected:

        try:
            ## Escuchar los mensajes que envia
            mensaje = cliente_socket.recv(2048).decode('utf-8')     # formato de transformacion unicode de 8 bits
            if mensaje != '':
                print(f'[NEW MESSAGE] {addr} : {mensaje}')

                # Difundir mensaje a todos los clientes (BROADCAST)
                for cliente, _ in lista_de_clientes:
                    if cliente != cliente_socket: # DETALLE: que solo les aparezca a los demas clientes, no a uno mismo
                        # mostrar mensaje
                        try:
                            cliente.send(f'{addr}: {mensaje}'.encode())
                        except ConnectionResetError:
                            print(f'[!] Error al enviar mensaje a {cliente}, eliminando')
                            # Practicar manejo de errores (EJ: eliminar al cliente de la lista si se cierra conexion, verificar que este en la lista, etc)
                            # antes de eliminar cliente, verificar si esta en la lista
                            try:
                                lista_de_clientes.remove((cliente,addr))
                            except ValueError:  # error que se lanza cuando intentas usar un valor con el tipo correcto pero contenido incorrecto
                                pass
                            print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')

            ## Si el mensaje es 'salir', cortar conexion y salir del hilo
            ### Seguimos practicando manejo de errores con respecto a remover un cliente si se cierra conexion
            if mensaje.lower() == 'salir':
                print(f'[!] Cerrando conexion de {addr}')
                cliente_socket.close()
                try:
                    lista_de_clientes.remove((cliente_socket, addr))
                except ValueError:
                    print('[!] Ese cliente ya no estaba en la lista (probablemente se ha desconectado)')
                connected = False       # para romper el loop
                print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')
        
        except (ConnectionResetError, KeyboardInterrupt, EOFError):
            print(f'[!] {addr} se desconecto inesperadamente')
            cliente_socket.close()
            try:
                lista_de_clientes.remove((cliente_socket, addr))
            except ValueError:
                print('[!] Ese cliente ya no estaba en la lista (probablemente se ha desconectado)')
            print(f'[i] Total de clientes conectados: {len(lista_de_clientes)}')
            connected = False

## Mientras el servidor este corriendo:
try: 
    while True:
        ### Aceptar una nueva conexion (cliente y direccion)
        try:
            cliente, address = socket_server.accept()
            print(f'[NEW CONNECTION ESTABLISHED] {address}')
            print(f'[i] Total de clientes conectados: {len(lista_de_clientes)+1}')
            
            ### Crear un hilo nuevo que se encargue de ese cliente
            thread_clients = threading.Thread(target=handle_clients, args=(cliente, address), daemon=True)
            thread_clients.start()
            ### El hilo tendra la tarea de ejercutar una funcion que maneje solo a ese cliente.

            #### Llevar registro de todos los clientes conectados 
            lista_de_clientes.append((cliente, address))
        except socket.timeout:
            # No hay nuevas conexiones, simplemente sigue el loop
            continue


except KeyboardInterrupt:
    print('\n[SHUTDOWN] Cerrando clientes...')
    for client, _ in lista_de_clientes:
        try:
            client.shutdown(socket.SHUT_RDWR)  # intenta cortar ambos sentidos
        except OSError:
            pass
        finally:
            try:
                client.close()
            except OSError:
                pass

    lista_de_clientes.clear()
    print('[SHUTDOWN] Cerrando socket del servidor...')
    socket_server.close()

    print('[SHUTDOWN] Servidor apagado.')
            