import os
import sys
from funciones import *
from recorredor_archivos import cargar_datos_recursivamente
from opciones_menu.alta_carta import alta_carta
from opciones_menu.mostrar_cartas import mostrar_cartas_totales
from opciones_menu.filtrar_cartas import filtrar_cartas
from opciones_menu.modificar_carta import modificar_carta
from opciones_menu.eliminar_carta import eliminar_carta
from opciones_menu.funciones_adicionales import funcionalidades_adicionales

DATA_DIR = "clash_royale"
CSV_FILENAME = "cartas.csv"
CAMPOS_CSV = ['nombre', 'vida', 'daño']
NIVELES_JERARQUIA = ['calidad', 'tipo', 'coste_elixir']

def main():
    """Función principal que ejecuta el menú de la aplicación."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    while True:
        limpiar_pantalla()
        cartas_globales = cargar_datos_recursivamente(DATA_DIR)
        
        print("--- Gestor de Cartas de Clash Royale ---")
        print("\nMenú Principal:")
        print("1. Alta de Nueva Carta")
        print("2. Mostrar Todas las Cartas")
        print("3. Filtrar Cartas")
        print("4. Modificar Carta")
        print("5. Eliminar Carta")
        print("6. Funcionalidades Adicionales (Ordenar/Estadísticas)")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            alta_carta()
        elif opcion == '2':
            mostrar_cartas_totales(cartas_globales)
        elif opcion == '3':
            filtrar_cartas(cartas_globales)
        elif opcion == '4':
            modificar_carta(cartas_globales)
        elif opcion == '5':
            eliminar_carta(cartas_globales)
        elif opcion == '6':
            funcionalidades_adicionales(cartas_globales)
        elif opcion == '0':
            print("¡Nos vemos en la arena!"); sys.exit(0)
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()