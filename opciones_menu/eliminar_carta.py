from funciones import *
from main import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR

def eliminar_carta(cartas):
    """Busca una carta y la elimina, persistiendo el cambio."""
    limpiar_pantalla()
    print("--- Eliminar Carta ---")
    if not cartas:
        print("No hay cartas para eliminar."); return

    nombre_carta = input("Ingrese el nombre exacto de la carta a eliminar: ").strip()
    coincidencias = [c for c in cartas if c.get('nombre', '').lower() == nombre_carta.lower()]

    if not coincidencias:
        print(f"No se encontró '{nombre_carta}'."); return

    carta_a_eliminar = coincidencias[0]
    if len(coincidencias) > 1:
        print("Se encontraron varias cartas con ese nombre. Seleccione una:")
        for i, c in enumerate(coincidencias):
            jerarquia = " / ".join([str(c.get(nivel, 'N/A')) for nivel in NIVELES_JERARQUIA])
            print(f"{i + 1}. [{jerarquia}] -> {c.get('nombre')}")
        try:
            opcion = int(input("Seleccione el número: ")) - 1
            if 0 <= opcion < len(coincidencias):
                carta_a_eliminar = coincidencias[opcion]
            else:
                print("Opción no válida."); return
        except ValueError:
            print("Entrada no válida."); return

    if input(f"¿Seguro que desea eliminar '{carta_a_eliminar['nombre']}'? (s/n): ").lower() != 's':
        print("Eliminación cancelada."); return

    try:
        cartas.remove(carta_a_eliminar)
        valores_jerarquia = [str(carta_a_eliminar.get(nivel)) for nivel in NIVELES_JERARQUIA]
        ruta_archivo_csv = os.path.join(DATA_DIR, *valores_jerarquia, CSV_FILENAME)

        items_del_mismo_archivo = [
            c for c in cartas if all(str(c.get(n)) == str(carta_a_eliminar.get(n)) for n in NIVELES_JERARQUIA)
        ]
        
        if guardar_lista_en_csv(ruta_archivo_csv, items_del_mismo_archivo):
            print("\n¡Carta eliminada con éxito!")
        else:
            cartas.append(carta_a_eliminar) # Revertir
            print("\nNo se pudo persistir la eliminación.")
    except Exception as e:
        print(f"Error durante la eliminación: {e}")