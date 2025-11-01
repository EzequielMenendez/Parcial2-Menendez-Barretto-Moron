import os
import csv
from recorredor_archivos import CAMPOS_CSV

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
        return None
    except ValueError:
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

#Función para pedir un texto
def pedir_texto(mensaje):
    """Pide un string por consola, valida el texto y que el país no este repetido"""
    while True:
        valor = input(mensaje)
        texto_valido = validar_texto(valor)
        if not texto_valido:
            print("Error: No debe ingresar un dato vacio y no puede contener números o caracteres especiales. 🔴")
            continue
        return valor

def pedir_entero(mensaje):
    """Pide un numero entero por consola y controla errores."""
    while True:
        valor = input(mensaje)
        valor = validar_entero_no_negativo(valor)
        if valor is None:
            print("Error: debe ingresar un numero entero valido no negativo. 🔴")
        else:
            return valor

#Función para validar un texto
def validar_texto(str):
    """Esta función valida un string. No debe contener números ni caracteres especiales"""
    if str.strip() == "":
        return False
    
    permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ. "
    
    return all(c in permitidos for c in str)