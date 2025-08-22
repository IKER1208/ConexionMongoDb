from arreglo import Arreglo
import os
import json

class Alumno(Arreglo):
    PASSING_GRADE = 70

    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, promedio=None, calificaciones=None):
        if nombre is None and apellido is None and edad is None and matricula is None and promedio is None and calificaciones is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            # Lista de calificaciones (0 a 100)
            self.calificaciones = list(calificaciones) if calificaciones else []
            # Promedio en escala 0 a 100
            self.promedio = promedio
            self.es_arreglo = False
            # Si no se proporcionó promedio pero sí calificaciones, calcularlo
            if self.promedio is None and self.calificaciones:
                self.calcular_promedio()
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
                    item.get('promedio'),
                    item.get('calificaciones', [])
                )
                alumno_arreglo.agregar(alumno)
            return alumno_arreglo
        else:
            return Alumno(
                data['nombre'],
                data['apellido'],
                data['edad'],
                data['matricula'],
                data.get('promedio'),
                data.get('calificaciones', [])
            )

    def to_dict(self):
        if self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        # Asegurar que el promedio esté actualizado
        if self.promedio is None and getattr(self, 'calificaciones', None):
            self.calcular_promedio()
        return {
            'tipo': 'alumno',
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'matricula': self.matricula,
            'calificaciones': getattr(self, 'calificaciones', []),
            'promedio': self.promedio
        }

    def actualizarPromedio(self, promedio):
        self.promedio = promedio

    def agregar_calificacion(self, calificacion):
        if calificacion is None:
            return False
        try:
            valor = float(calificacion)
        except Exception:
            return False
        if valor < 0 or valor > 100:
            return False
        if not hasattr(self, 'calificaciones') or self.calificaciones is None:
            self.calificaciones = []
        self.calificaciones.append(valor)
        self.calcular_promedio()
        return True

    def calcular_promedio(self):
        if not getattr(self, 'calificaciones', None):
            self.promedio = None
            return self.promedio
        self.promedio = round(sum(self.calificaciones) / len(self.calificaciones), 2)
        return self.promedio

    def calificacion_maxima(self):
        return max(self.calificaciones) if getattr(self, 'calificaciones', None) else None

    def calificacion_minima(self):
        return min(self.calificaciones) if getattr(self, 'calificaciones', None) else None

    def esta_aprobado(self, calificacion_minima=None):
        minimo = calificacion_minima if calificacion_minima is not None else Alumno.PASSING_GRADE
        promedio_actual = self.promedio if self.promedio is not None else self.calcular_promedio()
        return promedio_actual is not None and promedio_actual >= minimo

    def __str__(self):
        if self.es_arreglo:
            return Arreglo.__str__(self)
        promedio_txt = self.promedio if self.promedio is not None else 'N/A'
        cantidad_calif = len(getattr(self, 'calificaciones', []))
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Promedio: {promedio_txt}, "
                f"Calificaciones: {cantidad_calif}")
