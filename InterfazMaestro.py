from maestro import Maestro
from conexion import conectar_mongo
import json
import os

class InterfazMaestro:
    def __init__(self, maestros=None, archivo='maestros.json'):
        self.archivo = archivo
        self.guardar = False

        if maestros is not None and len(maestros.items) > 0:
            self.maestros = maestros
            print("Usando clase maestros.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando maestros desde archivo '{archivo}'.")
            self.maestros = Maestro()
            self.maestros.cargarArchivo(archivo, Maestro)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.maestros = Maestro()

        self.sincronizar_maestros_locales()

    def menu(self):
        while True:
            print("\n--- Menú de Maestros ---")
            print("1. Mostrar maestros")
            print("2. Agregar maestros")
            print("3. Eliminar maestros")
            print("4. Actualizar maestros")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(json.dumps(self.maestros.convertir_diccionario(), indent=4, ensure_ascii=False))
            elif opcion == "2":
                self.agregar()
            elif opcion == "3":
                self.eliminar()
            elif opcion == "4":
                self.actualizar()
            elif opcion == "5":
                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                    print("Cambios guardados en archivo.")
                print("Saliendo del sistema.")
                break
            else:
                print("Opción no válida.")

    def agregar(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = int(input("Edad: "))
        matricula = input("Matrícula: ")
        especialidad = input("Especialidad: ")
        nuevo_maestro = Maestro(nombre, apellido, edad, matricula, especialidad)

        self.maestros.agregar(nuevo_maestro)
        maestro_dict = nuevo_maestro.__dict__

        client = conectar_mongo()
        if client:
            db = client["escuela"]
            coleccion = db["Maestros"]
            coleccion.insert_one(maestro_dict)
            print("Maestro guardado en MongoDB.")
        else:
            archivo_temp = "maestros_no_sincronizados.json"
            datos = []
            if os.path.exists(archivo_temp):
                with open(archivo_temp, "r") as f:
                    datos = json.load(f)
            datos.append(maestro_dict)
            with open(archivo_temp, "w") as f:
                json.dump(datos, f, indent=4)
            print("No hay conexión. Maestro guardado localmente en espera de sincronización.")

        if self.guardar:
            self.maestros.guardarArchivo(self.archivo)

    def eliminar(self):
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            print("No hay maestros")
            return
        maestros_ordenados = sorted(self.maestros.items, key=lambda m: m.nombre)
        print("\n--- Lista de Maestros ---")
        for idx, maestro in enumerate(maestros_ordenados, 1):
            print(f"{idx}. {maestro.nombre} {maestro.apellido} (Matrícula: {maestro.matricula})")
        try:
            indice = int(input("Número del maestro a eliminar: ")) - 1
            if 0 <= indice < len(maestros_ordenados):
                maestro_a_eliminar = maestros_ordenados[indice]
                idx_real = self.maestros.items.index(maestro_a_eliminar)
                if self.maestros.eliminar(indice=idx_real):
                    if self.guardar:
                        self.maestros.guardarArchivo(self.archivo)
                    print("Maestro eliminado correctamente.")
                else:
                    print("No se pudo eliminar.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Índice inválido.")

    def actualizar(self):
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            print("No hay maestros")
            return
        maestros_ordenados = sorted(self.maestros.items, key=lambda m: m.nombre)
        print("\n--- Lista de Maestros ---")
        for idx, maestro in enumerate(maestros_ordenados, 1):
            print(f"{idx}. {maestro.nombre} {maestro.apellido} (Matrícula: {maestro.matricula})")
        try:
            indice = int(input("Número del maestro a actualizar: ")) - 1
            if 0 <= indice < len(maestros_ordenados):
                maestro = maestros_ordenados[indice]
                print("Deja en blanco si no quieres cambiar un campo.")

                nombre = input(f"Nombre ({maestro.nombre}): ") or maestro.nombre
                apellido = input(f"Apellido ({maestro.apellido}): ") or maestro.apellido
                edad_input = input(f"Edad ({maestro.edad}): ")
                edad = int(edad_input) if edad_input else maestro.edad
                matricula = input(f"Matrícula ({maestro.matricula}): ") or maestro.matricula
                especialidad = input(f"Especialidad ({maestro.especialidad}): ") or maestro.especialidad

                self.maestros.actualizar(
                    maestro,
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad,
                    matricula=matricula,
                    especialidad=especialidad
                )

                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                print("Maestro actualizado correctamente.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def sincronizar_maestros_locales(self):
        archivo_temp = "maestros_no_sincronizados.json"
        if not os.path.exists(archivo_temp):
            return

        client = conectar_mongo()
        if client:
            with open(archivo_temp, "r") as f:
                datos = json.load(f)

            if datos:
                db = client["escuela"]
                coleccion = db["Maestros"]
                coleccion.insert_many(datos)
                print(f"Se sincronizaron {len(datos)} maestros con MongoDB.")
                os.remove(archivo_temp)
        else:
            print("Aún no hay conexión a MongoDB. No se puede sincronizar.")

if __name__ == "__main__":
    interfaz = InterfazMaestro()
    interfaz.menu()
