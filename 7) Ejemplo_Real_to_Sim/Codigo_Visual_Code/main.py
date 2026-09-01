# ============================================
# SIMULACIÓN EN VS CODE - simulacion.py
# ============================================
# Este código se ejecuta en la PC
# Recibe el comando "MOVE" desde la ESP8266
# y mueve un cubo en PyBullet
# ============================================

import pybullet as p
import pybullet_data
import time
import serial
import sys

# --- CONFIGURACIÓN DEL PUERTO SERIE ---
# Intenta conectar a la ESP8266 en COM4
try:
    print("🔌 Conectando a ESP8266 en COM4...")
    ser = serial.Serial('COM4', 115200, timeout=0.1)
    print("✅ ESP8266 conectada exitosamente en COM4")
    esp8266_conectado = True
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    print("   Asegúrate de que:")
    print("   1. La ESP8266 esté conectada por USB")
    print("   2. Thonny esté CERRADO (esto es importante)")
    print("   3. El puerto sea COM4 (verifica en Administrador de Dispositivos)")
    print("\n🔧 Continuando en MODO DEMO con tecla 'M'")
    esp8266_conectado = False
    ser = None

# --- INICIALIZAR PYBULLET ---
print("\n🔄 Iniciando simulación PyBullet...")

# Conectar a PyBullet con interfaz gráfica
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Configurar gravedad
p.setGravity(0, -9.8, 0)
print("✅ Gravedad configurada")

# --- CREAR LA ESCENA ---
print("🔄 Creando escena...")

# Crear un suelo (plano)
plane_id = p.loadURDF("plane.urdf")
print("✅ Suelo creado")

# Crear un cubo
# Definir la forma del cubo (medio tamaño = 0.5m)
cube_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5])
# Crear el cubo con masa 1kg en posición (0, 0, 1)
cube_id = p.createMultiBody(1.0, cube_shape, basePosition=[0, 0, 1])
print("✅ Cubo creado en posición (0, 0, 1)")

# --- VARIABLES DE CONTROL ---
pos_x = 0  # Posición X del cubo
modo_demo = not esp8266_conectado

print("\n" + "="*50)
if esp8266_conectado:
    print("🎮 SISTEMA LISTO CON ESP8266")
    print("   Presiona el botón en la ESP8266 para mover el cubo")
else:
    print("🎮 MODO DEMO ACTIVADO")
    print("   Presiona la tecla 'M' en la ventana de PyBullet")
    print("   para mover el cubo")
print("="*50 + "\n")

print("🔄 Simulación ejecutándose...")
print("   (Presiona ESC en la ventana de PyBullet para salir)")

# --- BUCLE PRINCIPAL DE SIMULACIÓN ---
try:
    while True:
        # ============================================
        # 1. LEER COMANDOS DE LA ESP8266
        # ============================================
        if esp8266_conectado and ser:
            try:
                # Verificar si hay datos disponibles
                if ser.in_waiting > 0:
                    # Leer una línea completa (hasta '\n')
                    command = ser.readline().decode('utf-8').strip()
                    
                    if command == "MOVE":
                        # Mover el cubo 1 metro a la derecha
                        pos_x += 1
                        print(f"🎯 [ESP8266] Moviendo cubo a X = {pos_x}")
                        
                        # Actualizar la posición del cubo
                        p.resetBasePositionAndOrientation(
                            cube_id, 
                            [pos_x, 0, 1],  # Nueva posición
                            [0, 0, 0, 1]    # Sin rotación
                        )
            except Exception as e:
                print(f"⚠️ Error en comunicación: {e}")
                print("   Cambiando a modo DEMO")
                esp8266_conectado = False
                modo_demo = True
                ser = None
        
        # ============================================
        # 2. MODO DEMO: TECLA 'M'
        # ============================================
        if modo_demo:
            # Obtener eventos del teclado en PyBullet
            keys = p.getKeyboardEvents()
            
            # Verificar si la tecla 'M' está presionada
            if ord('m') in keys and keys[ord('m')] & p.KEY_IS_DOWN:
                pos_x += 1
                print(f"🎯 [DEMO] Moviendo cubo a X = {pos_x}")
                
                # Actualizar la posición del cubo
                p.resetBasePositionAndOrientation(
                    cube_id, 
                    [pos_x, 0, 1],
                    [0, 0, 0, 1]
                )
                
                # Pausa para evitar múltiples movimientos
                time.sleep(0.2)
        
        # ============================================
        # 3. AVANZAR LA SIMULACIÓN
        # ============================================
        p.stepSimulation()
        
        # Controlar la velocidad de la simulación
        # 240 steps por segundo (velocidad real)
        time.sleep(1/240)
        
# ============================================
# MANEJO DE INTERRUPCIONES Y LIMPIEZA
# ============================================
except KeyboardInterrupt:
    print("\n🛑 Simulación detenida por el usuario")
except Exception as e:
    print(f"❌ Error en la simulación: {e}")
finally:
    # Cerrar conexiones
    if ser:
        ser.close()
        print("🔌 Conexión serial cerrada")
    p.disconnect()
    print("👋 Simulación finalizada")