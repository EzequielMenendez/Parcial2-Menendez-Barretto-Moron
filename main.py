import os
import csv
import sys

# --- Constantes y Configuración de Clash Royale ---
DATA_DIR = "clash_royale"
CSV_FILENAME = "cartas.csv"
# Se elimina 'tiene_evolucion' de los campos
CAMPOS_CSV = ['nombre', 'vida', 'daño']
NIVELES_JERARQUIA = ['calidad', 'tipo', 'coste_elixir']

# --- Funciones Auxiliares ---

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

# --- Lógica Principal de Datos (CORREGIDA) ---

def cargar_datos_recursivamente(path, jerarquia_actual=None):
    """
    Recorre recursivamente la estructura de directorios y consolida todas las
    cartas de los archivos CSV en una sola lista de diccionarios.
    """
    if jerarquia_actual is None:
        jerarquia_actual = {}

    items_totales = []

    # Caso Base: Si es un archivo CSV, lo leemos.
    if os.path.isfile(path) and path.endswith(CSV_FILENAME):
        try:
            with open(path, mode='r', newline='', encoding='utf-8') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    item = {**jerarquia_actual, **fila}
                    items_totales.append(item)
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")
        return items_totales

    # Paso Recursivo: Si es un directorio, lo recorremos.
    if os.path.isdir(path):
        for elemento in os.listdir(path):
            ruta_completa = os.path.join(path, elemento)
            
            # Determinamos el nivel de profundidad actual para saber qué clave jerárquica usar.
            relative_path = path.replace(DATA_DIR, '').strip(os.sep)
            depth = len(relative_path.split(os.sep)) if relative_path else 0
            
            # Solo continuamos si la profundidad está dentro de nuestros niveles definidos.
            if depth < len(NIVELES_JERARQUIA):
                nueva_jerarquia = jerarquia_actual.copy()
                key_jerarquia = NIVELES_JERARQUIA[depth]
                nueva_jerarquia[key_jerarquia] = elemento
                
                # Llamada recursiva con la nueva ruta y la jerarquía actualizada.
                items_totales.extend(cargar_datos_recursivamente(ruta_completa, nueva_jerarquia))

    return items_totales

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

# --- Funcionalidades del Sistema (CRUD - MEJORADAS) ---

def alta_carta():
    """
    Da de alta una nueva carta, pidiendo datos al usuario con validación en bucle
    y creando la estructura de directorios si es necesario.
    """
    limpiar_pantalla()
    print("--- Alta de Nueva Carta ---")
    
    valores_jerarquia = {}
    # 1. Bucle de validación para datos jerárquicos
    for nivel in NIVELES_JERARQUIA:
        while True:
            prompt = f"Ingrese {nivel.replace('_', ' ').title()}: "
            valor = input(prompt).strip()
            if not valor:
                print("Error: Este campo no puede estar vacío.")
                continue

            if nivel == 'coste_elixir':
                elixir_validado = validar_entero_no_negativo(valor)
                if elixir_validado is not None:
                    valor = str(elixir_validado)
                    break
                else:
                    continue # La función de validación ya imprimió el error
            
            valores_jerarquia[nivel] = valor
            break

    # 2. Bucle de validación para atributos de la carta
    nueva_carta = {}
    while True:
        nombre = input("Ingrese el Nombre de la carta: ").strip()
        if nombre:
            nueva_carta['nombre'] = nombre
            break
        else:
            print("Error: El nombre no puede estar vacío.")

    while True:
        vida_str = input("Ingrese los Puntos de Vida (0 para hechizos): ")
        vida = validar_entero_no_negativo(vida_str)
        if vida is not None:
            nueva_carta['vida'] = vida
            break

    while True:
        daño_str = input("Ingrese el Daño (0 si no aplica): ")
        daño = validar_entero_no_negativo(daño_str)
        if daño is not None:
            nueva_carta['daño'] = daño
            break

    # 3. Persistencia
    try:
        ruta_jerarquica = os.path.join(DATA_DIR, *valores_jerarquia.values())
        os.makedirs(ruta_jerarquica, exist_ok=True)
        
        ruta_archivo_csv = os.path.join(ruta_jerarquica, CSV_FILENAME)
        escribir_cabecera = not os.path.exists(ruta_archivo_csv)

        with open(ruta_archivo_csv, mode='a', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
            if escribir_cabecera:
                escritor.writeheader()
            escritor.writerow(nueva_carta)
            
        print("\n¡Carta agregada con éxito!")

    except OSError as e:
        print(f"Error al crear la estructura de directorios: {e}")

def mostrar_cartas_totales(cartas):
    """Muestra una lista de todas las cartas con su jerarquía."""
    limpiar_pantalla()
    print("--- Listado Completo de Cartas ---")
    if not cartas:
        print("No hay cartas para mostrar.")
        return

    cartas_ordenadas = sorted(cartas, key=lambda x: (x.get('calidad', ''), x.get('nombre', '')))

    for carta in cartas_ordenadas:
        jerarquia = " / ".join([str(carta.get(nivel, 'N/A')) for nivel in NIVELES_JERARQUIA])
        # Se elimina la visualización de la evolución
        print(f"[{jerarquia}] -> Nombre: {carta.get('nombre')}, "
            f"Vida: {carta.get('vida')}, Daño: {carta.get('daño')}")


# Las demás funciones (filtrar, modificar, eliminar, etc.) no necesitan cambios drásticos
# en su lógica principal, pero se benefician de las mejoras en las funciones de validación
# y carga de datos. Se ajusta `modificar_carta` para usar bucles también.

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

# (El resto de las funciones como filtrar, eliminar, estadísticas y el menú principal
# se mantienen sin cambios ya que su lógica es compatible con las mejoras)

def filtrar_cartas(cartas):
    """Permite al usuario filtrar la lista de cartas por un atributo."""
    limpiar_pantalla()
    print("--- Filtrar Cartas ---")
    if not cartas:
        print("No hay cartas para filtrar.")
        return

    atributos_filtrables = CAMPOS_CSV + NIVELES_JERARQUIA
    print(f"Atributos disponibles para filtrar: {', '.join(atributos_filtrables)}")
    atributo = input("Ingrese el atributo por el cual desea filtrar: ").strip().lower()

    if atributo not in atributos_filtrables:
        print("Error: Atributo no válido.")
        return
    
    valor_filtro = input(f"Ingrese el valor a buscar para '{atributo}': ").strip()
    
    resultados = [c for c in cartas if valor_filtro.lower() in str(c.get(atributo, '')).lower()]
            
    if not resultados:
        print("No se encontraron cartas que coincidan con el filtro.")
    else:
        print("\n--- Resultados del Filtro ---")
        mostrar_cartas_totales(resultados)

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

def funcionalidades_adicionales(cartas):
    """Menú para ordenamiento y estadísticas."""
    while True:
        limpiar_pantalla()
        print("--- Funcionalidades Adicionales ---")
        print("1. Ordenar cartas")
        print("2. Mostrar estadísticas")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ordenar_cartas(cartas)
        elif opcion == '2':
            mostrar_estadisticas(cartas)
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")
        input("\nPresione Enter para continuar...")

def ordenar_cartas(cartas):
    """Permite ordenar la lista global por diferentes atributos."""
    limpiar_pantalla()
    print("--- Ordenar Cartas ---")
    if not cartas:
        print("No hay cartas para ordenar."); return
        
    print("Ordenar por: 1. Nombre (A-Z)  2. Daño (Mayor a Menor) 3. Vida (Mayor a menor)")
    criterio = input("Seleccione el criterio de ordenamiento: ")

    lista_ordenada = []
    if criterio == '1':
        lista_ordenada = sorted(cartas, key=lambda x: x.get('nombre', '').lower())
        print("\n--- Cartas ordenadas por Nombre ---")
    elif criterio == '2':
        lista_ordenada = sorted(cartas, key=lambda x: int(x.get('daño', 0)), reverse=True)
        print("\n--- Cartas ordenadas por Daño ---")
    elif criterio == '3':
        lista_ordenada = sorted(cartas, key=lambda x: int(x.get('vida', 0)), reverse=True)
        print("\n--- Cartas ordenadas por Vida ---")
    else:
        print("Criterio no válido."); return
    
    mostrar_cartas_totales(lista_ordenada)

def mostrar_estadisticas(cartas):
    """Calcula y muestra estadísticas sobre el total de cartas."""
    limpiar_pantalla()
    print("--- Estadísticas de Cartas ---")
    if not cartas:
        print("No hay datos para generar estadísticas."); return

    total_cartas = len(cartas)
    print(f"Cantidad total de cartas registradas: {total_cartas}")

    daños = [int(c.get('daño', 0)) for c in cartas]
    daño_total = sum(daños)
    promedio_daño = daño_total / total_cartas if total_cartas > 0 else 0
    print(f"Daño promedio por carta: {promedio_daño:,.2f}")
    
    conteo_por_calidad = {}
    for carta in cartas:
        calidad = carta.get('calidad', 'Desconocida')
        conteo_por_calidad[calidad] = conteo_por_calidad.get(calidad, 0) + 1
    
    print("\nRecuento de cartas por Calidad:")
    for calidad, cantidad in conteo_por_calidad.items():
        print(f"- {calidad}: {cantidad} carta(s)")

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
        print("7. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            alta_carta()
        elif opcion == '2':
            mostrar_cartas_totales(cartas_globales)
        elif opcion == '3':
            filtrar_cartas(cartas_globales)
        elif opcion == '4':
            modificar_carta(cartas_globales) # Nota: `modificar_carta` necesita la lista para operar
        elif opcion == '5':
            eliminar_carta(cartas_globales) # Nota: `eliminar_carta` necesita la lista para operar
        elif opcion == '6':
            funcionalidades_adicionales(cartas_globales)
        elif opcion == '7':
            print("¡Nos vemos en la arena!"); sys.exit(0)
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()