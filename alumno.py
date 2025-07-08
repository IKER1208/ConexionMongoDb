from arreglo import Arreglo
import os
import json

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, promedio=None, sexo=None, es_objeto=None):
        if nombre is None and apellido is None and edad is None and matricula is None and promedio is None and sexo is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.promedio = promedio
            self.sexo = sexo
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
                    nombre=item.get('nombre'),
                    apellido=item.get('apellido'),
                    edad=item.get('edad'),
                    matricula=item.get('matricula'),
                    promedio=item.get('promedio'),
                    sexo=item.get('sexo'),
                    es_objeto=item.get('es_objeto')
                )
                alumno_arreglo.agregar(alumno)
            return alumno_arreglo
        else:
            return Alumno(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                edad=data.get('edad'),
                matricula=data.get('matricula'),
                promedio=data.get('promedio'),
                sexo=data.get('sexo'),
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
            'promedio': self.promedio,
            'sexo': self.sexo,
            'es_objeto': self.es_arreglo if hasattr(self, 'es_arreglo') else False
        }

    def actualizarPromedio(self, promedio):
        self.promedio = promedio

    def __str__(self):
        if self.es_arreglo:
            return Arreglo.__str__(self)
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Promedio: {self.promedio}, Sexo: {self.sexo}")
