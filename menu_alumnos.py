from alumno import Alumno
import os
from conexion import conectar_mongo
import json

class MenuAlumnos:
    def __init__(self, alumnos=None):
        if alumnos is None:
            self.alumnos = Alumno()
            self.isJson = True
            self.cargar_datos()
        else:
            self.alumnos = alumnos
            self.isJson = False

    def cargar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            try:
                alumnos_data = list(db["Alumnos"].find())
                if alumnos_data:
                    self.alumnos.items = [Alumno(**{k: v for k, v in a.items() if k != '_id'}) for a in alumnos_data]
            except Exception as e:
                print(f"Error al cargar alumnos de MongoDB: {e}")
        else:
            try:
                if os.path.exists("alumnos.json"):
                    with open("alumnos.json", "r") as f:
                        data = json.load(f)
                        if data:
                            self.alumnos.items = [Alumno(**a) for a in data]
            except Exception as e:
                print(f"Error al cargar alumnos de JSON: {e}")

    def guardar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            try:
                db["Alumnos"].delete_many({})
                db["Alumnos"].insert_many([a.to_dict() for a in self.alumnos.items])
                print("Datos guardados en MongoDB.")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
        else:
            try:
                with open("alumnos.json", "w") as f:
                    json.dump([a.to_dict() for a in self.alumnos.items], f, indent=4)
                print("Datos guardados en JSON.")
            except Exception as e:
                print(f"Error al guardar en JSON: {e}")

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1. Listar alumnos")
            print("2. Agregar alumno")
            print("3. Editar alumno")
            print("4. Eliminar alumno")
            print("5. Gestionar calificaciones de un alumno")
            print("6. Estadísticas del grupo")
            print("7. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.editar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":
                self.menu_calificaciones()
            elif opcion == "6":
                self.estadisticas_grupo()
            elif opcion == "7":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def listar_alumnos(self):
        print("\n--- LISTA DE ALUMNOS ---")
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            print("No hay alumnos registrados.")
            return
            
        for i, alumno in enumerate(self.alumnos.items):
            promedio_txt = alumno.promedio if getattr(alumno, 'promedio', None) is not None else 'N/A'
            print(f"{i+1}. {alumno.nombre} {alumno.apellido} - {alumno.matricula} - Promedio: {promedio_txt}")

    def agregar_alumno(self):
        print("\n--- AGREGAR ALUMNO ---")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                promedio=None,
                calificaciones=[]
            )
            if not hasattr(self.alumnos, 'agregar'):
                self.alumnos = Alumno()
            self.alumnos.agregar(nuevo_alumno)
            print("Alumno agregado correctamente.")
            self.guardar_datos()
        except ValueError as e:
            print(f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            print(f"Error al agregar alumno: {str(e)}")

    def editar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
        try:
            indice = int(input("Seleccione el número del alumno a editar: ")) - 1
            alumno = self.alumnos.items[indice]
            print("\n--- EDITAR ALUMNO ---")
            print("Deje en blanco los campos que no desea modificar")
            nombre = input(f"Nombre ({alumno.nombre}): ") or alumno.nombre
            apellido = input(f"Apellido ({alumno.apellido}): ") or alumno.apellido
            edad = input(f"Edad ({alumno.edad}): ")
            edad = int(edad) if edad else alumno.edad
            matricula = input(f"Matrícula ({alumno.matricula}): ") or alumno.matricula
            promedio = input(f"Promedio ({alumno.promedio}): ")
            promedio = float(promedio) if promedio else alumno.promedio
            alumno.nombre = nombre
            alumno.apellido = apellido
            alumno.edad = edad
            alumno.matricula = matricula
            alumno.promedio = promedio
            print("Alumno actualizado correctamente.")
            self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def eliminar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
        try:
            indice = int(input("Seleccione el número del alumno a eliminar: ")) - 1
            confirmacion = input(f"¿Está seguro de eliminar a {self.alumnos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                if not self.alumnos.eliminar(indice=indice):
                    print("No se pudo eliminar el alumno.")
                else:
                    print("Alumno eliminado correctamente.")
                    self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def _seleccionar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return None, None
        try:
            indice = int(input("Seleccione el número del alumno: ")) - 1
            return self.alumnos.items[indice], indice
        except (IndexError, ValueError):
            print("Selección no válida.")
            return None, None

    def menu_calificaciones(self):
        alumno, _ = self._seleccionar_alumno()
        if alumno is None:
            return
        while True:
            print(f"\n--- CALIFICACIONES: {alumno.nombre} {alumno.apellido} ---")
            print("1. Listar calificaciones")
            print("2. Agregar calificación (0-100)")
            print("3. Ver promedio, máxima y mínima")
            print("4. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                califs = getattr(alumno, 'calificaciones', [])
                if not califs:
                    print("Sin calificaciones registradas.")
                else:
                    print(f"Calificaciones: {califs}")
            elif opcion == '2':
                try:
                    valor = float(input("Ingrese calificación (0-100): "))
                    if alumno.agregar_calificacion(valor):
                        print("Calificación agregada y promedio actualizado.")
                        self.guardar_datos()
                    else:
                        print("Valor inválido. Debe estar entre 0 y 100.")
                except ValueError:
                    print("Entrada inválida.")
            elif opcion == '3':
                print(f"Promedio: {alumno.promedio if alumno.promedio is not None else 'N/A'}")
                print(f"Máxima: {alumno.calificacion_maxima()}")
                print(f"Mínima: {alumno.calificacion_minima()}")
            elif opcion == '4':
                break
            else:
                print("Opción no válida.")

    def estadisticas_grupo(self):
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            print("No hay alumnos para calcular estadísticas.")
            return
        alumnos_validos = [a for a in self.alumnos.items if getattr(a, 'promedio', None) is not None or getattr(a, 'calificaciones', None)]
        # Asegurar promedios calculados
        for a in alumnos_validos:
            if a.promedio is None:
                a.calcular_promedio()
        promedios = [a.promedio for a in alumnos_validos if a.promedio is not None]
        if not promedios:
            print("No hay promedios calculados todavía.")
            return
        promedio_grupo = round(sum(promedios) / len(promedios), 2)
        aprobaron = sum(1 for a in alumnos_validos if a.esta_aprobado(70))
        reprobaron = sum(1 for a in alumnos_validos if a.promedio is not None and a.promedio < 70)
        abajo = sum(1 for a in alumnos_validos if a.promedio is not None and a.promedio < promedio_grupo)
        arriba = sum(1 for a in alumnos_validos if a.promedio is not None and a.promedio > promedio_grupo)
        print("\n--- ESTADÍSTICAS DEL GRUPO ---")
        print(f"Promedio del grupo: {promedio_grupo}")
        print(f"Alumnos que aprobaron (>=70): {aprobaron}")
        print(f"Alumnos que reprobaron (<70): {reprobaron}")
        print(f"Alumnos por debajo del promedio del grupo: {abajo}")
        print(f"Alumnos por arriba del promedio del grupo: {arriba}")

if __name__ == "__main__":
    alumno1 = Alumno(nombre="Juan", apellido="Pérez", edad=22, matricula="222222222", promedio=9.5)
    alumno2 = Alumno(nombre="Jose", apellido="García", edad=21, matricula="1222222222", promedio=8.7)
    alumnos = Alumno()
    alumnos.agregar(alumno1)
    alumnos.agregar(alumno2)
    app = MenuAlumnos(alumnos=alumnos)
    app.mostrar_menu() 