import os
import csv
from main import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR

def cargar_datos_recursivamente(path, jerarquia_actual=None):
    """
    Recorre recursivamente la estructura de directorios y consolida todas las
    cartas de los archivos CSV en una sola lista de diccionarios.
    """
    if jerarquia_actual is None:
        jerarquia_actual = {}

    items_totales = []

    # Caso Base: Si es un archivo CSV, lo leemos.
    if os.path.isfile(path) and path.endswith(CSV_FILENAME):
        try:
            with open(path, mode='r', newline='', encoding='utf-8') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    item = {**jerarquia_actual, **fila}
                    items_totales.append(item)
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")
        return items_totales

    # Paso Recursivo: Si es un directorio, lo recorremos.
    if os.path.isdir(path):
        for elemento in os.listdir(path):
            ruta_completa = os.path.join(path, elemento)
            
            # Determinamos el nivel de profundidad actual para saber qué clave jerárquica usar.
            relative_path = path.replace(DATA_DIR, '').strip(os.sep)
            depth = len(relative_path.split(os.sep)) if relative_path else 0
            
            # Solo continuamos si la profundidad está dentro de nuestros niveles definidos.
            if depth < len(NIVELES_JERARQUIA):
                nueva_jerarquia = jerarquia_actual.copy()
                key_jerarquia = NIVELES_JERARQUIA[depth]
                nueva_jerarquia[key_jerarquia] = elemento
                
                # Llamada recursiva con la nueva ruta y la jerarquía actualizada.
                items_totales.extend(cargar_datos_recursivamente(ruta_completa, nueva_jerarquia))

    return items_totales