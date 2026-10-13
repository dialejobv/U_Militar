# =============================================================
# Ejemplo 8 — PLANTILLA: estructura básica de un programa asyncio
# Copie este archivo como punto de partida para sus proyectos.
# =============================================================

# 1) IMPORTACIONES ---------------------------------------------
import asyncio
from machine import Pin

# 2) CONFIGURACIÓN DE HARDWARE ---------------------------------
led = Pin(2, Pin.OUT)
boton = Pin(0, Pin.IN, Pin.PULL_UP)

# 3) ESTADO COMPARTIDO Y SINCRONIZACIÓN ------------------------
estado = {"modo": "normal"}
evento_boton = asyncio.Event()


# 4) TAREAS (CORRUTINAS) ---------------------------------------
#    Regla de oro: toda tarea con 'while True' debe tener al menos
#    un 'await' dentro del ciclo. Nunca use time.sleep() aquí.
async def tarea_entrada():
    anterior = 1
    while True:
        actual = boton.value()
        if anterior == 1 and actual == 0:
            evento_boton.set()
        anterior = actual
        await asyncio.sleep_ms(20)


async def tarea_salida():
    while True:
        await evento_boton.wait()
        evento_boton.clear()
        estado["modo"] = "rapido" if estado["modo"] == "normal" else "normal"
        print("Modo:", estado["modo"])


async def tarea_periodica():
    while True:
        led.value(not led.value())
        await asyncio.sleep_ms(150 if estado["modo"] == "rapido" else 600)


# 5) FUNCIÓN PRINCIPAL -----------------------------------------
async def main():
    asyncio.create_task(tarea_entrada())
    asyncio.create_task(tarea_salida())
    asyncio.create_task(tarea_periodica())
    while True:                      # main se mantiene viva
        await asyncio.sleep(10)


# 6) ARRANQUE Y LIMPIEZA ---------------------------------------
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Programa detenido por el usuario")
finally:
    led.value(0)
    asyncio.new_event_loop()
