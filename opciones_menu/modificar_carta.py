from recorredor_archivos import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR, CAMPOS_CSV
from funciones import *

def modificar_carta(cartas):
    """Busca una carta, permite modificarla con validación en bucle y persiste el cambio."""
    limpiar_pantalla()
    print("--- Modificar Carta ---")
    if not cartas:
        print("No hay cartas para modificar."); return

    nombre_carta = input("Ingrese el nombre exacto de la carta a modificar: ").strip()
    coincidencias = [c for c in cartas if c.get('nombre', '').lower() == nombre_carta.lower()]

    if not coincidencias:
        print(f"No se encontró ninguna carta con el nombre '{nombre_carta}'."); return
    
    carta_a_modificar = coincidencias[0]
    #Si hay varias coincidencias se selecciona una para modificar
    if len(coincidencias) > 1:
        print("Se encontraron varias cartas con ese nombre. Seleccione una:")
        for i, c in enumerate(coincidencias):
            jerarquia = " / ".join([str(c.get(nivel, 'N/A')) for nivel in NIVELES_JERARQUIA])
            print(f"{i + 1}. [{jerarquia}] -> {c.get('nombre')}")
        try:
            opcion = int(input("Seleccione el número: ")) - 1
            if 0 <= opcion < len(coincidencias):
                carta_a_modificar = coincidencias[opcion]
            else:
                print("Opción no válida."); return
        except ValueError:
            print("Entrada no válida."); return

    print(f"\nAtributos modificables: {', '.join(CAMPOS_CSV)}")
    atributo = input("¿Qué atributo desea modificar?: ").strip().lower()

    if atributo not in CAMPOS_CSV:
        print("Error: Atributo no válido."); return

    # Se ingresa el nuevo valor
    item_original = carta_a_modificar.copy()
    mensaje = f"Ingrese el nuevo valor para '{atributo}': "
    if atributo in ['vida', 'daño']:
        carta_a_modificar[atributo] = pedir_entero(mensaje)
    elif atributo == 'nombre':
        carta_a_modificar[atributo] = pedir_texto(mensaje)

    try:
        #se guarda la jerarquía de archivos
        valores_jerarquia = [str(carta_a_modificar.get(nivel)) for nivel in NIVELES_JERARQUIA]
        ruta_archivo_csv = os.path.join(DATA_DIR, *valores_jerarquia, CSV_FILENAME)

        # Se filtra la lista global para encontrar todas las cartas que están en el mismo archivo
        # que la 'carta_a_modificar'. Compara la calidad, tipo y coste_elixir de cada
        # carta con la carta modificada para asegurar que se sobrescriba solo el archivo correcto.
        items_del_mismo_archivo = [
            c for c in cartas if all(str(c.get(n)) == str(carta_a_modificar.get(n)) for n in NIVELES_JERARQUIA)
        ]
        
        if guardar_lista_en_csv(ruta_archivo_csv, items_del_mismo_archivo):
            print("\n¡Carta modificada con éxito!")
        else:
            # Revertir cambio en memoria si falla la escritura
            carta_a_modificar.clear()
            carta_a_modificar.update(item_original)
            print("\nNo se pudo guardar la modificación.")
    except ValueError:
        print("Error de lógica: La carta a modificar no fue encontrada en la lista de memoria.")
    except (IOError, PermissionError) as e:
        print(f"Error al escribir en el archivo: No se pudo guardar el cambio. {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la modificación: {e}")