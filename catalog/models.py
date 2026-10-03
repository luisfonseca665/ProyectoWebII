from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User # NUEVO IMPORTE

class Carrera(models.Model):
    """Modelo que representa una carrera universitaria."""
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Código identificador de la carrera"
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
        return self.nombre

    def get_absolute_url(self):
        return reverse('carrera-detail', args=[str(self.id)])


class Materia(models.Model):
    """Modelo que representa una materia perteneciente a una carrera."""
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE, related_name='materias')
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=40)
    unidades = models.PositiveIntegerField(help_text="Número de unidades del temario")
    creditos = models.PositiveIntegerField()

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('materia-detail', args=[str(self.id)])


class Alumno(models.Model):
    """Modelo que representa a un estudiante matriculado."""
    ESTATUS_CHOICES = (
        ('A', 'Activo'),
        ('B', 'Baja'),
        ('E', 'Egresado'),
    )
    
    # NUEVO CAMPO PARA AUTENTICACIÓN
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='alumno_perfil')
    
    matricula = models.CharField(max_length=20, unique=True, primary_key=True)
    carrera = models.ForeignKey('Carrera', on_delete=models.RESTRICT, related_name='alumnos')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    estatus = models.CharField(
        max_length=1, 
        choices=ESTATUS_CHOICES, 
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
    """Modelo que representa a un profesor de la institución."""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profesor_perfil')
    numero_empleado = models.CharField(
        max_length=20, 
        unique=True, 
        primary_key=True,
        help_text="Número de nómina o identificador del docente"
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

    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name_plural = "Profesores"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def get_absolute_url(self):
        return reverse('profesor-detail', args=[str(self.numero_empleado)])


class Grupo(models.Model):
    """Modelo que representa un grupo específico para una materia."""
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='grupos')
    profesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos')
    clave = models.CharField(max_length=50)
    cupo = models.PositiveIntegerField()
    numAlumnos = models.PositiveIntegerField(
        default=0, 
        help_text="Cantidad actual de alumnos inscritos"
    )
    horario = models.CharField(max_length=100)
    
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