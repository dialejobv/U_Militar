# 13) Programación asincrónica en el ESP32

Simulación interactiva y ejemplos en MicroPython sobre programación asincrónica con `asyncio`.

**Simulación en línea:** [Simulador asyncio ESP32](https://dialejobv.github.io/U_Militar/13%29%20Esp_async/)

## Temas

- Bloqueante vs no bloqueante
- Corrutinas (`async`, `await`)
- Diferencia entre threads, Timers y asyncio
- Ventajas de asyncio en sistemas embebidos: bajo consumo, varios sensores y actuadores en paralelo, respuesta rápida a eventos
- Estructura básica de un programa con asyncio

## Contenido de la carpeta

| Archivo | Qué muestra |
|---|---|
| `index.html` | Simulación en HTML5, CSS y JavaScript (se publica con GitHub Pages) |
| `ejemplos/01_bloqueante.py` | Un programa con `time.sleep()` que pierde pulsaciones del botón |
| `ejemplos/02_no_bloqueante_ticks.py` | Sondeo con `ticks_ms()`: responde rápido pero la CPU nunca descansa |
| `ejemplos/03_corrutinas_async_await.py` | Dos LEDs con distinto ritmo usando corrutinas |
| `ejemplos/04_threads_timers_asyncio.py` | La misma tarea con `_thread`, `machine.Timer` y `asyncio` (variable `MODO`) |
| `ejemplos/05_sensores_actuadores.py` | Potenciómetro, servo, DHT22, buzzer y LED en cinco tareas |
| `ejemplos/06_respuesta_eventos.py` | Interrupción + `ThreadSafeFlag` + `Event` |
| `ejemplos/07_bajo_consumo.py` | `machine.freq()`, tareas con `gather()` y `deepsleep()` |
| `ejemplos/08_plantilla_asyncio.py` | Plantilla base para proyectos |

## Conexiones usadas en los ejemplos

| Componente | Pin del ESP32 |
|---|---|
| LED integrado | GPIO2 |
| Botón BOOT | GPIO0 (pull-up) |
| Potenciómetro | GPIO34 (ADC) |
| Servo SG90 | GPIO18 (PWM 50 Hz) |
| DHT22 | GPIO4 |
| Buzzer | GPIO19 (PWM) |

Los ejemplos requieren MicroPython 1.20 o superior (`import asyncio`). En firmware más antiguo use `import uasyncio as asyncio`.

## Cómo usar la simulación en clase

1. Elija el modo **Bloqueante** y presione **Ráfaga de 5 pulsaciones**.
2. Observe la línea de tiempo: las barras naranjas son el programa congelado en `sleep()`.
3. Repita con **Sondeo** y con **asyncio**, moviendo el potenciómetro y la temperatura.
4. Compare la tabla final: pulsaciones detectadas, latencia y CPU ocupada.
