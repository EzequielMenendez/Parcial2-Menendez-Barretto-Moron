from main import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR, CAMPOS_CSV
from funciones import *

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