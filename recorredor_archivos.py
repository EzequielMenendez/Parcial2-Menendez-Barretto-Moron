import os
import csv

DATA_DIR = "clash_royale"
CSV_FILENAME = "cartas.csv"
CAMPOS_CSV = ['nombre', 'vida', 'daño']
NIVELES_JERARQUIA = ['calidad', 'tipo', 'coste_elixir']

def cargar_datos_recursivamente(path, jerarquia_actual=None):
    """
    Recorre recursivamente la estructura de directorios y consolida todas las
    cartas de los archivos CSV en una sola lista de diccionarios.
    """
    if jerarquia_actual is None:
        jerarquia_actual = {}

    items_totales = []
    #Si el archivo es un csv lo abre y retorna sus cartas(CASO BASE)
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
    #Si el archivo es una carpeta la recorre(CASO RECURSIVO)
    if os.path.isdir(path):
        relative_path = path.replace(DATA_DIR, '').strip(os.sep)
        depth = len(relative_path.split(os.sep)) if relative_path else 0
        #Voy guardando la ruta
        for elemento in os.listdir(path):
            ruta_completa = os.path.join(path, elemento)
            nueva_jerarquia = jerarquia_actual.copy()

            if os.path.isdir(ruta_completa) and depth < len(NIVELES_JERARQUIA):
                key_jerarquia = NIVELES_JERARQUIA[depth]
                nueva_jerarquia[key_jerarquia] = elemento
            
            items_totales.extend(cargar_datos_recursivamente(ruta_completa, nueva_jerarquia))

    return items_totales