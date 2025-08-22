from arreglo import Arreglo
import os
import json

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, promedio=None):
        if nombre is None and apellido is None and edad is None and matricula is None and promedio is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.promedio = promedio
            self.es_arreglo = False
    def to_json(self):
        with open("alumnos.json", 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def read_json(self):
        with open("alumnos.json", 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        if not data:
            return None
        if isinstance(data, list):
            alumno_arreglo = Alumno()
            for item in data:
                alumno = Alumno(
                    item['nombre'],
                    item['apellido'],
                    item['edad'],
                    item['matricula'],
                    item['promedio']
                )
                alumno_arreglo.agregar(alumno)
            return alumno_arreglo
        else:
            return Alumno(
                data['nombre'],
                data['apellido'],
                data['edad'],
                data['matricula'],
                data['promedio']
            )

    def to_dict(self):
        if self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'tipo': 'alumno','nombre': self.nombre,'apellido': self.apellido,'edad': self.edad,'matricula': self.matricula,'promedio': self.promedio
        }

    def actualizarPromedio(self, promedio):
        self.promedio = promedio

    def __str__(self):
        if self.es_arreglo:
            return Arreglo.__str__(self)
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Promedio: {self.promedio}")
