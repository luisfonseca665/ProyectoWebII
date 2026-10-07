from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User # NUEVO IMPORTE

class Carrera(models.Model):
    """
    Representa una carrera universitaria dentro del sistema.
    Aquí guardamos la información básica como su nombre, la clave que la identifica,
    y cuántos créditos y semestres dura en total.
    """
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Id de la carrera"
    )
    nombre = models.CharField(
        max_length=40,
        help_text="Ej. Ingeniería en Sistemas Computacionales"
    )
    creditos = models.PositiveIntegerField(help_text="Total de créditos de la carrera")
    duracion = models.PositiveIntegerField(help_text="Duración en semestres")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        """Devuelve el nombre de la carrera para que sea fácil de identificar en los menús."""
        return self.nombre

    def get_absolute_url(self):
        """Genera la ruta o enlace directo para ver los detalles de esta carrera en específico."""
        return reverse('carrera-detail', args=[str(self.id)])


class Materia(models.Model):
    """
    Representa una materia que pertenece a una carrera.
    Guarda los detalles académicos como las unidades temáticas y los créditos que aporta.
    """
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE, related_name='materias')
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=40)
    unidades = models.PositiveIntegerField(help_text="Número de unidades del temario")
    creditos = models.PositiveIntegerField()

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        """Muestra el código y el nombre de la materia (Ej. 'AED-1026 - Estructura de Datos')."""
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        """Devuelve la URL para acceder a la vista de detalles de esta materia."""
        return reverse('materia-detail', args=[str(self.id)])


class Perfil(models.Model):
    """Modelo que representa el perfil de cada usuario"""
    ROLES = (
        ('CONTROL_ESCOLAR', 'Control escolar'),
        ('COORDINADOR', 'Coordinador'),
        ('PROFESOR', 'Profesor'),
        ('ALUMNO', 'Alumno'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        username = self.usuario.username if self.usuario else 'Sin usuario'
        return f"{username} - {self.get_rol_display()}"


class Alumno(models.Model):
    """Modelo que representa a un estudiante"""
    ESTATUS = (
        ('A', 'Activo'),
        ('B', 'Baja'),
        ('E', 'Egresado'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='alumno_perfil')
    
    matricula = models.CharField(max_length=20, unique=True, primary_key=True)
    carrera = models.ForeignKey('Carrera', on_delete=models.RESTRICT, related_name='alumnos')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    estatus = models.CharField(
        max_length=1, 
        choices=ESTATUS, 
        default='A'
    )
    semestre = models.PositiveIntegerField()

    class Meta:
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f"{self.matricula} - {self.apellidos} {self.nombre}"

    def get_absolute_url(self):
        return reverse('alumno-detail', args=[str(self.matricula)])


class Profesor(models.Model):
    """Modelo que representa a un profesor"""

    ESTATUS = (
        ('A', 'Activo'),
        ('B', 'Baja')
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profesor_perfil')
    numero_empleado = models.CharField(
        max_length=20, 
        unique=True, 
        primary_key=True,
        help_text="Identificador del docente"
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True, help_text="Correo institucional")
    especialidad = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ej. Ingeniería en Sistemas Computacionales, Ciencias Básicas"
    )
    estatus = models.CharField(
        max_length=1,
        choices=ESTATUS,
        default='A'
    )

    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name_plural = "Profesores"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def get_absolute_url(self):
        return reverse('profesor-detail', args=[str(self.numero_empleado)])


class Grupo(models.Model):
    """Modelo que representa un grupo"""
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='grupos')
    profesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos')
    clave = models.CharField(max_length=50)
    cupo = models.PositiveIntegerField()
    numAlumnos = models.PositiveIntegerField(
        default=0, 
        help_text="Cantidad actual de alumnos inscritos"
    )
    horario = models.CharField(max_length=100)
    activo = models.BooleanField(default=True, help_text="Para borrado lógico")
    
    alumnos = models.ManyToManyField(
        'Alumno', 
        through='Calificacion',
        help_text="Alumnos inscritos en este grupo"
    )

    class Meta:
        ordering = ['materia', 'clave']

    def __str__(self):
        return f"Grupo {self.clave} - {self.materia.nombre}"

    def get_absolute_url(self):
        return reverse('grupo-detail', args=[str(self.id)])


class Calificacion(models.Model):
    """Clase de asociación que relaciona Alumnos con Grupos y almacena su calificación final."""
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    
    calificacion_final = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name_plural = "Calificaciones"
        constraints = [
            models.UniqueConstraint(fields=['alumno', 'grupo'], name='unique_alumno_grupo')
        ]

    def __str__(self):
        return f"{self.alumno.matricula} en {self.grupo.clave}"