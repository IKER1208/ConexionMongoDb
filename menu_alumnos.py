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
        if os.path.exists("alumnos_offline.json"):
            try:
                with open("alumnos_offline.json", "r") as f:
                    data = json.load(f)
                if data:
                    self.alumnos.items = [Alumno(**a) for a in data]
                print("Datos cargados de alumnos_offline.json (modo offline).")
            except Exception as e:
                print(f"Error al cargar alumnos_offline.json: {e}")
        elif os.path.exists("alumnos.json"):
            try:
                with open("alumnos.json", "r") as f:
                    data = json.load(f)
                if data:
                    self.alumnos.items = [Alumno(**a) for a in data]
                print("Datos cargados de alumnos.json.")
            except Exception as e:
                print(f"Error al cargar alumnos.json: {e}")
        elif client:
            db = client["escuela"]
            self.sincronizar_offline(db)
            try:
                alumnos_data = list(db["Alumnos"].find())
                if alumnos_data:
                    self.alumnos.items = [Alumno(**{k: v for k, v in a.items() if k != '_id'}) for a in alumnos_data]
                print("Datos cargados de MongoDB.")
            except Exception as e:
                print(f"Error al cargar alumnos de MongoDB: {e}")
        else:
            print("No se encontraron datos de alumnos.")

    def guardar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            # Sincronizar datos offline si existen
            self.sincronizar_offline(db)
            try:
                db["Alumnos"].delete_many({})
                db["Alumnos"].insert_many([a.to_dict() for a in self.alumnos.items])
                print("Datos guardados en MongoDB.")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
        else:
            try:
                with open("alumnos_offline.json", "w") as f:
                    json.dump([a.to_dict() for a in self.alumnos.items], f, indent=4)
                print("Datos guardados en alumnos_offline.json (modo offline).")
            except Exception as e:
                print(f"Error al guardar en JSON offline: {e}")

    def sincronizar_offline(self, db):
        if os.path.exists("alumnos_offline.json"):
            try:
                with open("alumnos_offline.json", "r") as f:
                    offline_data = json.load(f)
                if offline_data:
                    db["Alumnos"].delete_many({})
                    db["Alumnos"].insert_many(offline_data)
                    print("Datos offline de alumnos sincronizados con MongoDB.")
                os.remove("alumnos_offline.json")
            except Exception as e:
                print(f"Error al sincronizar datos offline de alumnos: {e}")

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1. Listar alumnos")
            print("2. Agregar alumno")
            print("3. Editar alumno")
            print("4. Eliminar alumno")
            print("5. Salir")
            
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
            print(f"{i+1}. {alumno.nombre} {alumno.apellido} - {alumno.matricula}")

    def agregar_alumno(self):
        print("\n--- AGREGAR ALUMNO ---")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            promedio = float(input("Promedio (0-10): "))
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                promedio=promedio
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

if __name__ == "__main__":
    alumno1 = Alumno(nombre="Juan", apellido="Pérez", edad=22, matricula="222222222", promedio=9.5)
    alumno2 = Alumno(nombre="Jose", apellido="García", edad=21, matricula="1222222222", promedio=8.7)
    alumnos = Alumno()
    alumnos.agregar(alumno1)
    alumnos.agregar(alumno2)
    app = MenuAlumnos(alumnos=alumnos)
    app.mostrar_menu() 