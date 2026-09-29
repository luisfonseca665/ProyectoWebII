import os

base_dir = r"c:\Users\garci\Documentos\ITSUR\7 Semestre\Programacion Web II\ProyectoWebII\catalog"
templates_dir = os.path.join(base_dir, 'templates')
catalog_templates_dir = os.path.join(templates_dir, 'catalog')

os.makedirs(catalog_templates_dir, exist_ok=True)

# 1. Update views.py
views_content = """from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Carrera, Materia, Alumno, Profesor, Grupo, Calificacion
from django.db.models import Avg, Count

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_alumnos'] = Alumno.objects.count()
        context['num_profesores'] = Profesor.objects.count()
        context['num_grupos'] = Grupo.objects.count()
        context['num_carreras'] = Carrera.objects.count()
        return context

# --- CARRERA ---
class CarreraListView(ListView): model = Carrera; template_name = 'carrera_list.html'
class CarreraDetailView(DetailView): model = Carrera; template_name = 'catalog/carrera_detail.html'
class CarreraCreateView(CreateView): model = Carrera; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('carreras')
class CarreraUpdateView(UpdateView): model = Carrera; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('carreras')
class CarreraDeleteView(DeleteView): model = Carrera; success_url = reverse_lazy('carreras'); template_name = 'confirm_delete.html'

# --- MATERIA ---
class MateriaListView(ListView): model = Materia; template_name = 'materia_list.html'
class MateriaDetailView(DetailView): model = Materia; template_name = 'catalog/materia_detail.html'
class MateriaCreateView(CreateView): model = Materia; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('materias')
class MateriaUpdateView(UpdateView): model = Materia; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('materias')
class MateriaDeleteView(DeleteView): model = Materia; success_url = reverse_lazy('materias'); template_name = 'confirm_delete.html'

# --- ALUMNO ---
class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumno_list.html'
    def get_queryset(self):
        return Alumno.objects.annotate(promedio=Avg('calificacion__calificacion_final'))

class AlumnoDetailView(DetailView): 
    model = Alumno
    template_name = 'catalog/alumno_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calificaciones'] = Calificacion.objects.filter(alumno=self.object)
        return context

class AlumnoCreateView(CreateView): model = Alumno; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('alumnos')
class AlumnoUpdateView(UpdateView): model = Alumno; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('alumnos')
class AlumnoDeleteView(DeleteView): model = Alumno; success_url = reverse_lazy('alumnos'); template_name = 'confirm_delete.html'

# --- PROFESOR ---
class ProfesorListView(ListView): model = Profesor; template_name = 'profesor_list.html'
class ProfesorDetailView(DetailView): model = Profesor; template_name = 'catalog/profesor_detail.html'
class ProfesorCreateView(CreateView): model = Profesor; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('profesores')
class ProfesorUpdateView(UpdateView): model = Profesor; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('profesores')
class ProfesorDeleteView(DeleteView): model = Profesor; success_url = reverse_lazy('profesores'); template_name = 'confirm_delete.html'

# --- GRUPO ---
class GrupoListView(ListView): model = Grupo; template_name = 'grupo_list.html'
class GrupoDetailView(DetailView): model = Grupo; template_name = 'catalog/grupo_detail.html'
class GrupoCreateView(CreateView): model = Grupo; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('grupos')
class GrupoUpdateView(UpdateView): model = Grupo; fields = '__all__'; template_name = 'form_generico.html'; success_url = reverse_lazy('grupos')
class GrupoDeleteView(DeleteView): model = Grupo; success_url = reverse_lazy('grupos'); template_name = 'confirm_delete.html'
"""
with open(os.path.join(base_dir, 'views.py'), 'w', encoding='utf-8') as f:
    f.write(views_content)

# 2. Update urls.py
urls_content = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('carreras/', views.CarreraListView.as_view(), name='carreras'),
    path('carreras/nueva/', views.CarreraCreateView.as_view(), name='carrera-create'),
    path('carreras/<int:pk>/', views.CarreraDetailView.as_view(), name='carrera-detail'),
    path('carreras/<int:pk>/editar/', views.CarreraUpdateView.as_view(), name='carrera-update'),
    path('carreras/<int:pk>/eliminar/', views.CarreraDeleteView.as_view(), name='carrera-delete'),

    path('materias/', views.MateriaListView.as_view(), name='materias'),
    path('materias/nueva/', views.MateriaCreateView.as_view(), name='materia-create'),
    path('materias/<int:pk>/', views.MateriaDetailView.as_view(), name='materia-detail'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia-update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia-delete'),

    path('alumnos/', views.AlumnoListView.as_view(), name='alumnos'),
    path('alumnos/nuevo/', views.AlumnoCreateView.as_view(), name='alumno-create'),
    path('alumnos/<str:pk>/', views.AlumnoDetailView.as_view(), name='alumno-detail'),
    path('alumnos/<str:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno-update'),
    path('alumnos/<str:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno-delete'),

    path('profesores/', views.ProfesorListView.as_view(), name='profesores'),
    path('profesores/nuevo/', views.ProfesorCreateView.as_view(), name='profesor-create'),
    path('profesores/<str:pk>/', views.ProfesorDetailView.as_view(), name='profesor-detail'),
    path('profesores/<str:pk>/editar/', views.ProfesorUpdateView.as_view(), name='profesor-update'),
    path('profesores/<str:pk>/eliminar/', views.ProfesorDeleteView.as_view(), name='profesor-delete'),

    path('grupos/', views.GrupoListView.as_view(), name='grupos'),
    path('grupos/nuevo/', views.GrupoCreateView.as_view(), name='grupo-create'),
    path('grupos/<int:pk>/', views.GrupoDetailView.as_view(), name='grupo-detail'),
    path('grupos/<int:pk>/editar/', views.GrupoUpdateView.as_view(), name='grupo-update'),
    path('grupos/<int:pk>/eliminar/', views.GrupoDeleteView.as_view(), name='grupo-delete'),
]
"""
with open(os.path.join(base_dir, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write(urls_content)


# 3. Create pagina_maestra.html
pagina_maestra = """<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Control Escolar{% endblock %}</title>
    <!-- Bootstrap CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'home' %}"><i class="bi bi-mortarboard-fill"></i> SICE</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="{% url 'home' %}">Inicio</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Catálogos
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="{% url 'alumnos' %}">Alumnos</a></li>
                <li><a class="dropdown-item" href="{% url 'profesores' %}">Profesores</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="{% url 'carreras' %}">Carreras</a></li>
                <li><a class="dropdown-item" href="{% url 'materias' %}">Materias</a></li>
                <li><a class="dropdown-item" href="{% url 'grupos' %}">Grupos</a></li>
              </ul>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Buscar..." aria-label="Buscar">
            <button class="btn btn-outline-light" type="submit">Buscar</button>
          </form>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container fluid mt-4 mb-5">
        {% block content %}
        {% endblock %}
    </div>

    <!-- Bootstrap JS CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'pagina_maestra.html'), 'w', encoding='utf-8') as f:
    f.write(pagina_maestra)

# 4. Create home.html
home = """{% extends "pagina_maestra.html" %}

{% block title %}Inicio - Control Escolar{% endblock %}

{% block content %}
<div class="p-5 mb-4 bg-secondary-subtle rounded-3 text-center">
    <div class="container-fluid py-5">
      <h1 class="display-5 fw-bold">Sistema Integral de Control Escolar</h1>
      <p class="col-md-8 mx-auto fs-4">Bienvenido al panel de administración. Aquí podrás gestionar los catálogos principales de la institución educativa.</p>
    </div>
</div>

<div class="row text-center mt-4">
    <div class="col-md-3">
        <div class="card text-bg-primary mb-3">
            <div class="card-header">Alumnos Registrados</div>
            <div class="card-body">
              <h1 class="card-title">{{ num_alumnos }}</h1>
              <a href="{% url 'alumnos' %}" class="btn btn-light btn-sm mt-2">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-success mb-3">
            <div class="card-header">Profesores Activos</div>
            <div class="card-body">
              <h1 class="card-title">{{ num_profesores }}</h1>
              <a href="{% url 'profesores' %}" class="btn btn-light btn-sm mt-2">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-warning mb-3">
            <div class="card-header">Grupos Creados</div>
            <div class="card-body">
              <h1 class="card-title">{{ num_grupos }}</h1>
              <a href="{% url 'grupos' %}" class="btn btn-dark btn-sm mt-2">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-info mb-3">
            <div class="card-header">Carreras Ofertadas</div>
            <div class="card-body">
              <h1 class="card-title">{{ num_carreras }}</h1>
              <a href="{% url 'carreras' %}" class="btn btn-dark btn-sm mt-2">Ver Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home)

# 5. Generic templates
form_generico = """{% extends "pagina_maestra.html" %}
{% block title %}Formulario{% endblock %}
{% block content %}
<div class="card mx-auto" style="max-width: 600px;">
    <div class="card-header bg-primary text-white">
        <h5>Formulario de Registro / Edición</h5>
    </div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar</button>
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}"""
with open(os.path.join(templates_dir, 'form_generico.html'), 'w', encoding='utf-8') as f:
    f.write(form_generico)

confirm_delete = """{% extends "pagina_maestra.html" %}
{% block title %}Confirmar Eliminación{% endblock %}
{% block content %}
<div class="alert alert-danger" role="alert">
  <h4 class="alert-heading">¿Estás seguro?</h4>
  <p>Estás a punto de eliminar el registro: <strong>{{ object }}</strong>. Esta acción no se puede deshacer.</p>
  <hr>
  <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sí, Eliminar</button>
      <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}"""
with open(os.path.join(templates_dir, 'confirm_delete.html'), 'w', encoding='utf-8') as f:
    f.write(confirm_delete)

# 6. Create Lists
def write_list(name, title, btn_url, headers, row_html):
    content = f"""{{% extends "pagina_maestra.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h2>{title}</h2>
    <a href="{{% url '{btn_url}' %}}" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Agregar Nuevo</a>
</div>
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="table-dark text-white">
            <tr>
                {headers}
                <th>Operaciones</th>
            </tr>
        </thead>
        <tbody>
            {{% for item in object_list %}}
            <tr>
                {row_html}
            </tr>
            {{% empty %}}
            <tr>
                <td colspan="100%" class="text-center">No hay registros disponibles.</td>
            </tr>
            {{% endfor %}}
        </tbody>
    </table>
</div>
{{% endblock %}}
"""
    with open(os.path.join(templates_dir, f'{name}_list.html'), 'w', encoding='utf-8') as f:
        f.write(content)

write_list('alumno', 'Lista de Alumnos', 'alumno-create', 
    '<th>Matrícula</th><th>Nombre Completo</th><th>Carrera</th><th>Estatus</th><th>Semestre</th><th>Promedio</th>',
    """<td><a href="{{ item.get_absolute_url }}">{{ item.matricula }}</a></td>
       <td>{{ item.apellidos }} {{ item.nombre }}</td>
       <td>{{ item.carrera.codigo }}</td>
       <td>{{ item.get_estatus_display }}</td>
       <td>{{ item.semestre }}</td>
       <td>{{ item.promedio|floatformat:2|default:"N/A" }}</td>
       <td>
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
           <a href="{% url 'alumno-update' item.matricula %}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
           <a href="{% url 'alumno-delete' item.matricula %}" class="btn btn-sm btn-danger" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('profesor', 'Lista de Profesores', 'profesor-create',
    '<th>No. Empleado</th><th>Nombre Completo</th><th>Especialidad</th><th>Correo</th>',
    """<td><a href="{{ item.get_absolute_url }}">{{ item.numero_empleado }}</a></td>
       <td>{{ item.apellidos }} {{ item.nombre }}</td>
       <td>{{ item.especialidad }}</td>
       <td>{{ item.email }}</td>
       <td>
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
           <a href="{% url 'profesor-update' item.numero_empleado %}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
           <a href="{% url 'profesor-delete' item.numero_empleado %}" class="btn btn-sm btn-danger" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('carrera', 'Lista de Carreras', 'carrera-create',
    '<th>Código</th><th>Nombre de Carrera</th><th>Créditos</th><th>Semestres</th>',
    """<td><a href="{{ item.get_absolute_url }}">{{ item.codigo }}</a></td>
       <td>{{ item.nombre }}</td>
       <td>{{ item.creditos }}</td>
       <td>{{ item.duracion }}</td>
       <td>
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
           <a href="{% url 'carrera-update' item.id %}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
           <a href="{% url 'carrera-delete' item.id %}" class="btn btn-sm btn-danger" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('materia', 'Lista de Materias', 'materia-create',
    '<th>Código</th><th>Materia</th><th>Carrera</th><th>Créditos</th>',
    """<td><a href="{{ item.get_absolute_url }}">{{ item.codigo }}</a></td>
       <td>{{ item.nombre }}</td>
       <td>{{ item.carrera.nombre }}</td>
       <td>{{ item.creditos }}</td>
       <td>
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
           <a href="{% url 'materia-update' item.id %}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
           <a href="{% url 'materia-delete' item.id %}" class="btn btn-sm btn-danger" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('grupo', 'Lista de Grupos', 'grupo-create',
    '<th>Clave</th><th>Materia</th><th>Profesor</th><th>Horario</th><th>Alumnos</th>',
    """<td><a href="{{ item.get_absolute_url }}">{{ item.clave }}</a></td>
       <td>{{ item.materia.nombre }}</td>
       <td>{{ item.profesor|default:"Sin asignar" }}</td>
       <td>{{ item.horario }}</td>
       <td>{{ item.numAlumnos }} / {{ item.cupo }}</td>
       <td>
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
           <a href="{% url 'grupo-update' item.id %}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
           <a href="{% url 'grupo-delete' item.id %}" class="btn btn-sm btn-danger" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

# 7. Create Details
alumno_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle del Alumno{% endblock %}
{% block content %}
<div class="card mb-4">
    <div class="card-header bg-primary text-white">
        <h4><i class="bi bi-person-badge"></i> {{ object.apellidos }} {{ object.nombre }}</h4>
    </div>
    <div class="card-body row">
        <div class="col-md-6">
            <p><strong>Matrícula:</strong> {{ object.matricula }}</p>
            <p><strong>Carrera:</strong> {{ object.carrera.nombre }}</p>
        </div>
        <div class="col-md-6">
            <p><strong>Estatus:</strong> {{ object.get_estatus_display }}</p>
            <p><strong>Semestre:</strong> {{ object.semestre }}</p>
        </div>
    </div>
    <div class="card-footer">
        <a href="{% url 'alumno-update' object.matricula %}" class="btn btn-warning btn-sm">Editar</a>
        <a href="{% url 'alumnos' %}" class="btn btn-secondary btn-sm">Regresar a la lista</a>
    </div>
</div>

<h4 class="mt-4">Kardex / Calificaciones</h4>
<div class="table-responsive">
    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>Materia</th>
                <th>Grupo</th>
                <th>Profesor</th>
                <th>Calificación Final</th>
            </tr>
        </thead>
        <tbody>
            {% for cal in calificaciones %}
            <tr>
                <td>{{ cal.grupo.materia.nombre }}</td>
                <td>{{ cal.grupo.clave }}</td>
                <td>{{ cal.grupo.profesor|default:"-" }}</td>
                <td>
                    {% if cal.calificacion_final %}
                        {% if cal.calificacion_final < 70 %}
                            <span class="text-danger fw-bold">{{ cal.calificacion_final }}</span>
                        {% else %}
                            <span class="text-success fw-bold">{{ cal.calificacion_final }}</span>
                        {% endif %}
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">El alumno no cuenta con calificaciones registradas.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'alumno_detail.html'), 'w', encoding='utf-8') as f:
    f.write(alumno_detail)

profesor_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle del Profesor{% endblock %}
{% block content %}
<div class="card mb-4">
    <div class="card-header bg-success text-white">
        <h4><i class="bi bi-person-video3"></i> Prof. {{ object.nombre }} {{ object.apellidos }}</h4>
    </div>
    <div class="card-body row">
        <div class="col-md-6">
            <p><strong>Número de Empleado:</strong> {{ object.numero_empleado }}</p>
            <p><strong>Correo Electrónico:</strong> <a href="mailto:{{ object.email }}">{{ object.email }}</a></p>
        </div>
        <div class="col-md-6">
            <p><strong>Especialidad:</strong> {{ object.especialidad }}</p>
        </div>
    </div>
    <div class="card-footer">
        <a href="{% url 'profesor-update' object.numero_empleado %}" class="btn btn-warning btn-sm">Editar</a>
        <a href="{% url 'profesores' %}" class="btn btn-secondary btn-sm">Regresar a la lista</a>
    </div>
</div>

<h4 class="mt-4">Grupos Asignados</h4>
<div class="table-responsive">
    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>Materia</th>
                <th>Clave Grupo</th>
                <th>Horario</th>
                <th>Alumnos Inscritos</th>
            </tr>
        </thead>
        <tbody>
            {% for grupo in object.grupos.all %}
            <tr>
                <td><a href="{{ grupo.materia.get_absolute_url }}">{{ grupo.materia.nombre }}</a></td>
                <td><a href="{{ grupo.get_absolute_url }}">{{ grupo.clave }}</a></td>
                <td>{{ grupo.horario }}</td>
                <td>{{ grupo.numAlumnos }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">El profesor no tiene grupos asignados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'profesor_detail.html'), 'w', encoding='utf-8') as f:
    f.write(profesor_detail)

carrera_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle de Carrera{% endblock %}
{% block content %}
<div class="card mb-4">
    <div class="card-header bg-info text-dark">
        <h4><i class="bi bi-building"></i> {{ object.nombre }} ({{ object.codigo }})</h4>
    </div>
    <div class="card-body">
        <p><strong>Créditos Totales:</strong> {{ object.creditos }}</p>
        <p><strong>Duración (Semestres):</strong> {{ object.duracion }}</p>
    </div>
    <div class="card-footer">
        <a href="{% url 'carrera-update' object.id %}" class="btn btn-warning btn-sm">Editar</a>
        <a href="{% url 'carreras' %}" class="btn btn-secondary btn-sm">Regresar a la lista</a>
    </div>
</div>

<h4 class="mt-4">Mapa Curricular (Materias)</h4>
<ul>
    {% for mat in object.materias.all %}
        <li><a href="{{ mat.get_absolute_url }}">{{ mat.codigo }} - {{ mat.nombre }}</a> ({{ mat.creditos }} créditos)</li>
    {% empty %}
        <li>No hay materias registradas para esta carrera.</li>
    {% endfor %}
</ul>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'carrera_detail.html'), 'w', encoding='utf-8') as f:
    f.write(carrera_detail)

materia_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle de Materia{% endblock %}
{% block content %}
<div class="card mb-4">
    <div class="card-header bg-secondary text-white">
        <h4><i class="bi bi-book"></i> {{ object.nombre }} ({{ object.codigo }})</h4>
    </div>
    <div class="card-body">
        <p><strong>Carrera:</strong> <a href="{{ object.carrera.get_absolute_url }}">{{ object.carrera.nombre }}</a></p>
        <p><strong>Unidades:</strong> {{ object.unidades }}</p>
        <p><strong>Créditos:</strong> {{ object.creditos }}</p>
    </div>
    <div class="card-footer">
        <a href="{% url 'materia-update' object.id %}" class="btn btn-warning btn-sm">Editar</a>
        <a href="{% url 'materias' %}" class="btn btn-secondary btn-sm">Regresar a la lista</a>
    </div>
</div>

<h4 class="mt-4">Grupos Abiertos</h4>
<ul>
    {% for g in object.grupos.all %}
        <li>
            <a href="{{ g.get_absolute_url }}">Grupo {{ g.clave }}</a> - Prof. {{ g.profesor|default:"Sin asignar" }} 
            (Horario: {{ g.horario }} | Inscritos: {{ g.numAlumnos }}/{{ g.cupo }})
        </li>
    {% empty %}
        <li>No hay grupos aperturados para esta materia.</li>
    {% endfor %}
</ul>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'materia_detail.html'), 'w', encoding='utf-8') as f:
    f.write(materia_detail)

grupo_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle del Grupo{% endblock %}
{% block content %}
<div class="card mb-4">
    <div class="card-header bg-dark text-white">
        <h4><i class="bi bi-people-fill"></i> Grupo {{ object.clave }} - {{ object.materia.nombre }}</h4>
    </div>
    <div class="card-body">
        <p><strong>Profesor:</strong> {% if object.profesor %}<a href="{{ object.profesor.get_absolute_url }}">{{ object.profesor }}</a>{% else %}Sin asignar{% endif %}</p>
        <p><strong>Horario:</strong> {{ object.horario }}</p>
        <p><strong>Cupo:</strong> {{ object.numAlumnos }} / {{ object.cupo }} inscritos</p>
    </div>
    <div class="card-footer">
        <a href="{% url 'grupo-update' object.id %}" class="btn btn-warning btn-sm">Editar</a>
        <a href="{% url 'grupos' %}" class="btn btn-secondary btn-sm">Regresar a la lista</a>
    </div>
</div>

<h4 class="mt-4">Alumnos Inscritos</h4>
<div class="table-responsive">
    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>Matrícula</th>
                <th>Nombre del Alumno</th>
                <th>Calificación Final</th>
            </tr>
        </thead>
        <tbody>
            {% for calif in object.calificacion_set.all %}
            <tr>
                <td><a href="{{ calif.alumno.get_absolute_url }}">{{ calif.alumno.matricula }}</a></td>
                <td>{{ calif.alumno.apellidos }} {{ calif.alumno.nombre }}</td>
                <td>
                    {% if calif.calificacion_final < 70 %}
                        <span class="text-danger fw-bold">{{ calif.calificacion_final }}</span>
                    {% else %}
                        <span class="text-success">{{ calif.calificacion_final }}</span>
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="3" class="text-center">No hay alumnos inscritos en este grupo.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'grupo_detail.html'), 'w', encoding='utf-8') as f:
    f.write(grupo_detail)

print("UI Generada Correctamente.")
