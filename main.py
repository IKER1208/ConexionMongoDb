import json
from alumno import Alumno
from maestro import Maestro
from grupo import Grupo
from arreglo import Arreglo

if __name__ == "__main__":
    # Alumnos
    alumno1 = Alumno("Lucas", "Gómez", 17, "100100100", 'M')
    alumno2 = Alumno("Valeria", "Santos", 16, "200200200", 'F')
    alumno3 = Alumno("Mateo", "Ramírez", 18, "300300300", 'M')

    alumnos = Arreglo() 
    alumnos.agregar(alumno1, alumno2, alumno3)

    alumnos_diccionario = alumnos.convertir_diccionario()
    alumnos_json = json.dumps(alumnos_diccionario, indent=4, ensure_ascii=False)
    print("Alumnos:")
    print(alumnos_json)

    alumnos.eliminar(alumno2)
    diccionario2 = alumnos.convertir_diccionario()
    diccionario2_json = json.dumps(diccionario2, indent=4, ensure_ascii=False)
    print("Alumnos después de eliminar:")
    print(diccionario2_json)

    # Maestros
    maestro1 = Maestro("Sofía", "Herrera", "29", 40001, "Física")
    maestro2 = Maestro("Emilio", "Vega", "41", 40002, "Historia")

    maestros = Arreglo() 
    maestros.agregar(maestro1, maestro2)

    maestros_diccionario = maestros.convertir_diccionario()
    maestros_json = json.dumps(maestros_diccionario, indent=4, ensure_ascii=False)
    print("Maestros:")
    print(maestros_json)

    maestros.eliminar(maestro2)
    diccionario3 = maestros.convertir_diccionario()
    diccionario3_json = json.dumps(diccionario3, indent=4, ensure_ascii=False)
    print("Maestros después de eliminar:")
    print(diccionario3_json)

    # Grupos
    grupo1 = Grupo("Robótica", "3", "C")
    grupo1.asignarMaestro(maestro1)
    grupo1.alumnos.agregar(alumno1, alumno3)

    grupo2 = Grupo("Literatura", "4", "D")
    grupo2.asignarMaestro(maestro2)
    grupo2.alumnos.agregar(alumno1, alumno2, alumno3)

    grupos = Grupo()
    grupos.agregar(grupo1, grupo2)

    grupos_diccionario = grupos.convertir_diccionario()
    grupos_json = json.dumps(grupos_diccionario, indent=4, ensure_ascii=False)
    print("Grupos:")
    print(grupos_json)

    alumnos.guardarArchivo("alumnos.json")
    maestros.guardarArchivo("maestros.json")
    grupos.guardarArchivo("grupos.json") 