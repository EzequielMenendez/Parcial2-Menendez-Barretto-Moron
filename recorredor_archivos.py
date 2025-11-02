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
                    #Primero, creamos un nuevo diccionario para la carta
                    #copiando la jerarquía que ya conocemos (ej. {'calidad': 'Epica', ...})
                    item = jerarquia_actual.copy()
                    
                    #Luego, actualizamos ese diccionario con los datos de la fila del CSV
                    #(ej. {'nombre': 'Pekka', 'vida': 3000, ...})
                    item.update(fila)
                    
                    items_totales.append(item)
                    
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")
        return items_totales
    
    #Si el archivo es una carpeta la recorre(CASO RECURSIVO)
    if os.path.isdir(path):
        # Primero, obtenemos la ruta relativa, quitando la carpeta base.
        # Ej. "clash_royale/Epica/Tropa" -> "Epica/Tropa"
        relative_path = path.replace(DATA_DIR, '')
        relative_path = relative_path.strip(os.sep)
        
        #Ahora calculamos la profundidad
        if relative_path == '':
            #Si la ruta relativa está vacía, estamos en la carpeta raíz.
            profundidad = 0
        else:
            #Si no está vacía, separamos la ruta por las barras
            #Ej. "Epica/Tropa" -> ['Epica', 'Tropa']
            partes_de_la_ruta = relative_path.split(os.sep)
            #La profundidad es la cantidad de carpetas en esa lista.
            profundidad = len(partes_de_la_ruta)
            
        try:
            #Recorro el path
            for elemento in os.listdir(path):
                #Se le agrega a la ruta el elemento actual
                # Ej: path="clash_royale/Epica", elemento="Tropa" -> ruta_completa="clash_royale/Epica/Tropa"
                ruta_completa = os.path.join(path, elemento)

                #Crea una copia del diccionario de jerarquía actual.
                nueva_jerarquia = jerarquia_actual.copy()

                #Si el elemento actual es una carpeta y faltan niveles de jerarquía
                if os.path.isdir(ruta_completa) and profundidad < len(NIVELES_JERARQUIA):
                    key_jerarquia = NIVELES_JERARQUIA[profundidad]
                    nueva_jerarquia[key_jerarquia] = elemento
                
                #Llamamos a la recursión, extendiendo la lista total
                cartas_encontradas = cargar_datos_recursivamente(ruta_completa, nueva_jerarquia)
                items_totales.extend(cartas_encontradas)
        
        except PermissionError:
            print(f"Error: No se tienen permisos para acceder a la carpeta {path}.")
        except OSError as e:
            print(f"Error del sistema al leer la carpeta {path}: {e}")
            
    return items_totales