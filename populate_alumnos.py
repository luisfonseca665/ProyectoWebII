import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sicenet2.settings')
django.setup()

from catalog.models import Carrera, Grupo, Alumno, Calificacion

def generate_students():
    print("Borrando alumnos y calificaciones anteriores...")
    Calificacion.objects.all().delete()
    Alumno.objects.all().delete()

    nombres_list = [
        "Alejandro", "María", "José", "Guadalupe", "Francisco", "Juana", "Antonio", "Margarita",
        "Miguel", "Rosa", "Daniel", "Alicia", "Carlos", "Silvia", "Eduardo", "Teresa", "Jorge", 
        "Josefina", "Fernando", "Laura", "Roberto", "Patricia", "Javier", "Diana", "Luis", 
        "Andrea", "Ricardo", "Gabriela", "Hugo", "Verónica", "Andrés", "Daniela", "Diego",
        "Carmen", "Rafael", "Leticia", "Mauricio", "Brenda", "Arturo", "Susana"
    ]
    apellidos_list = [
        "Hernández", "García", "Martínez", "López", "González", "Pérez", "Rodríguez",
        "Sánchez", "Ramírez", "Cruz", "Gómez", "Flores", "Morales", "Vázquez", "Jiménez",
        "Reyes", "Díaz", "Torres", "Gutiérrez", "Ruiz", "Mendoza", "Aguilar", "Ortiz",
        "Moreno", "Castillo", "Romero", "Álvarez", "Chávez", "Rivera", "Juárez", "Ramos",
        "Domínguez", "Herrera", "Medina", "Castro", "Vargas", "Guzmán", "Velázquez", "Rojas"
    ]

    carreras = Carrera.objects.all()
    
    total_alumnos = 0
    alumnos_por_carrera = random.randint(25, 40) # 25-40 students per career

    print(f"Generando alumnos para {carreras.count()} carreras...")

    for carrera in carreras:
        # Get groups for this career
        grupos_carrera = Grupo.objects.filter(materia__carrera=carrera)
        
        for i in range(1, alumnos_por_carrera + 1):
            nombre = random.choice(nombres_list)
            apellidos = f"{random.choice(apellidos_list)} {random.choice(apellidos_list)}"
            matricula = f"23{carrera.codigo}{str(i).zfill(3)}" # e.g. 23ISC001 (Año 2023, Carrera ISC, Número 001)
            
            # Semestre aleatorio basado en la duración de la carrera
            semestre = random.randint(1, carrera.duracion)
            
            # Estatus (80% Activo, 10% Baja, 10% Egresado)
            rand_estatus = random.random()
            if rand_estatus < 0.8:
                estatus = 'A'
            elif rand_estatus < 0.9:
                estatus = 'B'
            else:
                estatus = 'E'

            alumno = Alumno.objects.create(
                matricula=matricula,
                carrera=carrera,
                nombre=nombre,
                apellidos=apellidos,
                estatus=estatus,
                semestre=semestre
            )
            total_alumnos += 1

            # Inscribir alumno a 2-4 grupos al azar correspondientes a su carrera
            if grupos_carrera.exists():
                num_grupos_inscribir = min(random.randint(2, 4), grupos_carrera.count())
                grupos_seleccionados = random.sample(list(grupos_carrera), num_grupos_inscribir)
                
                for grupo in grupos_seleccionados:
                    # Generar calificación (Campana de Gauss simulada para que sea realista)
                    # Mayormente entre 70 y 100, algunos reprobados
                    prob = random.random()
                    if prob < 0.05:
                        calif = random.uniform(0, 69.9) # 5% reprueban
                    elif prob < 0.15:
                        calif = random.uniform(70, 75) # 10% panzazo
                    elif prob < 0.60:
                        calif = random.uniform(76, 90) # 45% regular a bueno
                    else:
                        calif = random.uniform(91, 100) # 40% excelente

                    calificacion = Decimal(calif).quantize(Decimal('0.01'))

                    Calificacion.objects.create(
                        alumno=alumno,
                        grupo=grupo,
                        calificacion_final=calificacion
                    )
                    
                    # Actualizar numAlumnos del grupo
                    grupo.numAlumnos = grupo.calificacion_set.count()
                    grupo.save()

    print(f"¡Se han creado {total_alumnos} alumnos y sus calificaciones con éxito!")

if __name__ == '__main__':
    generate_students()
