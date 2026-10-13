# =============================================================
# Ejemplo 2 — Programa NO BLOQUEANTE con ticks_ms (sondeo)
# Placa: ESP32 con MicroPython
# Conexiones: LED en GPIO2, botón BOOT en GPIO0
# -------------------------------------------------------------
# Ya no usamos sleep(): preguntamos "¿ya pasó el tiempo?"
# en cada vuelta del bucle. El botón responde de inmediato...
# pero la CPU gira sin parar (100 % ocupada) aunque no haya
# nada que hacer. Ese es el precio del "sondeo" (polling).
# =============================================================
from machine import Pin
import time

led = Pin(2, Pin.OUT)
boton = Pin(0, Pin.IN, Pin.PULL_UP)

PERIODO_LED_MS = 1000
ultimo_cambio = time.ticks_ms()
boton_antes = 1
vueltas = 0                      # cuántas veces gira el bucle
ultimo_reporte = time.ticks_ms()

while True:
    ahora = time.ticks_ms()
    vueltas += 1

    # Tarea 1: parpadeo sin bloquear
    # ticks_diff() maneja correctamente el desbordamiento del contador
    if time.ticks_diff(ahora, ultimo_cambio) >= PERIODO_LED_MS:
        led.value(not led.value())
        ultimo_cambio = ahora

    # Tarea 2: detectar el FLANCO de bajada del botón (1 -> 0)
    boton_ahora = boton.value()
    if boton_antes == 1 and boton_ahora == 0:
        print("Botón detectado en t =", ahora, "ms")
    boton_antes = boton_ahora

    # Tarea 3: mostrar cuántas vueltas da el bucle por segundo
    if time.ticks_diff(ahora, ultimo_reporte) >= 5000:
        print("Vueltas del bucle en 5 s:", vueltas, "(CPU siempre ocupada)")
        vueltas = 0
        ultimo_reporte = ahora
