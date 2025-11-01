from recorredor_archivos import NIVELES_JERARQUIA, CAMPOS_CSV
from funciones import *
from opciones_menu.mostrar_cartas import mostrar_cartas_totales

def filtrar_cartas(cartas):
    """Permite al usuario filtrar la lista de cartas por un atributo."""
    limpiar_pantalla()
    print("--- Filtrar Cartas ---")
    if not cartas:
        print("No hay cartas para filtrar.")
        return
    #guarda los filtros posible
    atributos_filtrables = CAMPOS_CSV + NIVELES_JERARQUIA
    print(f"Atributos disponibles para filtrar: {', '.join(atributos_filtrables)}")
    atributo = input("Ingrese el atributo por el cual desea filtrar: ").strip().lower()
    #se pide ingresar un filtro
    if atributo not in atributos_filtrables:
        print("Error: Atributo no válido.")
        return
    
    valor_filtro = input(f"Ingrese el valor a buscar para '{atributo}': ").strip()
    # Se filtra la lista global para encontrar todas las cartas que están en el mismo archivo
    # que la 'carta_a_modificar'. Compara la calidad, tipo y coste_elixir de cada
    # carta con la carta modificada para asegurar que se sobrescriba solo el archivo correcto.
    resultados = [c for c in cartas if valor_filtro.lower() in str(c.get(atributo, '')).lower()]
            
    if not resultados:
        print("No se encontraron cartas que coincidan con el filtro.")
    else:
        print("\n--- Resultados del Filtro ---")
        mostrar_cartas_totales(resultados)
