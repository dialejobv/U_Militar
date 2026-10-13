# =============================================================
# Ejemplo 1 — Programa BLOQUEANTE
# Placa: ESP32 con MicroPython
# Conexiones: LED integrado en GPIO2, botón BOOT en GPIO0
# -------------------------------------------------------------
# Idea para la clase: presione el botón varias veces rápido.
# ¿Cuántas pulsaciones detecta el programa? ¿Por qué se pierden?
# =============================================================
from machine import Pin
import time

led = Pin(2, Pin.OUT)
boton = Pin(0, Pin.IN, Pin.PULL_UP)   # 0 = presionado

contador = 0

while True:
    led.value(1)
    time.sleep(1)            # <- la CPU no puede hacer NADA más durante 1 s
    led.value(0)
    time.sleep(1)            # <- otro segundo "congelado"

    # El botón solo se revisa una vez cada 2 segundos.
    # Si la pulsación dura 150 ms, lo más probable es que se pierda.
    if boton.value() == 0:
        contador += 1
        print("Botón detectado. Total:", contador)
