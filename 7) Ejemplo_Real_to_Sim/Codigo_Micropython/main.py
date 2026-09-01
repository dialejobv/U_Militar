# ============================================
# CODIGO PARA ESP8266 - main.py
# ============================================
# Este código se ejecuta en la ESP8266
# Envía el comando "MOVE" por el puerto serie
# cuando se presiona el botón
# ============================================

from machine import Pin, UART
import time

# --- CONFIGURACIÓN DEL BOTÓN ---
# GPIO14 con resistencia pull-up interna
# El pin lee 0 (False) cuando se presiona el botón
button = Pin(14, Pin.IN, Pin.PULL_UP)
print("✅ Botón configurado en GPIO14")

# --- CONFIGURACIÓN DEL PUERTO SERIE ---
# UART0 para comunicación con la PC
# Velocidad: 115200 baudios
uart = UART(0, baudrate=115200)
print("✅ UART configurado a 115200 baudios")

# --- VARIABLES DE CONTROL ---
last_state = 1  # Estado anterior del botón (1 = no presionado)
enviar_comando = False

print("\n" + "="*50)
print("🎮 ESP8266 LISTA")
print("   Presiona el botón para enviar 'MOVE'")
print("   El comando se enviará por el puerto COM4")
print("="*50 + "\n")

# --- BUCLE PRINCIPAL ---
while True:
    # Leer el estado actual del botón
    current_state = button.value()
    
    # Detectar cuando el botón se presiona (flanco de bajada: 1 → 0)
    if last_state == 1 and current_state == 0:
        print("🔘 ¡Botón presionado!")
        
        # Enviar el comando por el puerto serie
        # El '\n' es importante para que la PC sepa dónde termina el comando
        uart.write("MOVE\n")
        print("📤 Comando 'MOVE' enviado")
        
        # Pequeña pausa para evitar rebotes del botón
        time.sleep(0.3)
    
    # Actualizar el estado anterior
    last_state = current_state
    
    # Pequeña pausa para no saturar el procesador
    time.sleep(0.05)