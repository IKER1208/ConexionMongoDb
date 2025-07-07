from arreglo import Arreglo
import json
from conexion import conectar_mongo
db = conectar_mongo()

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, sexo=None):
        if nombre is None and apellido is None and edad is None and matricula is None and sexo is None:
            super().__init__()
            self.es_objeto = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.sexo = sexo
            self.es_objeto = False

    def __str__(self):
        if self.es_objeto:
            return f"Total de alumnos: {super().__str__()}"
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, sexo: {self.sexo}, "
                f"Matrícula: {self.matricula}")

    def convertir_diccionario(self):
        if self.es_objeto:
            return super().convertir_diccionario()
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "matricula": self.matricula,
            "sexo": self.sexo
        }
    
    def guardar_mongo(self):
        """Guarda el alumno en MongoDB"""
        if db:
            try:
                db.Alumnos.insert_one(self.convertir_dict_mongo())
                return True
            except:
                return False
        return False

    def mostrar(self):
        print(str(self))

if __name__ == "__main__":
    from InterfazAlumno import InterfazAlumno

    alumnos = Alumno()
    alumnos.agregar(Alumno("Nicolás", "Torres", 19, "555111222", "M"))
    alumnos.agregar(Alumno("Camila", "Ríos", 18, "555333444", "F"))

    interfaz = InterfazAlumno()
    interfaz.menu()
