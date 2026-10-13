# =============================================================
# Ejemplo 4 — La MISMA tarea resuelta de tres formas
#   "thread"  -> _thread (hilos de FreeRTOS)
#   "timer"   -> machine.Timer (callback periódico)
#   "asyncio" -> corrutinas cooperativas
# Placa: ESP32 con MicroPython. LED en GPIO2.
# Cambie la variable MODO y compare el comportamiento.
# =============================================================
MODO = "asyncio"          # "thread" | "timer" | "asyncio"

from machine import Pin, Timer
import time

led = Pin(2, Pin.OUT)

# -------------------------------------------------------------
if MODO == "thread":
    # Cada hilo tiene su propia pila (~4 KB o más) y el sistema
    # operativo lo interrumpe cuando quiere (multitarea PREEMPTIVA).
    # Riesgo: dos hilos tocando la misma variable -> condición de carrera.
    import _thread

    candado = _thread.allocate_lock()
    contador = 0

    def tarea_led():
        global contador
        while True:
            led.value(not led.value())
            with candado:            # proteger datos compartidos
                contador += 1
            time.sleep_ms(500)

    _thread.start_new_thread(tarea_led, ())

    while True:
        with candado:
            print("[thread] cambios de LED:", contador)
        time.sleep(2)

# -------------------------------------------------------------
elif MODO == "timer":
    # El Timer llama a la función cada 500 ms. El callback debe
    # ser MUY corto: nada de print largos, sleep ni lecturas lentas.
    def al_vencer(t):
        led.value(not led.value())

    tim = Timer(0)                   # el ESP32 tiene timers 0 a 3
    tim.init(period=500, mode=Timer.PERIODIC, callback=al_vencer)

    while True:
        print("[timer] el programa principal sigue libre")
        time.sleep(2)

# -------------------------------------------------------------
else:
    # Una sola pila, un solo hilo. Cada tarea decide cuándo ceder
    # (multitarea COOPERATIVA) en cada 'await'. Sin candados.
    import asyncio

    contador = 0

    async def tarea_led():
        global contador
        while True:
            led.value(not led.value())
            contador += 1            # seguro: nadie nos interrumpe aquí
            await asyncio.sleep_ms(500)

    async def tarea_reporte():
        while True:
            print("[asyncio] cambios de LED:", contador)
            await asyncio.sleep(2)

    async def main():
        await asyncio.gather(tarea_led(), tarea_reporte())

    asyncio.run(main())
