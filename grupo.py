from alumno import Alumno
from arreglo import Arreglo
from maestro import Maestro
import os
import json

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, seccion=None, maestro=None, alumnos=None, es_objeto=None):
        if nombre is None and maestro is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.grado = grado
            self.seccion = seccion
            if isinstance(maestro, dict):
                self.maestro = Maestro(
                    nombre=maestro.get('nombre'),
                    apellido=maestro.get('apellido'),
                    edad=maestro.get('edad'),
                    matricula=maestro.get('matricula'),
                    especialidad=maestro.get('especialidad'),
                    es_objeto=maestro.get('es_objeto')
                )
            else:
                self.maestro = maestro
            if alumnos is None:
                self.alumnos = Alumno()
            elif isinstance(alumnos, list):
                self.alumnos = Alumno()
                for a in alumnos:
                    if isinstance(a, dict):
                        self.alumnos.agregar(Alumno(
                            nombre=a.get('nombre'),
                            apellido=a.get('apellido'),
                            edad=a.get('edad'),
                            matricula=a.get('matricula'),
                            promedio=a.get('promedio'),
                            sexo=a.get('sexo'),
                            es_objeto=a.get('es_objeto')
                        ))
                    else:
                        self.alumnos.agregar(a)
            else:
                self.alumnos = alumnos
            self.es_arreglo = False
    def to_json(self):
        with open("grupos.json", 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def read_json(self):
        with open("grupos.json", 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        if not data:
            return None
        if isinstance(data, list):
            grupo_arreglo = Grupo()
            for item in data:
                grupo = Grupo(
                    nombre=item.get('nombre'),
                    grado=item.get('grado'),
                    seccion=item.get('seccion'),
                    maestro=item.get('maestro'),
                    alumnos=item.get('alumnos'),
                    es_objeto=item.get('es_objeto')
                )
                grupo_arreglo.agregar(grupo)
            return grupo_arreglo
        else:
            return Grupo(
                nombre=data.get('nombre'),
                grado=data.get('grado'),
                seccion=data.get('seccion'),
                maestro=data.get('maestro'),
                alumnos=data.get('alumnos'),
                es_objeto=data.get('es_objeto')
            )

    def to_dict(self):
        if self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'nombre': self.nombre,
            'grado': self.grado,
            'seccion': self.seccion,
            'maestro': self.maestro.to_dict() if self.maestro else None,
            'alumnos': self.alumnos.to_dict() if self.alumnos else [],
            'es_objeto': self.es_arreglo if hasattr(self, 'es_arreglo') else False
        }

    def asignar_maestro(self, maestro):
        self.maestro = maestro

    def cambiarNombre(self, nombre):
        self.nombre = nombre

    def __str__(self):
        if self.es_arreglo:
            return f"Total de grupos: {len(self.items)}"
        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido}" if self.maestro else "Falta asignar"
        return (
            f"Grupo: {self.nombre}\n"
            f"Grado: {self.grado}\n"
            f"Sección: {self.seccion}\n"
            f"Maestro: {maestro_info}\n"
            f"Total de alumnos: {str(self.alumnos)}\n"
        )




if __name__ == "__main__":
    from InterfazGrupo import InterfazGrupo

    grupos = Grupo()
    maestro = Maestro("Renata", "Silva", 37, "M010", "Arte")
    alumno = Alumno("Javier", "Mendoza", 15, "888777666", "M")
    grupo_individual = Grupo("Astronomía", "2do", "B", maestro, [alumno])
    grupos.agregar(grupo_individual)

    interfaz = InterfazGrupo(grupos)
    interfaz.menu()