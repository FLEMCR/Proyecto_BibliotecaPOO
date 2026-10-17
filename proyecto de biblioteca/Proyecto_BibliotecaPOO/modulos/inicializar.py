# Mira esto que vi en un video de yt, al imprimir el texto lo hace con delay y parece que alguien lo estuviera digitando talvez podriamos usarlo (EJECUTA ESTE ARCHIVO)

import random
import time


def incicializar(texto, min_delay=0.02, max_delay=0.15):
    for digito in texto:
        print(digito, end="", flush=True)
        time.sleep(random.uniform(min_delay, max_delay))
    print()


for fila in [
    "Conectando a la base de datos...",
    "Accediendo al sistema...",
    "Iniciando sesion...",
    "Cargando...",
]:
    incicializar(fila)
    time.sleep(0.5)
