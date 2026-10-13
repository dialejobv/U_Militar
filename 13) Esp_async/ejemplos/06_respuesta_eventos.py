# =============================================================
# Ejemplo 6 — Respuesta rápida a eventos
# Placa: ESP32 con MicroPython
# Conexiones: botón BOOT en GPIO0, LED en GPIO2
# -------------------------------------------------------------
# 1) La interrupción (IRQ) del botón solo levanta una bandera.
# 2) Una tarea dormida en 'await bandera.wait()' despierta al instante.
# 3) Esa tarea avisa a otras con asyncio.Event.
# Mientras tanto, un "trabajo pesado" se divide en trozos
# y cede el control con 'await asyncio.sleep_ms(0)'.
# =============================================================
import asyncio
import time
from machine import Pin

boton = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

bandera_boton = asyncio.ThreadSafeFlag()   # segura para usar desde una IRQ
evento_alarma = asyncio.Event()            # comunica tareas entre sí
t_pulsacion = 0


def irq_boton(pin):
    # La rutina de interrupción debe ser mínima
    global t_pulsacion
    t_pulsacion = time.ticks_ms()
    bandera_boton.set()


boton.irq(trigger=Pin.IRQ_FALLING, handler=irq_boton)


async def atender_boton():
    while True:
        await bandera_boton.wait()          # duerme sin gastar CPU
        await asyncio.sleep_ms(20)          # antirrebote
        if boton.value() == 0:
            retardo = time.ticks_diff(time.ticks_ms(), t_pulsacion)
            print("Botón atendido en", retardo, "ms")
            evento_alarma.set()


async def reaccionar_alarma():
    while True:
        await evento_alarma.wait()
        evento_alarma.clear()
        for _ in range(6):                  # parpadeo rápido de aviso
            led.value(not led.value())
            await asyncio.sleep_ms(80)
        led.value(0)


async def trabajo_pesado():
    # Un cálculo largo NO debe acaparar la CPU:
    # se parte en trozos y se cede el control entre ellos.
    while True:
        total = 0
        for i in range(20000):
            total += i * i
            if i % 500 == 0:
                await asyncio.sleep_ms(0)   # "deja pasar" a las demás tareas
        print("Cálculo terminado:", total)
        await asyncio.sleep(3)


async def main():
    await asyncio.gather(atender_boton(), reaccionar_alarma(), trabajo_pesado())


asyncio.run(main())
