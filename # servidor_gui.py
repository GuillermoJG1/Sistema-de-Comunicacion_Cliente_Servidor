# servidor_gui.py
import socket
import threading
import FreeSimpleGUI as sg

# Configuración de la interfaz
sg.theme('DarkBlue3')

# Datos de conexión
host = '192.168.1.2'
port = 55555

# Iniciar servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen()

# Listar clientes con apodos
clientes = []
apodos = []

# Diseño de la interfaz del servidor
layout_servidor = [
    [sg.Text('Servidor de Chat', font=('Helvetica', 16))],
    [sg.Text(f'Dirección: {host}:{port}', font=('Helvetica', 10))],
    [sg.Multiline('', size=(60, 20), key='-LOG-', autoscroll=True, disabled=True)],
    [sg.Button('Iniciar Servidor'), sg.Button('Detener Servidor'), sg.Button('Salir')]
]

ventana_servidor = sg.Window('Servidor de Chat', layout_servidor, finalize=True)
ventana_servidor['-LOG-'].update('Servidor listo. Presiona "Iniciar Servidor"\n')

# Enviar mensaje a los clientes
def difusion(mensaje):
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except:
            continue

# Manejo de la mensajería
def manejar(cliente):
    while True:
        try:
            # Difusión de la mensajeria
            mensaje = cliente.recv(1024)
            difusion(mensaje)
            
            # Mostrar en el log del servidor
            try:
                mensaje_decodificado = mensaje.decode('ascii')
                ventana_servidor['-LOG-'].print(f"Mensaje: {mensaje_decodificado}")
            except:
                ventana_servidor['-LOG-'].print("Mensaje no decodificable")
                
        except:
            # Remover clientes
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apodo = apodos[index]
            mensaje_salida = f'{apodo} se ha retirado!'
            difusion(mensaje_salida.encode('ascii'))
            ventana_servidor['-LOG-'].print(mensaje_salida)
            apodos.remove(apodo)
            break

# Función de recepción
def recibir():
    while servidor_activo:
        try:
            # Aceptar conexiones de nuevos clientes
            cliente, direccion = servidor.accept()
            ventana_servidor['-LOG-'].print(f"Conectado {str(direccion)}")

            # Solicitar y almacenar Nick
            cliente.send('NICK'.encode('ascii'))
            apodo = cliente.recv(1024).decode('ascii')
            apodos.append(apodo)
            clientes.append(cliente)

            # Anunciar la entrada del usuario a la sala
            ventana_servidor['-LOG-'].print(f"Apodo: {apodo}")
            difusion(f"{apodo} se ha unido!".encode('ascii'))
            cliente.send('Conectado al servidor!'.encode('ascii'))

            # Comienza a manejar el hilo de cada cliente
            thread = threading.Thread(target=manejar, args=(cliente,))
            thread.daemon = True
            thread.start()
        except:
            break

# Variable para controlar el estado del servidor
servidor_activo = False
hilo_servidor = None

# Bucle principal del servidor
while True:
    evento, valores = ventana_servidor.read(timeout=100)
    
    if evento == sg.WIN_CLOSED or evento == 'Salir':
        servidor_activo = False
        if hilo_servidor:
            servidor.close()
        break
        
    elif evento == 'Iniciar Servidor' and not servidor_activo:
        servidor_activo = True
        hilo_servidor = threading.Thread(target=recibir, daemon=True)
        hilo_servidor.start()
        ventana_servidor['-LOG-'].print("Servidor iniciado. Esperando clientes...")
        
    elif evento == 'Detener Servidor' and servidor_activo:
        servidor_activo = False
        servidor.close()
        # Crear un nuevo socket para futuras conexiones
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, port))
        servidor.listen()
        ventana_servidor['-LOG-'].print("Servidor detenido. Puedes reiniciarlo.")

ventana_servidor.close()