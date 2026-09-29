import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sicenet2.settings')
django.setup()

from catalog.models import Carrera, Materia, Profesor, Grupo

def populate():
    print("Borrando datos anteriores (Carrera, Materia, Profesor, Grupo)...")
    Grupo.objects.all().delete()
    Profesor.objects.all().delete()
    Materia.objects.all().delete()
    Carrera.objects.all().delete()

    print("Creando Carreras...")
    carreras_data = [
        {"codigo": "ISC", "nombre": "Ingeniería en Sistemas Computacionales", "creditos": 260, "duracion": 9},
        {"codigo": "IEL", "nombre": "Ingeniería Electrónica", "creditos": 260, "duracion": 9},
        {"codigo": "IAM", "nombre": "Ingeniería Ambiental", "creditos": 260, "duracion": 9},
        {"codigo": "LGA", "nombre": "Licenciatura en Gastronomía", "creditos": 240, "duracion": 8},
        {"codigo": "IGE", "nombre": "Ingeniería en Gestión Empresarial", "creditos": 260, "duracion": 9},
        {"codigo": "IIN", "nombre": "Ingeniería Industrial", "creditos": 260, "duracion": 9},
        {"codigo": "IAU", "nombre": "Ingeniería Automotriz", "creditos": 260, "duracion": 9},
    ]

    carreras = {}
    for data in carreras_data:
        c = Carrera.objects.create(**data)
        carreras[data["codigo"]] = c

    print("Creando Materias...")
    materias_data = [
        # Sistemas Computacionales
        {"carrera": "ISC", "codigo": "ISC-101", "nombre": "Fundamentos de Programación", "unidades": 5, "creditos": 5},
        {"carrera": "ISC", "codigo": "ISC-102", "nombre": "Estructura de Datos", "unidades": 6, "creditos": 5},
        {"carrera": "ISC", "codigo": "ISC-103", "nombre": "Bases de Datos", "unidades": 5, "creditos": 5},
        {"carrera": "ISC", "codigo": "ISC-104", "nombre": "Redes de Computadoras", "unidades": 6, "creditos": 5},
        # Electrónica
        {"carrera": "IEL", "codigo": "IEL-101", "nombre": "Circuitos Eléctricos", "unidades": 5, "creditos": 5},
        {"carrera": "IEL", "codigo": "IEL-102", "nombre": "Electrónica Analógica", "unidades": 6, "creditos": 5},
        {"carrera": "IEL", "codigo": "IEL-103", "nombre": "Microcontroladores", "unidades": 5, "creditos": 5},
        # Ambiental
        {"carrera": "IAM", "codigo": "IAM-101", "nombre": "Química Orgánica", "unidades": 5, "creditos": 5},
        {"carrera": "IAM", "codigo": "IAM-102", "nombre": "Microbiología Ambiental", "unidades": 4, "creditos": 4},
        {"carrera": "IAM", "codigo": "IAM-103", "nombre": "Termodinámica", "unidades": 5, "creditos": 5},
        # Gastronomía
        {"carrera": "LGA", "codigo": "LGA-101", "nombre": "Bases Culinarias", "unidades": 6, "creditos": 6},
        {"carrera": "LGA", "codigo": "LGA-102", "nombre": "Panadería y Repostería", "unidades": 5, "creditos": 5},
        {"carrera": "LGA", "codigo": "LGA-103", "nombre": "Nutrición", "unidades": 4, "creditos": 4},
        # Gestión Empresarial
        {"carrera": "IGE", "codigo": "IGE-101", "nombre": "Fundamentos de Gestión Empresarial", "unidades": 5, "creditos": 5},
        {"carrera": "IGE", "codigo": "IGE-102", "nombre": "Contabilidad Financiera", "unidades": 5, "creditos": 5},
        {"carrera": "IGE", "codigo": "IGE-103", "nombre": "Comportamiento Organizacional", "unidades": 4, "creditos": 4},
        # Industrial
        {"carrera": "IIN", "codigo": "IIN-101", "nombre": "Dibujo Industrial", "unidades": 4, "creditos": 4},
        {"carrera": "IIN", "codigo": "IIN-102", "nombre": "Estudio del Trabajo", "unidades": 5, "creditos": 5},
        {"carrera": "IIN", "codigo": "IIN-103", "nombre": "Gestión de la Calidad", "unidades": 5, "creditos": 5},
        # Automotriz
        {"carrera": "IAU", "codigo": "IAU-101", "nombre": "Mecánica del Automóvil", "unidades": 6, "creditos": 5},
        {"carrera": "IAU", "codigo": "IAU-102", "nombre": "Dinámica del Vehículo", "unidades": 5, "creditos": 5},
        {"carrera": "IAU", "codigo": "IAU-103", "nombre": "Motores de Combustión Interna", "unidades": 6, "creditos": 6},
        
        # Tronco Común (Asignadas a múltiples carreras para simular)
        {"carrera": "ISC", "codigo": "MAT-101-ISC", "nombre": "Cálculo Diferencial", "unidades": 5, "creditos": 5},
        {"carrera": "IEL", "codigo": "MAT-101-IEL", "nombre": "Cálculo Diferencial", "unidades": 5, "creditos": 5},
        {"carrera": "IIN", "codigo": "MAT-101-IIN", "nombre": "Cálculo Diferencial", "unidades": 5, "creditos": 5},
        
        {"carrera": "ISC", "codigo": "FIS-101-ISC", "nombre": "Física General", "unidades": 5, "creditos": 5},
        {"carrera": "IAU", "codigo": "FIS-101-IAU", "nombre": "Física General", "unidades": 5, "creditos": 5},
    ]

    materias = []
    for data in materias_data:
        carrera = carreras[data.pop("carrera")]
        m = Materia.objects.create(carrera=carrera, **data)
        materias.append(m)

    print("Creando Profesores...")
    profesores_data = [
        {"numero_empleado": "EMP-001", "nombre": "Juan", "apellidos": "Pérez Gómez", "email": "juan.perez@itsur.edu.mx", "especialidad": "Matemáticas"},
        {"numero_empleado": "EMP-002", "nombre": "María", "apellidos": "López Cruz", "email": "maria.lopez@itsur.edu.mx", "especialidad": "Física"},
        {"numero_empleado": "EMP-003", "nombre": "Carlos", "apellidos": "Martínez Ruiz", "email": "carlos.martinez@itsur.edu.mx", "especialidad": "Sistemas Computacionales"},
        {"numero_empleado": "EMP-004", "nombre": "Ana", "apellidos": "García Fernández", "email": "ana.garcia@itsur.edu.mx", "especialidad": "Química y Biología"},
        {"numero_empleado": "EMP-005", "nombre": "Roberto", "apellidos": "Sánchez Torres", "email": "roberto.sanchez@itsur.edu.mx", "especialidad": "Administración"},
        {"numero_empleado": "EMP-006", "nombre": "Laura", "apellidos": "Ramírez Díaz", "email": "laura.ramirez@itsur.edu.mx", "especialidad": "Gastronomía"},
        {"numero_empleado": "EMP-007", "nombre": "Pedro", "apellidos": "Hernández Flores", "email": "pedro.hernandez@itsur.edu.mx", "especialidad": "Ingeniería Industrial y Automotriz"},
        {"numero_empleado": "EMP-008", "nombre": "Elena", "apellidos": "Vázquez Castro", "email": "elena.vazquez@itsur.edu.mx", "especialidad": "Electrónica y Microcontroladores"},
        {"numero_empleado": "EMP-009", "nombre": "Miguel", "apellidos": "Rojas Silva", "email": "miguel.rojas@itsur.edu.mx", "especialidad": "Bases de Datos y Redes"},
    ]

    profesores = {}
    for data in profesores_data:
        p = Profesor.objects.create(**data)
        profesores[data["numero_empleado"]] = p

    print("Creando Grupos y asignando materias y profesores...")
    # Asignaciones lógicas
    asignaciones = [
        # Profesor de Matemáticas (Juan) da Cálculo en varias carreras
        (Materia.objects.get(codigo="MAT-101-ISC"), profesores["EMP-001"], "1A", "L-V 07:00-08:00"),
        (Materia.objects.get(codigo="MAT-101-IEL"), profesores["EMP-001"], "1A", "L-V 08:00-09:00"),
        (Materia.objects.get(codigo="MAT-101-IIN"), profesores["EMP-001"], "1B", "L-V 09:00-10:00"),
        
        # Profesora de Física (María) da Física General
        (Materia.objects.get(codigo="FIS-101-ISC"), profesores["EMP-002"], "1A", "L-J 10:00-11:15"),
        (Materia.objects.get(codigo="FIS-101-IAU"), profesores["EMP-002"], "2A", "L-J 11:15-12:30"),
        
        # Profesores de Sistemas
        (Materia.objects.get(codigo="ISC-101"), profesores["EMP-003"], "1A", "L-V 11:00-12:00"),
        (Materia.objects.get(codigo="ISC-102"), profesores["EMP-003"], "2A", "L-V 12:00-13:00"),
        (Materia.objects.get(codigo="ISC-103"), profesores["EMP-009"], "3A", "L-V 09:00-10:00"),
        (Materia.objects.get(codigo="ISC-104"), profesores["EMP-009"], "4A", "L-V 10:00-11:00"),
        
        # Electrónica
        (Materia.objects.get(codigo="IEL-101"), profesores["EMP-008"], "3A", "Ma-J 07:00-09:00"),
        (Materia.objects.get(codigo="IEL-103"), profesores["EMP-008"], "5A", "Ma-J 09:00-11:00"),
        
        # Ambiental
        (Materia.objects.get(codigo="IAM-101"), profesores["EMP-004"], "1A", "L-M-V 08:00-10:00"),
        (Materia.objects.get(codigo="IAM-102"), profesores["EMP-004"], "2A", "Ma-J 08:00-10:00"),
        
        # Gastronomía
        (Materia.objects.get(codigo="LGA-101"), profesores["EMP-006"], "1A", "L-V 14:00-16:00"),
        (Materia.objects.get(codigo="LGA-102"), profesores["EMP-006"], "2A", "L-V 16:00-18:00"),
        
        # Gestión Empresarial
        (Materia.objects.get(codigo="IGE-101"), profesores["EMP-005"], "1A", "L-J 16:00-17:15"),
        (Materia.objects.get(codigo="IGE-102"), profesores["EMP-005"], "2A", "L-J 17:15-18:30"),
        
        # Industrial y Automotriz
        (Materia.objects.get(codigo="IIN-101"), profesores["EMP-007"], "2A", "V 07:00-11:00"),
        (Materia.objects.get(codigo="IAU-101"), profesores["EMP-007"], "3A", "L-M 11:00-13:30"),
    ]

    for materia, profesor, clave, horario in asignaciones:
        Grupo.objects.create(
            materia=materia,
            profesor=profesor,
            clave=clave,
            cupo=30,
            horario=horario
        )
        
    print("¡Base de datos poblada exitosamente!")

if __name__ == '__main__':
    populate()
