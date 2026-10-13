# =============================================================
# Ejemplo 7 — asyncio y bajo consumo
# Placa: ESP32 con MicroPython
# Conexiones: sensor analógico (LDR o potenciómetro) en GPIO34
# -------------------------------------------------------------
# Estrategia de un nodo de sensores con batería:
#   1. Bajar la frecuencia de la CPU (240 MHz -> 80 MHz).
#   2. Hacer todo el trabajo con tareas asyncio: mientras esperan,
#      el planificador no gira en un bucle de sondeo.
#   3. Cuando TODO terminó, dormir profundamente (deep sleep).
#      El ESP32 se reinicia al despertar y vuelve a ejecutar main.py.
# Guarde este archivo como main.py para probar el ciclo completo.
# =============================================================
import asyncio
import machine
from machine import Pin, ADC

machine.freq(80_000_000)          # menos MHz = menos corriente

sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)
led = Pin(2, Pin.OUT)

SEGUNDOS_DORMIDO = 30


async def medir(n_muestras, separacion_ms):
    muestras = []
    for _ in range(n_muestras):
        muestras.append(sensor.read_u16())
        await asyncio.sleep_ms(separacion_ms)   # espera sin sondeo
    return sum(muestras) // len(muestras)


async def indicar_actividad():
    # Destello corto para saber que el nodo está despierto
    led.value(1)
    await asyncio.sleep_ms(50)
    led.value(0)


async def main():
    # Medición e indicación ocurren de forma concurrente
    promedio, _ = await asyncio.gather(medir(10, 100), indicar_actividad())
    print("Promedio:", promedio)
    # (aquí se enviaría el dato por Wi-Fi/ESP-NOW/LoRa)


asyncio.run(main())

print("Durmiendo", SEGUNDOS_DORMIDO, "s...")
machine.deepsleep(SEGUNDOS_DORMIDO * 1000)    # consumo de microamperios
