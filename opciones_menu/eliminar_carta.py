from funciones import *
from recorredor_archivos import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR

def eliminar_carta(cartas):
    """Busca una carta y la elimina, persistiendo el cambio."""
    limpiar_pantalla()
    print("--- Eliminar Carta ---")
    if not cartas:
        print("No hay cartas para eliminar."); return

    #Se ingresa una carta y se buscan coincidencias
    nombre_carta = input("Ingrese el nombre exacto de la carta a eliminar: ").strip()
    coincidencias = [c for c in cartas if c.get('nombre', '').lower() == nombre_carta.lower()]
    if not coincidencias:
        print(f"No se encontró '{nombre_carta}'."); return

    carta_a_eliminar = coincidencias[0]
    #Si hay varias coincidencias se selecciona una para eliminar
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

    try:
        #Se elimina la carta de la lista
        cartas.remove(carta_a_eliminar)
        valores_jerarquia = [str(carta_a_eliminar.get(nivel)) for nivel in NIVELES_JERARQUIA]
        ruta_archivo_csv = os.path.join(DATA_DIR, *valores_jerarquia, CSV_FILENAME)
        #se genera una lista que compara la calidad, tipo y elixir de la carta a eliminar para validar si se encuentra en el mismo archivo que la carta a eliminar
        #y guarda las coincidencias
        items_del_mismo_archivo = [
            c for c in cartas if all(str(c.get(n)) == str(carta_a_eliminar.get(n)) for n in NIVELES_JERARQUIA)
        ]
        
        if guardar_lista_en_csv(ruta_archivo_csv, items_del_mismo_archivo):
            print("\n¡Carta eliminada con éxito!")
        else:
            cartas.append(carta_a_eliminar) # Revertir
            print("\nNo se pudo persistir la eliminación.")
    except ValueError:
        print("Error de lógica: La carta a eliminar no fue encontrada en la lista de memoria.")
    except (IOError, PermissionError) as e:
        print(f"Error al escribir en el archivo: No se pudo guardar el cambio. {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la eliminación: {e}")