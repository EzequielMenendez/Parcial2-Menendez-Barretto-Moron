import os
from funciones import *
from recorredor_archivos import *
from opciones_menu.agregar_carta import agregar_carta
from opciones_menu.mostrar_cartas import mostrar_cartas_totales
from opciones_menu.filtrar_cartas import filtrar_cartas
from opciones_menu.modificar_carta import modificar_carta
from opciones_menu.eliminar_carta import eliminar_carta
from opciones_menu.funciones_adicionales import funcionalidades_adicionales

def main():
    """Función principal que ejecuta el menú de la aplicación."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    while True:
        limpiar_pantalla()
        cartas_globales = cargar_datos_recursivamente(DATA_DIR)
        
        print("=== Gestor de Cartas de Clash Royale ===")
        print("\nMenú Principal:")
        print("1. Agregar Nueva Carta")
        print("2. Mostrar Todas las Cartas")
        print("3. Filtrar Cartas")
        print("4. Modificar Carta")
        print("5. Eliminar Carta")
        print("6. Funcionalidades Adicionales (Ordenar/Estadísticas)")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        match opcion:
            case "1":
                agregar_carta()
            case "2":
                mostrar_cartas_totales(cartas_globales)
            case "3":
                filtrar_cartas(cartas_globales)
            case "4":
                modificar_carta(cartas_globales)
            case "5":
                eliminar_carta(cartas_globales)
            case "6":
                funcionalidades_adicionales(cartas_globales)
            case "0":
                print("¡Nos vemos en la Arena!"); break
            case _:
                print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()