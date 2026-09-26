from django.shortcuts import render
from django.views.generic import ListView
from .models import Alumno
from django.db.models import Avg

class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumnos.html'

    def get_queryset(self):
        return Alumno.objects.annotate(
            promedio=Avg('calificacion__calificacion_final')
        )