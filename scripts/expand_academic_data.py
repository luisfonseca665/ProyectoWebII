import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sicenet2.settings')
django.setup()

from catalog.models import Carrera, Materia, Profesor, Grupo, Alumno, Calificacion

def expand_data():
    print("Añadiendo nuevas materias por carrera...")
    
    nuevas_materias = {
        "ISC": [
            ("ISC-201", "Algoritmos y Lógica de Programación", 5, 5),
            ("ISC-202", "Sistemas Operativos", 5, 5),
            ("ISC-203", "Arquitectura de Computadoras", 5, 5),
            ("ISC-204", "Programación Web", 5, 5),
            ("ISC-205", "Inteligencia Artificial", 5, 5),
            ("ISC-206", "Taller de Bases de Datos", 4, 4),
            ("ISC-207", "Ingeniería de Software II", 5, 5),
            ("ISC-208", "Graficación", 4, 4),
        ],
        "IEL": [
            ("IEL-201", "Álgebra Lineal Aplicada", 5, 5),
            ("IEL-202", "Electrónica de Potencia", 5, 5),
            ("IEL-203", "Sistemas Digitales", 5, 5),
            ("IEL-204", "Instrumentación Industrial", 4, 4),
            ("IEL-205", "Control Clásico", 5, 5),
            ("IEL-206", "Procesamiento Digital de Señales", 5, 5),
            ("IEL-207", "Optoelectrónica", 4, 4),
        ],
        "IAM": [
            ("IAM-201", "Ecología General", 4, 4),
            ("IAM-202", "Geología Ambiental", 4, 4),
            ("IAM-203", "Hidrología Superficial", 5, 5),
            ("IAM-204", "Toxicología Ambiental", 5, 5),
            ("IAM-205", "Gestión de Residuos Sólidos", 5, 5),
            ("IAM-206", "Energías Renovables", 4, 4),
            ("IAM-207", "Evaluación de Impacto Ambiental", 5, 5),
        ],
        "LGA": [
            ("LGA-201", "Enología y Maridaje", 4, 4),
            ("LGA-202", "Cocina Mexicana Tradicional", 6, 6),
            ("LGA-203", "Ensamble y Diseño de Menús", 4, 4),
            ("LGA-204", "Seguridad e Higiene Alimentaria", 4, 4),
            ("LGA-205", "Administración de Restaurantes", 5, 5),
            ("LGA-206", "Cocina Asiática", 5, 5),
            ("LGA-207", "Garde Manger y Arte Culinario", 5, 5),
        ],
        "IGE": [
            ("IGE-201", "Mercadotecnia Digital", 5, 5),
            ("IGE-202", "Derecho Laboral y Mercantil", 4, 4),
            ("IGE-203", "Logística y Cadena de Suministro", 5, 5),
            ("IGE-204", "Economía Empresarial", 5, 5),
            ("IGE-205", "Habilidades Directivas", 4, 4),
            ("IGE-206", "Desarrollo Sustentable", 5, 5),
            ("IGE-207", "Plan de Negocios e Incubación", 5, 5),
        ],
        "IIN": [
            ("IIN-201", "Ergonomía Industrial", 5, 5),
            ("IIN-202", "Simulación de Procesos", 5, 5),
            ("IIN-203", "Logística Industrial", 5, 5),
            ("IIN-204", "Metrología y Normalización", 4, 4),
            ("IIN-205", "Control Estadístico de la Calidad", 5, 5),
            ("IIN-206", "Mantenimiento Industrial", 4, 4),
            ("IIN-207", "Automatización Industrial", 5, 5),
        ],
        "IAU": [
            ("IAU-201", "Termodinámica Aplicada", 5, 5),
            ("IAU-202", "Sistemas de Frenos y Suspensión", 5, 5),
            ("IAU-203", "Electrónica Automotriz", 5, 5),
            ("IAU-204", "Autotrónica y Escáner", 5, 5),
            ("IAU-205", "Diseño Asistido por Computadora (CAD)", 4, 4),
            ("IAU-206", "Transmisiones Automáticas", 5, 5),
            ("IAU-207", "Diagnóstico Avanzado Automotriz", 5, 5),
        ]
    }

    profesores = list(Profesor.objects.all())
    
    for codigo_carrera, materias_info in nuevas_materias.items():
        try:
            carrera = Carrera.objects.get(codigo=codigo_carrera)
        except Carrera.DoesNotExist:
            continue

        for cod, nom, uni, cred in materias_info:
            materia, created = Materia.objects.get_or_create(
                codigo=cod,
                defaults={
                    "carrera": carrera,
                    "nombre": nom,
                    "unidades": uni,
                    "creditos": cred
                }
            )
            # Create 1 or 2 groups for this materia
            for clave in ["1A", "2A"]:
                profesor = random.choice(profesores)
                horario = f"L-V {random.randint(7, 18)}:00-{random.randint(7, 18)+1}:00"
                Grupo.objects.get_or_create(
                    materia=materia,
                    clave=clave,
                    defaults={
                        "profesor": profesor,
                        "cupo": 35,
                        "numAlumnos": 0,
                        "horario": horario
                    }
                )

    print("Actualizando kardex de los alumnos con más materias y calificaciones...")
    
    alumnos = Alumno.objects.all()
    for alumno in alumnos:
        # Get all groups available for the student's career
        grupos_disponibles = list(Grupo.objects.filter(materia__carrera=alumno.carrera))
        
        # Determine how many groups to enroll (between 6 and 10)
        num_grupos = min(random.randint(6, 10), len(grupos_disponibles))
        grupos_inscribir = random.sample(grupos_disponibles, num_grupos)
        
        for grupo in grupos_inscribir:
            if not Calificacion.objects.filter(alumno=alumno, grupo=grupo).exists():
                prob = random.random()
                if prob < 0.08:
                    calif = random.uniform(50, 69.9) # reprobado
                elif prob < 0.25:
                    calif = random.uniform(70, 79.9) # regular
                elif prob < 0.70:
                    calif = random.uniform(80, 92) # bueno
                else:
                    calif = random.uniform(93, 100) # excelente
                
                calificacion = Decimal(calif).quantize(Decimal('0.01'))
                
                Calificacion.objects.create(
                    alumno=alumno,
                    grupo=grupo,
                    calificacion_final=calificacion
                )

        # Update student count per group
        for g in grupos_disponibles:
            g.numAlumnos = g.calificacion_set.count()
            g.save()

    print("¡Kardex de alumnos enriquecido exitosamente con múltiples materias!")

if __name__ == '__main__':
    expand_data()
