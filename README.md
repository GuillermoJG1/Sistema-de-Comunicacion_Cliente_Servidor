# Protocolo Cliente-Servidor

Sistema de mensajería en tiempo real que implementa una arquitectura cliente-servidor robusta para comunicación multiusuario.

#Integrantes
Lara López Lisseth Yaret
Martinez Gonzalez Guillermo Josue
Quintero Manríquez Alejandra

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Flujo del Protocolo](#flujo-del-protocolo)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Especificaciones del Protocolo](#especificaciones-del-protocolo)
- [Contribuir](#contribuir)

##  Descripción General

Este proyecto implementa un sistema de chat en tiempo real con interfaz gráfica que permite comunicación entre múltiples usuarios a través de una arquitectura cliente-servidor. Incluye aplicaciones separadas para servidor (`servidor_gui.py`) y cliente (`cliente_gui.py`) con interfaces gráficas intuitivas desarrolladas con FreeSimpleGUI.

##  Estructura del Proyecto
protocolo-cliente-servidor/
├── servidor_gui.py    # Aplicación servidor con interfaz gráfica
├── cliente_gui.py     # Aplicación cliente con interfaz gráfica
└── README.md          # Documentación del proyecto

##  Flujo del Protocolo

### 1. Conexión Inicial
- El cliente establece conexión con el servidor usando el puerto designado
- El cliente se identifica con un nombre o ID único
- Se requiere conexión a internet y dirección IP fija para conexión exitosa
- El servidor envía un mensaje especial de confirmación al aceptar la conexión

### 2. Identificación de Usuario
- El servidor valida que el nombre de usuario no esté repetido
- Si es válido, el cliente se agrega a la lista de usuarios activos
- El servidor envía mensaje de confirmación de conexión al cliente

### 3. Envío de Mensajes
- El cliente escribe y envía mensaje al servidor
- El mensaje incluye el contenido y la identificación del remitente
- El servidor recibe y procesa el mensaje

### 4. Manejo de Mensajes en el Servidor
- El servidor verifica el origen del mensaje
- El mensaje se retransmite a todos los clientes conectados en el puerto específico
- Se rechazan mensajes de puertos no autorizados

### 5. Gestión de Desconexiones (Opcional)
- El servidor notifica a otros clientes cuando un usuario se desconecta
- Se muestran mensajes de error para problemas de conexión
- Limpieza automática de usuarios desconectados

##  Características

- **Interfaz Gráfica Intuitiva**: Aplicación servidor y cliente con GUI usando FreeSimpleGUI
- **Comunicación en Tiempo Real**: Entrega instantánea de mensajes entre clientes
- **Gestión de Usuarios**: Validación de nombres únicos y seguimiento de usuarios activos
- **Difusión de Mensajes**: El servidor retransmite mensajes a todos los clientes conectados
- **Monitoreo de Conexiones**: Panel del servidor para visualizar conexiones y actividad
- **Manejo de Errores**: Gestión integral de errores para problemas de conexión
- **Desconexión Segura**: Notificación automática cuando usuarios se desconectan

##  Requisitos

- Python 3.7 o superior
- Conexión a internet
- Configuración de dirección IP fija
- Acceso al puerto designado del servidor (por defecto: 55555)

### Dependencias
```bash
pip install FreeSimpleGUI
 Instalación
bash# Clonar el repositorio
git clone https://github.com/tuusuario/protocolo-cliente-servidor.git

# Navegar al directorio del proyecto
cd protocolo-cliente-servidor

# Instalar dependencias
pip install FreeSimpleGUI
 Uso
Iniciar el Servidor
bash# Ejecutar la aplicación del servidor con interfaz gráfica
python servidor_gui.py

Haz clic en "Iniciar Servidor" para comenzar a aceptar conexiones
El servidor estará disponible en 127.0.0.1:55555 (configurable en el código)
Puedes monitorear las conexiones y mensajes en la ventana del servidor

Conectar Clientes
bash# Ejecutar la aplicación cliente con interfaz gráfica
python cliente_gui.py

Ingresa tu nombre de usuario en el campo "Nombre"
Haz clic en "Conectar" para unirte al chat
Escribe mensajes en el campo inferior y presiona "Enviar" o Enter
Usa "Desconectar" para salir del chat de forma segura

Comandos Básicos

Conectar: Ingresar nombre y presionar botón "Conectar"
Enviar mensaje: Escribir en el campo de mensaje y presionar Enter o "Enviar"
Desconectar: Presionar botón "Desconectar" para salir de forma segura

 Especificaciones del Protocolo
Proceso de Conexión

Cliente inicia conexión TCP al servidor
Cliente envía paquete de identificación con nombre de usuario
Servidor valida unicidad del nombre de usuario
Servidor responde con aceptación/rechazo
Conexión establecida para clientes aceptados

Formato de Mensaje
json{
  "remitente": "nombre_usuario",
  "contenido": "contenido del mensaje",
  "marca_tiempo": "marca de tiempo ISO",
  "tipo": "mensaje"
}
Manejo de Errores

Nombre de usuario duplicado: Conexión rechazada
Problemas de red: Mensaje de error mostrado
Desconexión del servidor: Todos los clientes notificados
Puerto inválido: Mensaje ignorado

 Contribuir

Hacer fork del repositorio
Crear rama de características (git checkout -b caracteristica/NuevaCaracteristica)
Hacer commit de cambios (git commit -m 'Agregar nueva característica')
Push a la rama (git push origin caracteristica/NuevaCaracteristica)
Abrir Pull Request

