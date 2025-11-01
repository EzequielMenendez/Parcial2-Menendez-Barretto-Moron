from funciones import *
from opciones_menu.mostrar_cartas import mostrar_cartas_totales

def funcionalidades_adicionales(cartas):
    """Menú para ordenamiento y estadísticas."""
    while True:
        limpiar_pantalla()
        print("--- Funcionalidades Adicionales ---")
        print("1. Ordenar cartas")
        print("2. Mostrar estadísticas")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                ordenar_cartas(cartas)
            case "2":
                mostrar_estadisticas(cartas)
            case "3":
                break
            case _:
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
        #Se ordena con key:lambda para filtrar solo por el atributo
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
    #promedio de daño
    daños = [int(c.get('daño', 0)) for c in cartas]
    daño_total = sum(daños)
    promedio_daño = daño_total / total_cartas if total_cartas > 0 else 0
    print(f"Daño promedio por carta: {promedio_daño:,.2f}")
    #Realizo un contador de calidades
    conteo_por_calidad = {}
    for carta in cartas:
        calidad = carta.get('calidad', 'Desconocida')
        conteo_por_calidad[calidad] = conteo_por_calidad.get(calidad, 0) + 1
    
    print("\nRecuento de cartas por Calidad:")
    for calidad, cantidad in conteo_por_calidad.items():
        print(f"- {calidad}: {cantidad} carta(s)")