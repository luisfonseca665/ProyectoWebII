import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sicenet2.settings')
django.setup()

from django.contrib.auth.models import User
from catalog.models import Alumno, Profesor, Perfil

def asignar_usuarios():
    print("Iniciando asignación de usuarios y perfiles...")

    # 1. Crear usuarios para Profesores
    profesores = Profesor.objects.all()
    prof_creados = 0
    for prof in profesores:
        username = prof.numero_empleado.lower().replace("-", "_")
        # Si no tiene usuario asignado, buscar o crear
        if not prof.usuario:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': prof.nombre,
                    'last_name': prof.apellidos,
                    'email': prof.email,
                    'is_staff': False
                }
            )
            if created:
                user.set_password("Profesor123!")
                user.save()
            
            prof.usuario = user
            prof.save()

            # Crear o actualizar Perfil con rol PROFESOR
            Perfil.objects.update_or_create(
                usuario=user,
                defaults={'rol': 'PROFESOR'}
            )
            prof_creados += 1

    print(f"Profesores vinculados con usuario y rol PROFESOR: {prof_creados}")

    # 2. Crear usuarios para Alumnos
    alumnos = Alumno.objects.all()
    alum_creados = 0
    for alum in alumnos:
        username = alum.matricula.lower()
        if not alum.usuario:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': alum.nombre,
                    'last_name': alum.apellidos,
                    'email': f"{username}@itsur.edu.mx",
                    'is_staff': False
                }
            )
            if created:
                user.set_password("Alumno123!")
                user.save()
            
            alum.usuario = user
            alum.save()

            # Crear o actualizar Perfil con rol ALUMNO
            Perfil.objects.update_or_create(
                usuario=user,
                defaults={'rol': 'ALUMNO'}
            )
            alum_creados += 1

    print(f"Alumnos vinculados con usuario y rol ALUMNO: {alum_creados}")

    # 3. Crear usuarios de prueba para Control Escolar y Coordinador
    user_ce, created_ce = User.objects.get_or_create(
        username="control_escolar",
        defaults={
            'first_name': 'Encargado',
            'last_name': 'Control Escolar',
            'email': 'control.escolar@itsur.edu.mx',
            'is_staff': True
        }
    )
    if created_ce:
        user_ce.set_password("Control123!")
        user_ce.save()
    Perfil.objects.update_or_create(usuario=user_ce, defaults={'rol': 'CONTROL_ESCOLAR'})

    user_coord, created_coord = User.objects.get_or_create(
        username="coordinador",
        defaults={
            'first_name': 'Coordinador',
            'last_name': 'Académico',
            'email': 'coordinador@itsur.edu.mx',
            'is_staff': False
        }
    )
    if created_coord:
        user_coord.set_password("Coord123!")
        user_coord.save()
    Perfil.objects.update_or_create(usuario=user_coord, defaults={'rol': 'COORDINADOR'})

    print("Usuarios de prueba creados:")
    print(" - Control Escolar: usuario 'control_escolar', contraseña 'Control123!'")
    print(" - Coordinador: usuario 'coordinador', contraseña 'Coord123!'")
    print(" - Profesores: usuario '[numero_empleado]', contraseña 'Profesor123!'")
    print(" - Alumnos: usuario '[matricula]', contraseña 'Alumno123!'")
    print("¡Asignación completada con éxito!")

if __name__ == '__main__':
    asignar_usuarios()
