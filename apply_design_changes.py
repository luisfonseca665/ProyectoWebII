import os

base_dir = r"c:\Users\garci\Documentos\ITSUR\7 Semestre\Programacion Web II\ProyectoWebII\catalog"
templates_dir = os.path.join(base_dir, 'templates')
catalog_templates_dir = os.path.join(templates_dir, 'catalog')

# 1. Update pagina_maestra.html
pagina_maestra = """<!DOCTYPE html>
<html lang="es" data-bs-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Control Escolar{% endblock %}</title>
    <!-- Bootstrap CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        .navbar-custom {
            background-color: #198754 !important;
        }
        .text-success-custom {
            color: #198754 !important;
        }
        .bg-success-custom {
            background-color: #198754 !important;
        }
    </style>
</head>
<body class="bg-light">
    <!-- Navbar Verde -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom shadow-sm">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="{% url 'home' %}"><i class="bi bi-mortarboard-fill me-1"></i> SICE</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link text-white" aria-current="page" href="{% url 'home' %}">Inicio</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
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
    <div class="container mt-4 mb-5">
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


# 2. Update home.html
home = """{% extends "pagina_maestra.html" %}

{% block title %}Inicio - Control Escolar{% endblock %}

{% block content %}
<div class="mb-4">
    <h3 class="fw-bold text-success-custom mb-1">Sistema Integral de Control Escolar</h3>
    <p class="text-muted fs-6 mb-0">Bienvenido al panel de administración. Aquí podrás gestionar los catálogos principales de la institución educativa.</p>
</div>

<div class="row text-center mt-4">
    <div class="col-md-3 mb-3">
        <div class="card bg-white shadow-sm" style="border: 1px solid #000;">
            <div class="card-header bg-white fw-bold text-success-custom border-bottom" style="border-color: #000 !important;">Alumnos Registrados</div>
            <div class="card-body">
              <h2 class="card-title text-dark fw-bold mb-3">{{ num_alumnos }}</h2>
              <a href="{% url 'alumnos' %}" class="btn btn-outline-success btn-sm">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card bg-white shadow-sm" style="border: 1px solid #000;">
            <div class="card-header bg-white fw-bold text-success-custom border-bottom" style="border-color: #000 !important;">Profesores Activos</div>
            <div class="card-body">
              <h2 class="card-title text-dark fw-bold mb-3">{{ num_profesores }}</h2>
              <a href="{% url 'profesores' %}" class="btn btn-outline-success btn-sm">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card bg-white shadow-sm" style="border: 1px solid #000;">
            <div class="card-header bg-white fw-bold text-success-custom border-bottom" style="border-color: #000 !important;">Grupos Creados</div>
            <div class="card-body">
              <h2 class="card-title text-dark fw-bold mb-3">{{ num_grupos }}</h2>
              <a href="{% url 'grupos' %}" class="btn btn-outline-success btn-sm">Ver Lista</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card bg-white shadow-sm" style="border: 1px solid #000;">
            <div class="card-header bg-white fw-bold text-success-custom border-bottom" style="border-color: #000 !important;">Carreras Ofertadas</div>
            <div class="card-body">
              <h2 class="card-title text-dark fw-bold mb-3">{{ num_carreras }}</h2>
              <a href="{% url 'carreras' %}" class="btn btn-outline-success btn-sm">Ver Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home)


# 3. Create Lists (Removing Edit button, green links and titles)
def write_list(name, title, btn_url, headers, row_html):
    content = f"""{{% extends "pagina_maestra.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h2 class="text-success-custom fw-bold">{title}</h2>
    <a href="{{% url '{btn_url}' %}}" class="btn btn-success"><i class="bi bi-plus-circle me-1"></i> Agregar Nuevo</a>
</div>
<div class="table-responsive bg-white rounded shadow-sm p-2">
    <table class="table table-hover align-middle mb-0">
        <thead class="table-success">
            <tr>
                {headers}
                <th class="text-center">Operaciones</th>
            </tr>
        </thead>
        <tbody>
            {{% for item in object_list %}}
            <tr>
                {row_html}
            </tr>
            {{% empty %}}
            <tr>
                <td colspan="100%" class="text-center py-4 text-muted">No hay registros disponibles.</td>
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
    """<td><a href="{{ item.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ item.matricula }}</a></td>
       <td>{{ item.apellidos }} {{ item.nombre }}</td>
       <td>{{ item.carrera.codigo }}</td>
       <td>{{ item.get_estatus_display }}</td>
       <td>{{ item.semestre }}</td>
       <td><span class="badge text-bg-light border">{{ item.promedio|floatformat:2|default:"N/A" }}</span></td>
       <td class="text-center">
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info text-white" title="Ver detalle"><i class="bi bi-eye"></i> Ver detalle</a>
           <a href="{% url 'alumno-delete' item.matricula %}" class="btn btn-sm btn-outline-danger ms-1" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('profesor', 'Lista de Profesores', 'profesor-create',
    '<th>No. Empleado</th><th>Nombre Completo</th><th>Especialidad</th><th>Correo</th>',
    """<td><a href="{{ item.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ item.numero_empleado }}</a></td>
       <td>{{ item.apellidos }} {{ item.nombre }}</td>
       <td>{{ item.especialidad }}</td>
       <td>{{ item.email }}</td>
       <td class="text-center">
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info text-white" title="Ver detalle"><i class="bi bi-eye"></i> Ver detalle</a>
           <a href="{% url 'profesor-delete' item.numero_empleado %}" class="btn btn-sm btn-outline-danger ms-1" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('carrera', 'Lista de Carreras', 'carrera-create',
    '<th>Código</th><th>Nombre de Carrera</th><th>Créditos</th><th>Semestres</th>',
    """<td><a href="{{ item.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ item.codigo }}</a></td>
       <td>{{ item.nombre }}</td>
       <td>{{ item.creditos }}</td>
       <td>{{ item.duracion }}</td>
       <td class="text-center">
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info text-white" title="Ver detalle"><i class="bi bi-eye"></i> Ver detalle</a>
           <a href="{% url 'carrera-delete' item.id %}" class="btn btn-sm btn-outline-danger ms-1" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('materia', 'Lista de Materias', 'materia-create',
    '<th>Código</th><th>Materia</th><th>Carrera</th><th>Créditos</th>',
    """<td><a href="{{ item.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ item.codigo }}</a></td>
       <td>{{ item.nombre }}</td>
       <td>{{ item.carrera.nombre }}</td>
       <td>{{ item.creditos }}</td>
       <td class="text-center">
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info text-white" title="Ver detalle"><i class="bi bi-eye"></i> Ver detalle</a>
           <a href="{% url 'materia-delete' item.id %}" class="btn btn-sm btn-outline-danger ms-1" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")

write_list('grupo', 'Lista de Grupos', 'grupo-create',
    '<th>Clave</th><th>Materia</th><th>Profesor</th><th>Horario</th><th>Alumnos</th>',
    """<td><a href="{{ item.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ item.clave }}</a></td>
       <td>{{ item.materia.nombre }}</td>
       <td>{{ item.profesor|default:"Sin asignar" }}</td>
       <td>{{ item.horario }}</td>
       <td>{{ item.numAlumnos }} / {{ item.cupo }}</td>
       <td class="text-center">
           <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-info text-white" title="Ver detalle"><i class="bi bi-eye"></i> Ver detalle</a>
           <a href="{% url 'grupo-delete' item.id %}" class="btn btn-sm btn-outline-danger ms-1" title="Eliminar"><i class="bi bi-trash"></i></a>
       </td>""")


# 4. Details (Green headers, removed 'Regresar a la lista', green object names, single download report button)
alumno_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle del Alumno{% endblock %}
{% block content %}
<div class="card mb-4 shadow-sm">
    <div class="card-header bg-success text-white">
        <h4 class="mb-0"><i class="bi bi-person-badge me-2"></i> {{ object.apellidos }} {{ object.nombre }}</h4>
    </div>
    <div class="card-body row">
        <div class="col-md-6">
            <p><strong>Matrícula:</strong> {{ object.matricula }}</p>
            <p><strong>Carrera:</strong> <a href="{{ object.carrera.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ object.carrera.nombre }}</a></p>
        </div>
        <div class="col-md-6">
            <p><strong>Estatus:</strong> {{ object.get_estatus_display }}</p>
            <p><strong>Semestre:</strong> {{ object.semestre }}</p>
        </div>
    </div>
    <div class="card-footer bg-white">
        <a href="{% url 'alumno-update' object.matricula %}" class="btn btn-warning btn-sm"><i class="bi bi-pencil me-1"></i> Editar</a>
    </div>
</div>

<div class="d-flex justify-content-between align-items-center mt-4 mb-3">
    <h4 class="text-success-custom fw-bold mb-0">Kardex / Calificaciones</h4>
    <a href="{% url 'alumno-exportar-kardex' object.matricula %}" class="btn btn-success btn-sm">
        <i class="bi bi-file-earmark-excel-fill me-1"></i> Descargar reporte
    </a>
</div>

<div class="table-responsive bg-white rounded shadow-sm p-2">
    <table class="table table-bordered table-hover align-middle mb-0">
        <thead class="table-success">
            <tr>
                <th>Código</th>
                <th>Materia</th>
                <th>Grupo</th>
                <th>Profesor</th>
                <th>Calificación Final</th>
                <th>Estatus</th>
            </tr>
        </thead>
        <tbody>
            {% for cal in calificaciones %}
            <tr>
                <td>{{ cal.grupo.materia.codigo }}</td>
                <td><a href="{{ cal.grupo.materia.get_absolute_url }}" class="text-success-custom text-decoration-none fw-bold">{{ cal.grupo.materia.nombre }}</a></td>
                <td><a href="{{ cal.grupo.get_absolute_url }}" class="text-success-custom text-decoration-none">{{ cal.grupo.clave }}</a></td>
                <td>
                    {% if cal.grupo.profesor %}
                        <a href="{{ cal.grupo.profesor.get_absolute_url }}" class="text-success-custom text-decoration-none">{{ cal.grupo.profesor }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td>
                    {% if cal.calificacion_final %}
                        {% if cal.calificacion_final < 70 %}
                            <span class="text-danger fw-bold">{{ cal.calificacion_final }}</span>
                        {% else %}
                            <span class="text-success-custom fw-bold">{{ cal.calificacion_final }}</span>
                        {% endif %}
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td>
                    {% if cal.calificacion_final %}
                        {% if cal.calificacion_final >= 70 %}
                            <span class="badge text-bg-success">Aprobado</span>
                        {% else %}
                            <span class="badge text-bg-danger">Reprobado</span>
                        {% endif %}
                    {% else %}
                        <span class="badge text-bg-secondary">Cursando</span>
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" class="text-center py-3">El alumno no cuenta con calificaciones registradas.</td>
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
<div class="card mb-4 shadow-sm">
    <div class="card-header bg-success text-white">
        <h4 class="mb-0"><i class="bi bi-person-video3 me-2"></i> Prof. {{ object.nombre }} {{ object.apellidos }}</h4>
    </div>
    <div class="card-body row">
        <div class="col-md-6">
            <p><strong>Número de Empleado:</strong> {{ object.numero_empleado }}</p>
            <p><strong>Correo Electrónico:</strong> <a href="mailto:{{ object.email }}" class="text-success-custom">{{ object.email }}</a></p>
        </div>
        <div class="col-md-6">
            <p><strong>Especialidad:</strong> {{ object.especialidad }}</p>
        </div>
    </div>
    <div class="card-footer bg-white">
        <a href="{% url 'profesor-update' object.numero_empleado %}" class="btn btn-warning btn-sm"><i class="bi bi-pencil me-1"></i> Editar</a>
    </div>
</div>

<h4 class="text-success-custom fw-bold mt-4 mb-3">Grupos Asignados</h4>
<div class="table-responsive bg-white rounded shadow-sm p-2">
    <table class="table table-bordered table-hover align-middle mb-0">
        <thead class="table-success">
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
                <td><a href="{{ grupo.materia.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ grupo.materia.nombre }}</a></td>
                <td><a href="{{ grupo.get_absolute_url }}" class="text-success-custom text-decoration-none">{{ grupo.clave }}</a></td>
                <td>{{ grupo.horario }}</td>
                <td>{{ grupo.numAlumnos }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center py-3">El profesor no tiene grupos asignados.</td>
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
<div class="card mb-4 shadow-sm">
    <div class="card-header bg-success text-white">
        <h4 class="mb-0"><i class="bi bi-building me-2"></i> {{ object.nombre }} ({{ object.codigo }})</h4>
    </div>
    <div class="card-body">
        <p><strong>Créditos Totales:</strong> {{ object.creditos }}</p>
        <p><strong>Duración (Semestres):</strong> {{ object.duracion }}</p>
    </div>
    <div class="card-footer bg-white">
        <a href="{% url 'carrera-update' object.id %}" class="btn btn-warning btn-sm"><i class="bi bi-pencil me-1"></i> Editar</a>
    </div>
</div>

<h4 class="text-success-custom fw-bold mt-4 mb-3">Mapa Curricular (Materias)</h4>
<div class="list-group bg-white shadow-sm">
    {% for mat in object.materias.all %}
        <a href="{{ mat.get_absolute_url }}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <span class="text-success-custom fw-bold">{{ mat.codigo }} - {{ mat.nombre }}</span>
            <span class="badge bg-success rounded-pill">{{ mat.creditos }} créditos</span>
        </a>
    {% empty %}
        <div class="list-group-item text-muted text-center">No hay materias registradas para esta carrera.</div>
    {% endfor %}
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'carrera_detail.html'), 'w', encoding='utf-8') as f:
    f.write(carrera_detail)

materia_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle de Materia{% endblock %}
{% block content %}
<div class="card mb-4 shadow-sm">
    <div class="card-header bg-success text-white">
        <h4 class="mb-0"><i class="bi bi-book me-2"></i> {{ object.nombre }} ({{ object.codigo }})</h4>
    </div>
    <div class="card-body">
        <p><strong>Carrera:</strong> <a href="{{ object.carrera.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ object.carrera.nombre }}</a></p>
        <p><strong>Unidades:</strong> {{ object.unidades }}</p>
        <p><strong>Créditos:</strong> {{ object.creditos }}</p>
    </div>
    <div class="card-footer bg-white">
        <a href="{% url 'materia-update' object.id %}" class="btn btn-warning btn-sm"><i class="bi bi-pencil me-1"></i> Editar</a>
    </div>
</div>

<h4 class="text-success-custom fw-bold mt-4 mb-3">Grupos Abiertos</h4>
<div class="list-group bg-white shadow-sm">
    {% for g in object.grupos.all %}
        <a href="{{ g.get_absolute_url }}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <div>
                <strong class="text-success-custom">Grupo {{ g.clave }}</strong> - Prof. {{ g.profesor|default:"Sin asignar" }}
                <div class="small text-muted">Horario: {{ g.horario }}</div>
            </div>
            <span class="badge bg-secondary rounded-pill">Inscritos: {{ g.numAlumnos }}/{{ g.cupo }}</span>
        </a>
    {% empty %}
        <div class="list-group-item text-muted text-center">No hay grupos aperturados para esta materia.</div>
    {% endfor %}
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'materia_detail.html'), 'w', encoding='utf-8') as f:
    f.write(materia_detail)

grupo_detail = """{% extends "pagina_maestra.html" %}
{% block title %}Detalle del Grupo{% endblock %}
{% block content %}
<div class="card mb-4 shadow-sm">
    <div class="card-header bg-success text-white">
        <h4 class="mb-0"><i class="bi bi-people-fill me-2"></i> Grupo {{ object.clave }} - {{ object.materia.nombre }}</h4>
    </div>
    <div class="card-body">
        <p><strong>Profesor:</strong> {% if object.profesor %}<a href="{{ object.profesor.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ object.profesor }}</a>{% else %}Sin asignar{% endif %}</p>
        <p><strong>Horario:</strong> {{ object.horario }}</p>
        <p><strong>Cupo:</strong> {{ object.numAlumnos }} / {{ object.cupo }} inscritos</p>
    </div>
    <div class="card-footer bg-white">
        <a href="{% url 'grupo-update' object.id %}" class="btn btn-warning btn-sm"><i class="bi bi-pencil me-1"></i> Editar</a>
    </div>
</div>

<h4 class="text-success-custom fw-bold mt-4 mb-3">Alumnos Inscritos</h4>
<div class="table-responsive bg-white rounded shadow-sm p-2">
    <table class="table table-bordered table-hover align-middle mb-0">
        <thead class="table-success">
            <tr>
                <th>Matrícula</th>
                <th>Nombre del Alumno</th>
                <th>Calificación Final</th>
            </tr>
        </thead>
        <tbody>
            {% for calif in object.calificacion_set.all %}
            <tr>
                <td><a href="{{ calif.alumno.get_absolute_url }}" class="text-success-custom fw-bold text-decoration-none">{{ calif.alumno.matricula }}</a></td>
                <td>{{ calif.alumno.apellidos }} {{ calif.alumno.nombre }}</td>
                <td>
                    {% if calif.calificacion_final %}
                        {% if calif.calificacion_final < 70 %}
                            <span class="text-danger fw-bold">{{ calif.calificacion_final }}</span>
                        {% else %}
                            <span class="text-success-custom fw-bold">{{ calif.calificacion_final }}</span>
                        {% endif %}
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="3" class="text-center py-3">No hay alumnos inscritos en este grupo.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}"""
with open(os.path.join(catalog_templates_dir, 'grupo_detail.html'), 'w', encoding='utf-8') as f:
    f.write(grupo_detail)

print("Rediseño visual aplicado con éxito.")
