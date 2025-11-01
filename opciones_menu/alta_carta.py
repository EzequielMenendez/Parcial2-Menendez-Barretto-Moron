from recorredor_archivos import CSV_FILENAME, NIVELES_JERARQUIA, DATA_DIR, CAMPOS_CSV
from funciones import *

def alta_carta():
    """
    Da de alta una nueva carta, pidiendo datos al usuario con validación en bucle
    y creando la estructura de directorios si es necesario.
    """
    limpiar_pantalla()
    print("--- Alta de Nueva Carta ---")
    
    valores_jerarquia = {}
    # Hace un buqule por cada nivel de jerarquía
    for nivel in NIVELES_JERARQUIA:
        #Se usa while para validar ingreso correcto de datos
        while True:
            prompt = f"Ingrese {nivel.replace('_', ' ').title()}: "
            valor = input(prompt).strip()
            if not valor:
                print("Error: Este campo no puede estar vacío.")
                continue
            
            #Si es el ultimo nivel de jerarquía guarda el valor y rompe el ciclo. Si no continua recorriendo
            if nivel == 'coste_elixir':
                elixir_validado = validar_entero_no_negativo(valor)
                if elixir_validado is not None:
                    valor = str(elixir_validado)
                else:
                    print("El elixir debe ser un número no negativo.")
                    continue
            
            valores_jerarquia[nivel] = valor
            break

    #se piden los datos de la carta
    nueva_carta = {}
    nueva_carta['nombre'] = pedir_texto("Ingrese el nombre de la carta: ")
    nueva_carta['vida'] = pedir_entero("Ingrese los Puntos de Vida: ")
    nueva_carta['daño'] = pedir_entero("Ingrese el Daño: ")

    #Se guardan los datos en el csv
    try:
        # Esta línea ahora recibirá los 3 valores y funcionará
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