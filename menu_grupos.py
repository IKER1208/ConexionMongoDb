from grupo import Grupo
from alumno import Alumno
from maestro import Maestro
from menu_alumnos import MenuAlumnos
from menu_maestros import MenuMaestros
import os
from conexion import conectar_mongo
import json

class MenuGrupos:
    def __init__(self, grupos=None):
        if grupos is None:
            self.grupos = Grupo()
            self.isJson = True
            self.cargar_datos()
        else:
            self.grupos = grupos
            self.isJson = False

    def cargar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            try:
                grupos_data = list(db["Grupos"].find())
                if grupos_data:
                    self.grupos.items = [Grupo(**{k: v for k, v in g.items() if k != '_id'}) for g in grupos_data]
            except Exception as e:
                print(f"Error al cargar grupos de MongoDB: {e}")
        else:
            try:
                if os.path.exists("grupos.json"):
                    with open("grupos.json", "r") as f:
                        data = json.load(f)
                        if data:
                            self.grupos.items = [Grupo(**g) for g in data]
            except Exception as e:
                print(f"Error al cargar grupos de JSON: {e}")

    def guardar_datos(self):
        client = conectar_mongo()
        if client:
            db = client["escuela"]
            try:
                db["Grupos"].delete_many({})
                db["Grupos"].insert_many([g.to_dict() for g in self.grupos.items])
                print("Datos guardados en MongoDB.")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
        else:
            try:
                with open("grupos.json", "w") as f:
                    json.dump([g.to_dict() for g in self.grupos.items], f, indent=4)
                print("Datos guardados en JSON.")
            except Exception as e:
                print(f"Error al guardar en JSON: {e}")

    def mostrar_menu(self):
        while True:
            print("\n=== MENU GRUPOS ===")
            print("1. Ver grupos")
            print("2. Nuevo grupo")
            print("3. Cambiar grupo")
            print("4. Borrar grupo")
            print("5. Asignar maestro")
            print("6. Gestionar alumnos")
            print("7. Gestionar profesores")
            print("8. Salir")
            
            opcion = input("Opción: ")
            
            if opcion == "1":
                self.listar_grupos()
            elif opcion == "2":
                self.agregar_grupo()
            elif opcion == "3":
                self.editar_grupo()
            elif opcion == "4":
                self.eliminar_grupo()
            elif opcion == "5":
                self.asignar_maestro_grupo()
            elif opcion == "6":
                self.gestionar_alumno_grupo()
            elif opcion == "7":
                self.gestionar_profesores()
            elif opcion == "8":
                print("Adiós")
                break
            else:
                print("Opción inválida")

    def listar_grupos(self):
        print("\n=== GRUPOS ===")
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            print("No hay grupos")
            return
            
        for i, grupo in enumerate(self.grupos.items):
            print(f"\n{i+1}. {grupo.nombre}")
            if grupo.maestro:
                print(f"   Profesor: {grupo.maestro.nombre} {grupo.maestro.apellido}")
            else:
                print("   Profesor: Sin asignar")
            
            if hasattr(grupo, 'alumnos') and grupo.alumnos and hasattr(grupo.alumnos, 'items') and grupo.alumnos.items:
                print("   Alumnos:")
                for alumno in grupo.alumnos.items:
                    print(f"   - {alumno.nombre} {alumno.apellido}")
            else:
                print("   Sin alumnos")

    def agregar_grupo(self):
        print("\n=== NUEVO GRUPO ===")
        try:
            nombre = input("Nombre: ")
            nuevo_grupo = Grupo(nombre=nombre)
            if not hasattr(self.grupos, 'agregar'):
                self.grupos = Grupo()
            self.grupos.agregar(nuevo_grupo)
            menu_maestros = MenuMaestros()
            menu_maestros.listar_maestros()
            maestro_indice = int(input("Número del profesor: ")) - 1
            maestro = menu_maestros.maestros.items[maestro_indice]
            nuevo_grupo.maestro = maestro
            print(f"Profesor asignado")    
            grupo_creado = self.grupos.items[-1]
            menu_alumnos = MenuAlumnos(alumnos=grupo_creado.alumnos)
            menu_alumnos.mostrar_menu()
            self.alumnos = menu_alumnos.alumnos
            self.guardar_datos()
            print("Grupo creado")
        except Exception as e:
            print(f"Error: {str(e)}")

    def editar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            indice = int(input("Número del grupo: ")) - 1
            grupo = self.grupos.items[indice]
            print("\n=== CAMBIAR GRUPO ===")
            nuevo_nombre = input(f"Nuevo nombre ({grupo.nombre}): ") or grupo.nombre
            grupo.nombre = nuevo_nombre
            self.guardar_datos()
            print("Grupo actualizado")
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def eliminar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            indice = int(input("Número del grupo: ")) - 1
            confirmacion = input(f"¿Borrar grupo {self.grupos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                if not self.grupos.eliminar(indice=indice):
                    print("No se pudo borrar")
                else:
                    print("Grupo borrado")
            self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def asignar_maestro_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            grupo_indice = int(input("Número del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            menu_maestros = MenuMaestros()
            menu_maestros.listar_maestros()
            maestro_indice = int(input("Número del profesor: ")) - 1
            maestro = menu_maestros.maestros.items[maestro_indice]
            grupo.maestro = maestro
            self.guardar_datos()
            print("Profesor asignado")
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def gestionar_alumno_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            grupo_indice = int(input("Número del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            menu_alumnos = MenuAlumnos(alumnos=self.grupos.items[grupo_indice].alumnos)
            menu_alumnos.mostrar_menu()
            self.alumnos = menu_alumnos.alumnos
            self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def gestionar_profesores(self):
        menu_maestros = MenuMaestros()
        menu_maestros.mostrar_menu()
        self.maestros = menu_maestros.maestros
        self.guardar_datos()

if __name__ == "__main__":
    app = MenuGrupos()
    app.mostrar_menu() 