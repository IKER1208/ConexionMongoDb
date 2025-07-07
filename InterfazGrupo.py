from grupo import Grupo
from InterfazMaestro import InterfazMaestro
from InterfazAlumno import InterfazAlumno
from conexion import conectar_mongo
import json
import os

from maestro import Maestro

class InterfazGrupo:
    def __init__(self, grupos=None, archivo="grupos.json"):
        self.archivo = archivo
        self.guardar = False

        if grupos is not None and len(grupos.items) > 0:
            self.grupos = grupos
            print("Usando clase Grupo.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando grupos desde archivo '{archivo}'.")
            self.grupos = Grupo()
            self.grupos.cargarArchivo(archivo, Grupo)

            self.grupos_offline = Grupo()
            self.grupos_offline.cargarArchivo(archivo="grupos_offline.json",clase_objeto= Grupo)

            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.grupos = Grupo()

        self.interfaz_maestro = InterfazMaestro()
        self.interfaz_alumno = InterfazAlumno()
        self.sincronizar_grupos_locales()

    def menu(self):
        while True:
            print("\n--- Menú de Grupos ---")
            print("1. Mostrar grupos")
            print("2. Agregar grupo")
            print("3. Eliminar grupo")
            print("4. Actualizar grupo")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.mostrar_grupos()
            elif opcion == "2":
                self.agregar_grupo()
            elif opcion == "3":
                self.eliminar_grupo()
            elif opcion == "4":
                self.actualizar_grupo()
            elif opcion == "5":
                print("Saliendo.")
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                break
            else:
                print("Opción no válida.")

    def mostrar_grupos(self):
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            print("No hay grupos")
            return
        grupos_ordenados = sorted(self.grupos.items, key=lambda g: g.nombre)
        print("\n--- Lista de Grupos ---")
        for idx, grupo in enumerate(grupos_ordenados, 1):
            print(f"{idx}. {grupo.nombre} (Grado: {getattr(grupo, 'grado', '-')}, Sección: {getattr(grupo, 'seccion', '-')})")
            if hasattr(grupo, 'maestro') and grupo.maestro:
                print(f"   Maestro: {grupo.maestro.nombre} {grupo.maestro.apellido}")
            else:
                print("   Maestro: Sin asignar")
            if hasattr(grupo, 'alumnos') and grupo.alumnos and hasattr(grupo.alumnos, 'items') and grupo.alumnos.items:
                print("   Alumnos:")
                for alumno in grupo.alumnos.items:
                    print(f"      - {alumno.nombre} {alumno.apellido}")
            else:
                print("   Sin alumnos")

    def agregar_grupo(self):
        nombre = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")

        print("\n--- Creando un nuevo maestro ---")
        self.interfaz_maestro.agregar()
        if len(self.interfaz_maestro.maestros.items) > 0:
            maestro = self.interfaz_maestro.maestros.items[-1]
        else:
            print("No se pudo crear el maestro.")
            return

        grupo = Grupo(nombre, grado, seccion, maestro)

        agregar_mas = input("¿Deseas agregar alumnos? (s/n): ").lower()
        if agregar_mas == "s":
            print("\n--- Gestionando alumnos para el grupo ---")
            temp_alumnos = grupo.alumnos

            interfaz_alumno = InterfazAlumno(temp_alumnos)
            interfaz_alumno.menu()

            grupo.alumnos = interfaz_alumno.alumnos

       

        client = conectar_mongo()
        if client:
            db = client["escuela"]
            coleccion = db["Grupos"]
            grupo_dict = grupo.convertir_dict_mongo() if hasattr(grupo, "convertir_dict_mongo") else grupo.__dict__

            # Convierte maestro y alumnos a dict si existen
            if "maestro" in grupo_dict and hasattr(grupo_dict["maestro"], "__dict__"):
                grupo_dict["maestro"] = grupo_dict["maestro"].__dict__
            if "alumnos" in grupo_dict and hasattr(grupo_dict["alumnos"], "items"):
                grupo_dict["alumnos"] = [alumno.__dict__ for alumno in grupo_dict["alumnos"].items]

            coleccion.insert_one(grupo_dict)
            print("✅ Grupo guardado en MongoDB.")
        else:
            self.grupos_offline.agregar(grupo)
            self.grupos_offline.guardarArchivo(self.archivo_offline)

        self.grupos.agregar(grupo)

        if self.guardar:
            self.grupos.guardarArchivo(self.archivo)
            print("Grupo agregado y guardado en archivo.")
        else:
            print("Grupo agregado (modo objeto).")

    def eliminar_grupo(self):
        self.mostrar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            grupos_ordenados = sorted(self.grupos.items, key=lambda g: g.nombre)
            indice = int(input("Número del grupo a eliminar: ")) - 1
            if 0 <= indice < len(grupos_ordenados):
                grupo_a_eliminar = grupos_ordenados[indice]
                confirmacion = input(f"¿Borrar grupo {grupo_a_eliminar.nombre}? (s/n): ")
                if confirmacion.lower() == 's':
                    # Buscar el índice real en self.grupos.items
                    idx_real = self.grupos.items.index(grupo_a_eliminar)
                    if self.grupos.eliminar(indice=idx_real):
                        if self.guardar:
                            self.grupos.guardarArchivo(self.archivo)
                        print("Grupo eliminado.")
                    else:
                        print("No se pudo eliminar el grupo.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Índice inválido.")

    def actualizar_grupo(self):
        self.mostrar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            grupos_ordenados = sorted(self.grupos.items, key=lambda g: g.nombre)
            indice = int(input("Número del grupo a actualizar: ")) - 1
            if 0 <= indice < len(grupos_ordenados):
                grupo = grupos_ordenados[indice]
                print("Deja en blanco si no deseas cambiar un campo.")

                nombre = input(f"Nombre ({grupo.nombre}): ") or grupo.nombre
                grado = input(f"Grado ({grupo.grado}): ") or grupo.grado
                seccion = input(f"Sección ({grupo.seccion}): ") or grupo.seccion

                grupo.nombre = nombre
                grupo.grado = grado
                grupo.seccion = seccion

                actualizar_maestro = input("¿Deseas actualizar al maestro? (s/n): ").lower()
                if actualizar_maestro == "s":
                    print("\n--- Actualizando maestro ---")
                    temp_maestros = Maestro()
                    temp_maestros.agregar(grupo.maestro)
                    self.interfaz_maestro.maestros = temp_maestros
                    self.interfaz_maestro.menu()
                    if len(self.interfaz_maestro.maestros.items) > 0:
                        grupo.maestro = self.interfaz_maestro.maestros.items[0]
                    else:
                        print("No se pudo actualizar el maestro, manteniendo el original.")

                actualizar_alumnos = input("¿Deseas gestionar los alumnos del grupo? (s/n): ").lower()
                if actualizar_alumnos == "s":
                    print("\n--- Gestionando alumnos del grupo ---")
                    temp_alumnos = grupo.alumnos
                    self.interfaz_alumno.alumnos = temp_alumnos
                    self.interfaz_alumno.menu()
                    grupo.alumnos = self.interfaz_alumno.alumnos

                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def sincronizar_grupos_locales(self):
        archivo_temp = "grupos_no_sincronizados.json"
        if not os.path.exists(archivo_temp):
            return

        client = conectar_mongo()
        if client:
            with open(archivo_temp, "r") as f:
                datos = json.load(f)

            if datos:
                db = client["escuela"]
                coleccion = db["Grupos"]
                coleccion.insert_many(datos)
                print(f"✅ Se sincronizaron {len(datos)} grupos con MongoDB.")
                os.remove(archivo_temp)
        else:
            print("❌ Aún no hay conexión a MongoDB. No se puede sincronizar.")

if __name__ == "__main__":
    interfaz = InterfazGrupo()
    interfaz.menu()
