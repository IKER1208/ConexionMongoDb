from alumno import Alumno
from arreglo import Arreglo
from maestro import Maestro
import os
import json

class Grupo(Arreglo):
    def __init__(self, nombre=None, maestro=None):
        if nombre is None and maestro is None: 
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.maestro = maestro
            self.alumnos = Alumno()
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
                grupo = grupo_arreglo._dict_to_object(item)                
                grupo_arreglo.agregar(grupo)
            return grupo_arreglo
        else:
            maestro_data = data.get('maestro')
            maestro = None
            if maestro_data:
                maestro = Maestro(
                    maestro_data['nombre'],
                    maestro_data['apellido'],
                    maestro_data['edad'],
                    maestro_data['matricula'],
                    maestro_data['especialidad']
                )
            
            grupo = Grupo(data['nombre'], maestro)
            
            alumnos_data = data.get('alumnos', [])
            if alumnos_data:
                alumnos = Alumno()
                alumnos._dict_to_object(alumnos_data)
            if len(alumnos_data)>0:
                alumnos=Alumno()
                alumnos=alumnos._dict_to_object(alumnos_data)
                grupo.alumnos=alumnos
                grupo.alumnos = alumnos
            
            return grupo

    def to_dict(self):
        if self.es_arreglo:
                return  [item.to_dict() for item in self.items] if self.items else []
        return {
            'tipo': 'grupo','nombre': self.nombre,
            'maestro': self.maestro.to_dict()if self.maestro 
              else None,'alumnos': self.alumnos.to_dict()
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