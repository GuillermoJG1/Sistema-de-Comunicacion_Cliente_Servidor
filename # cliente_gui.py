# cliente_gui.py
import socket
import threading
import FreeSimpleGUI as sg

# Tema de la interfaz
sg.theme('DarkTeal9')

# Diseño de la interfaz del cliente
layout_cliente = [
    [sg.Text('Nombre:'), sg.Input(key='-NICK-', size=(20, 1)), 
     sg.Button('Conectar', bind_return_key=True), sg.Button('Desconectar')],
    [sg.Multiline('', size=(60, 15), key='-CHAT-', autoscroll=True, disabled=True)],
    [sg.Text('Mensaje:'), sg.Input(key='-MSG-', size=(50, 1)), 
     sg.Button('Enviar',bind_return_key=True)],
    [sg.StatusBar('Desconectado', key='-STATUS-', size=(60, 1))]
]

ventana_cliente = sg.Window('Cliente de Chat', layout_cliente, finalize=True)
ventana_cliente['-NICK-'].set_focus()

# Variables globales
cliente = None
apodo = ""
conectado = False

# Función para conectar al servidor
def conectar_servidor():
    global cliente, conectado, apodo
    
    apodo = valores['-NICK-']
    if not apodo:
        ventana_cliente['-STATUS-'].update('Debe ingresar un nombre')
        return
        
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('192.168.1.2', 55555))
        conectado = True
        
        # Iniciar hilo para recibir mensajes
        thread_recibir = threading.Thread(target=recibir, daemon=True)
        thread_recibir.start()
        
        ventana_cliente['-STATUS-'].update(f'Conectado como: {apodo}')
        ventana_cliente['-CHAT-'].print(f'Conectado al servidor como {apodo}')
        ventana_cliente['-NICK-'].update(disabled=True)
        ventana_cliente['-Conectar-'].update(disabled=True)
        ventana_cliente['-Desconectar-'].update(disabled=False)
        ventana_cliente['-MSG-'].set_focus()
        
    except Exception as e:
        ventana_cliente['-STATUS-'].update(f'Error de conexión: {str(e)}')
        conectado = False

# Función para desconectar del servidor
def desconectar_servidor():
    global cliente, conectado
    
    if cliente:
        try:
            cliente.close()
        except:
            pass
            
    conectado = False
    ventana_cliente['-STATUS-'].update('Desconectado')
    ventana_cliente['-NICK-'].update(disabled=False)
    ventana_cliente['-Conectar-'].update(disabled=False)
    ventana_cliente['-Desconectar-'].update(disabled=True)
    ventana_cliente['-CHAT-'].print('Desconectado del servidor')

# Función para recibir mensajes del servidor
def recibir():
    while conectado:
        try:
            mensaje = cliente.recv(1024).decode('ascii')
            if mensaje == 'NICK':
                cliente.send(apodo.encode('ascii'))
            else:
                ventana_cliente['-CHAT-'].print(mensaje)
        except:
            if conectado:  # Solo mostrar error si realmente estábamos conectados
                ventana_cliente['-CHAT-'].print("Ha ocurrido un error!")
                ventana_cliente['-STATUS-'].update('Error de conexión')
            break

# Función para enviar mensajes al servidor
def enviar_mensaje():
    mensaje = valores['-MSG-']
    if mensaje and conectado:
        try:
            mensaje_completo = f'{apodo}: {mensaje}'
            cliente.send(mensaje_completo.encode('ascii'))
            ventana_cliente['-MSG-'].update('')
        except:
            ventana_cliente['-CHAT-'].print("Error al enviar el mensaje")

# Bucle principal del cliente
while True:
    evento, valores = ventana_cliente.read()
    
    if evento == sg.WIN_CLOSED:
        if conectado:
            desconectar_servidor()
        break
        
    elif evento == 'Conectar' and not conectado:
        conectar_servidor()
        
    elif evento == 'Desconectar' and conectado:
        desconectar_servidor()
        
    elif evento == 'Enviar' and conectado:
        enviar_mensaje()

ventana_cliente.close()