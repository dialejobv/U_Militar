# =============================================================
# Ejemplo 3 — Corrutinas con async / await
# Placa: ESP32 con MicroPython (v1.20 o superior: "import asyncio")
# Conexiones: LED rojo en GPIO2 (integrado), LED verde en GPIO15
#             (con resistencia de 220 Ω a GND)
# -------------------------------------------------------------
# async def  -> define una CORRUTINA (una función que puede pausarse)
# await      -> "pausa aquí y deja trabajar a las demás tareas"
# create_task-> pone la corrutina a correr de forma concurrente
# =============================================================
import asyncio
from machine import Pin

led_rojo = Pin(2, Pin.OUT)
led_verde = Pin(15, Pin.OUT)


# Una corrutina reutilizable: la misma función maneja cualquier LED
async def parpadear(led, periodo_ms, nombre):
    while True:
        led.value(not led.value())
        await asyncio.sleep_ms(periodo_ms)   # cede el control, NO bloquea


# Una corrutina también puede DEVOLVER un valor
async def leer_promedio(n_muestras):
    suma = 0
    for i in range(n_muestras):
        suma += i * 10                   # (aquí iría la lectura real del sensor)
        await asyncio.sleep_ms(100)      # entre muestras otros pueden trabajar
    return suma / n_muestras


async def main():
    # Las dos tareas de parpadeo corren "al mismo tiempo"
    asyncio.create_task(parpadear(led_rojo, 500, "rojo"))
    asyncio.create_task(parpadear(led_verde, 1300, "verde"))

    while True:
        # await espera el resultado SIN detener los LEDs
        promedio = await leer_promedio(10)
        print("Promedio calculado:", promedio)
        await asyncio.sleep(2)


asyncio.run(main())   # arranca el planificador (event loop)
