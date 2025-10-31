import os
import csv
from main import CAMPOS_CSV

def limpiar_pantalla():
    """Limpia la consola para una mejor experiencia de usuario."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_entero_no_negativo(valor):
    """
    Valida que un valor sea un número entero y no negativo (permite 0).
    Devuelve el número o None si la validación falla.
    """
    try:
        numero = int(valor)
        if numero >= 0:
            return numero
        else:
            print("Error: El número no puede ser negativo.")
            return None
    except ValueError:
        print("Error: El valor debe ser un número entero.")
        return None

def guardar_lista_en_csv(ruta_archivo, lista_items):
    """
    Sobrescribe un archivo CSV con una lista de cartas.
    Utilizado para las operaciones de Modificar y Eliminar.
    """
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=CAMPOS_CSV)
            escritor.writeheader()
            for item in lista_items:
                datos_a_escribir = {campo: item.get(campo) for campo in CAMPOS_CSV}
                escritor.writerow(datos_a_escribir)
        return True
    except IOError as e:
        print(f"Error al escribir en el archivo {ruta_archivo}: {e}")
        return False