import json
from alumno import Alumno
from maestro import Maestro
from grupo import Grupo
from arreglo import Arreglo
from menu_grupos import MenuGrupos
from menu_alumnos import MenuAlumnos
from menu_maestros import MenuMaestros

if __name__ == "__main__":
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Gestión de Grupos")
        print("2. Gestión de Alumnos")
        print("3. Gestión de Maestros")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            MenuGrupos().mostrar_menu()
        elif opcion == "2":
            MenuAlumnos().mostrar_menu()
        elif opcion == "3":
            MenuMaestros().mostrar_menu()
        elif opcion == "4":
            print("Adiós!")
            break
        else:
            print("Opción inválida.") 