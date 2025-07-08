from arreglo import Arreglo
import os
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None, es_objeto=None):
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.especialidad = especialidad
            self.es_arreglo = False
    def to_json(self):
        with open("maestros.json", 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def read_json(self):
        with open("maestros.json", 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        if not data:
            return None
        if isinstance(data, list):
            maestro_arreglo = Maestro()
            for item in data:
                maestro = Maestro(
                    nombre=item.get('nombre'),
                    apellido=item.get('apellido'),
                    edad=item.get('edad'),
                    matricula=item.get('matricula'),
                    especialidad=item.get('especialidad'),
                    es_objeto=item.get('es_objeto')
                )
                maestro_arreglo.agregar(maestro)
            return maestro_arreglo
        else:
            return Maestro(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                edad=data.get('edad'),
                matricula=data.get('matricula'),
                especialidad=data.get('especialidad'),
                es_objeto=data.get('es_objeto')
            )

    def to_dict(self):
        if self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'matricula': self.matricula,
            'especialidad': self.especialidad,
            'es_objeto': self.es_arreglo if hasattr(self, 'es_arreglo') else False
        }

    def __str__(self):
        if self.es_arreglo:
            return Arreglo.__str__(self)
        return (f"Maestro: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matricula: {self.matricula}, Especialidad: {self.especialidad}")

    def cambiarEspecialidad(self, especialidad):
        self.especialidad = especialidad


if __name__ == "__main__":
    from InterfazMaestro import InterfazMaestro

    interfaz = InterfazMaestro()
    interfaz.menu()
