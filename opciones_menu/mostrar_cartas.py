from recorredor_archivos import NIVELES_JERARQUIA
from funciones import *

def mostrar_cartas_totales(cartas):
    """Muestra una lista de todas las cartas con su jerarquía."""
    limpiar_pantalla()
    print("--- Listado Completo de Cartas ---")
    if not cartas:
        print("No hay cartas para mostrar.")
        return
    #Muestra las cartas
    for carta in cartas:
        jerarquia = " / ".join([str(carta.get(nivel, 'N/A')) for nivel in NIVELES_JERARQUIA])
        print(f"[{jerarquia}] -> Nombre: {carta.get('nombre')}, "
            f"Vida: {carta.get('vida')}, Daño: {carta.get('daño')}")