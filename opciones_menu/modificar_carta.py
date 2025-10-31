from main import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR, CAMPOS_CSV
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
    
    # Lógica para seleccionar una carta si hay duplicados
    carta_a_modificar = coincidencias[0]
    if len(coincidencias) > 1:
        # (El código para manejar duplicados se mantiene igual)
        pass # Placeholder for brevity

    print(f"\nAtributos modificables: {', '.join(CAMPOS_CSV)}")
    atributo = input("¿Qué atributo desea modificar?: ").strip().lower()

    if atributo not in CAMPOS_CSV:
        print("Error: Atributo no válido."); return

    # Bucle de validación para el nuevo valor
    while True:
        nuevo_valor_str = input(f"Ingrese el nuevo valor para '{atributo}': ").strip()
        valor_validado = None
        if atributo in ['vida', 'daño']:
            valor_validado = validar_entero_no_negativo(nuevo_valor_str)
        elif atributo == 'nombre':
            if nuevo_valor_str:
                valor_validado = nuevo_valor_str
            else:
                print("El nombre no puede estar vacío.")

        if valor_validado is not None:
            break # Salimos del bucle si el valor es válido
    
    # Actualizar en memoria y persistir
    item_original = carta_a_modificar.copy()
    carta_a_modificar[atributo] = valor_validado

    try:
        # (El resto de la lógica para guardar el archivo se mantiene igual)
        valores_jerarquia = [str(carta_a_modificar.get(nivel)) for nivel in NIVELES_JERARQUIA]
        ruta_archivo_csv = os.path.join(DATA_DIR, *valores_jerarquia, CSV_FILENAME)
        items_del_mismo_archivo = [c for c in cartas if all(str(c.get(n)) == str(carta_a_modificar.get(n)) for n in NIVELES_JERARQUIA)]
        if guardar_lista_en_csv(ruta_archivo_csv, items_del_mismo_archivo):
            print("\n¡Carta modificada con éxito!")
        else:
            # Revertir cambio en memoria
            carta_a_modificar.clear()
            carta_a_modificar.update(item_original)
            print("\nNo se pudo guardar la modificación.")
    except Exception as e:
        print(f"Error al intentar guardar la modificación: {e}")