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
        try:
            client = conectar_mongo()
            if client:
                if os.path.exists("alumnos.json"):
                    data = self.alumnos.read_json()
                    if data:
                        self.alumnos = data
                else:
                    db = client["escuela"]
                    try:
                        alumnos_data = list(db["Alumnos"].find())
                        if alumnos_data:
                            self.alumnos.items = [Alumno(**{k: v for k, v in a.items() if k != '_id'}) for a in alumnos_data]
                            self.alumnos.to_json()
                    except Exception as e:
                        print(f"Error al cargar alumnos de MongoDB: {e}")
            else:
                if os.path.exists("alumnos_offline.json"):
                    data = self.alumnos.read_json("alumnos_offline.json")
                    if data:
                        self.alumnos = data
                elif os.path.exists("alumnos.json"):
                    data = self.alumnos.read_json()
                    if data:
                        self.alumnos = data
        except Exception as e:
            print(f"Error al cargar alumnos: {e}")

    def guardar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            self.sincronizar_offline(db)
            try:
                db["Alumnos"].delete_many({})
                db["Alumnos"].insert_many([a.to_dict() for a in self.alumnos.items])
                self.alumnos.to_json()
                print("Datos guardados en alumnos.json y MongoDB.")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
        else:
            try:
                self.alumnos.to_json("alumnos_offline.json")
                print("Datos guardados en alumnos_offline.json (modo offline).")
            except Exception as e:
                print(f"Error al guardar en JSON offline: {e}")

    def sincronizar_offline(self, db):
        if os.path.exists("alumnos_offline.json"):
            try:
                offline_data = self.alumnos.read_json("alumnos_offline.json")
                if offline_data:
                    for alumno in offline_data:
                        if not db["Alumnos"].find_one({"matricula": alumno.get("matricula")}):
                            db["Alumnos"].insert_one(alumno)
                    print("Datos offline sincronizados con MongoDB.")
                os.remove("alumnos_offline.json")
            except Exception as e:
                print(f"Error al sincronizar datos offline: {e}")

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1. Listar alumnos")
            print("2. Agregar alumno")
            print("3. Editar alumno")
            print("4. Eliminar alumno")
            print("5. Estadisticas de calificaciones")
            print("6. Salir")
            
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
                self.estadisticas_calificaciones()
            elif opcion == "6":
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
            print(f"{i+1}. {alumno.nombre} {alumno.apellido} - {alumno.matricula} - {alumno.calificacion}")

    def agregar_alumno(self):
        print("\n--- AGREGAR ALUMNO ---")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            calificacion = float(input("Calificacion (0-100): "))
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                calificacion=calificacion
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
            calificacion = input(f"Calificacion ({alumno.calificacion}): ")
            calificacion = float(calificacion) if calificacion else alumno.calificacion
            alumno.nombre = nombre
            alumno.apellido = apellido
            alumno.edad = edad
            alumno.matricula = matricula
            alumno.calificacion = calificacion
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

    def estadisticas_calificaciones(self):
        print("\n--- ESTADÍSTICAS DE CALIFICACIONES ---")
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            print("No hay alumnos registrados.")
            return
        calificaciones = [a.calificacion for a in self.alumnos.items]
        prom = sum(calificaciones) / len(calificaciones)
        print(f"Promedio de calificaciones: {prom}")
        print(f"Alumnos debajo del promedio: {sum(1 for c in calificaciones if c < prom)}")
        print(f"Alumnos arriba del promedio: {sum(1 for c in calificaciones if c > prom)}")
        print(f"Alumnos aprobados: {sum(1 for c in calificaciones if c >= 70)}")
        print(f"Alumnos reprobados: {sum(1 for c in calificaciones if c < 70)}")
 

if __name__ == "__main__":
    app = MenuAlumnos()
    app.mostrar_menu() 