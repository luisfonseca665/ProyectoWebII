import os

base_dir = r"c:\Users\garci\Documentos\ITSUR\7 Semestre\Programacion Web II\ProyectoWebII\catalog"
templates_dir = os.path.join(base_dir, 'templates')
catalog_templates_dir = os.path.join(templates_dir, 'catalog')

# 1. Update views.py to add `actualizar_calificaciones`
views_path = os.path.join(base_dir, 'views.py')
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

if 'def actualizar_calificaciones' not in views_content:
    imports_to_add = "import json\nfrom django.http import JsonResponse\nfrom django.views.decorators.csrf import csrf_exempt\nfrom django.views.decorators.http import require_POST\nfrom django.core.exceptions import ValidationError\n"
    views_content = imports_to_add + views_content

    new_view = """
@require_POST
def actualizar_calificaciones(request, pk):
    try:
        data = json.loads(request.body)
        alumno = get_object_or_404(Alumno, pk=pk)
        calificaciones = data.get('calificaciones', [])
        
        for item in calificaciones:
            calif_id = item.get('id')
            nueva_calificacion = item.get('calificacion')
            
            # Validation
            if nueva_calificacion is None or nueva_calificacion == '':
                return JsonResponse({'success': False, 'error': 'La calificación no puede ser nula o vacía.'}, status=400)
            
            nueva_calificacion = float(nueva_calificacion)
            if nueva_calificacion < 0 or nueva_calificacion > 100:
                return JsonResponse({'success': False, 'error': 'La calificación debe estar entre 0 y 100.'}, status=400)
                
            calificacion_obj = Calificacion.objects.get(id=calif_id, alumno=alumno)
            calificacion_obj.calificacion_final = nueva_calificacion
            calificacion_obj.save()
            
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
"""
    views_content += new_view
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(views_content)

# 2. Update urls.py to add `actualizar_calificaciones`
urls_path = os.path.join(base_dir, 'urls.py')
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

if 'actualizar-calificaciones' not in urls_content:
    urls_content = urls_content.replace(
        "path('alumnos/<str:pk>/exportar-kardex/', views.exportar_kardex_excel, name='alumno-exportar-kardex'),",
        "path('alumnos/<str:pk>/exportar-kardex/', views.exportar_kardex_excel, name='alumno-exportar-kardex'),\n    path('alumnos/<str:pk>/actualizar-calificaciones/', views.actualizar_calificaciones, name='alumno-actualizar-calificaciones'),"
    )
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)

# 3. Update alumno_detail.html
alumno_detail_path = os.path.join(catalog_templates_dir, 'alumno_detail.html')
alumno_detail_content = """{% extends "pagina_maestra.html" %}
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
    <div>
        <button id="btn-edit-kardex" class="btn btn-warning btn-sm me-2"><i class="bi bi-pencil me-1"></i> Editar Kardex</button>
        <button id="btn-save-kardex" class="btn btn-primary btn-sm me-2 d-none"><i class="bi bi-save me-1"></i> Guardar</button>
        <button id="btn-cancel-kardex" class="btn btn-secondary btn-sm me-2 d-none"><i class="bi bi-x me-1"></i> Cancelar</button>
        <a href="{% url 'alumno-exportar-kardex' object.matricula %}" class="btn btn-success btn-sm">
            <i class="bi bi-file-earmark-excel-fill me-1"></i> Descargar reporte
        </a>
    </div>
</div>

<div class="table-responsive bg-white rounded shadow-sm p-2">
    <!-- Notice we omit datatable class here to avoid conflicts with inline editing inputs in this specific table -->
    <table class="table table-bordered table-hover align-middle mb-0" id="kardex-table">
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
            <tr data-calificacion-id="{{ cal.id }}">
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
                <td class="grade-cell" data-original-grade="{{ cal.calificacion_final|default:'' }}">
                    {% if cal.calificacion_final %}
                        {% if cal.calificacion_final < 70 %}
                            <span class="text-danger fw-bold grade-text">{{ cal.calificacion_final }}</span>
                        {% else %}
                            <span class="text-success-custom fw-bold grade-text">{{ cal.calificacion_final }}</span>
                        {% endif %}
                    {% else %}
                        <span class="grade-text">-</span>
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

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const btnEdit = document.getElementById("btn-edit-kardex");
        const btnSave = document.getElementById("btn-save-kardex");
        const btnCancel = document.getElementById("btn-cancel-kardex");
        const gradeCells = document.querySelectorAll(".grade-cell");

        function getCSRFToken() {
            let cookieValue = null;
            const name = 'csrftoken';
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        btnEdit.addEventListener("click", function() {
            btnEdit.classList.add("d-none");
            btnSave.classList.remove("d-none");
            btnCancel.classList.remove("d-none");

            gradeCells.forEach(cell => {
                const originalGrade = cell.getAttribute("data-original-grade");
                const textSpan = cell.querySelector(".grade-text");
                if (textSpan) textSpan.classList.add("d-none");
                
                let input = cell.querySelector(".grade-input");
                if (!input) {
                    input = document.createElement("input");
                    input.type = "number";
                    input.min = "0";
                    input.max = "100";
                    input.step = "0.01";
                    input.className = "form-control grade-input";
                    input.value = originalGrade;
                    cell.appendChild(input);
                } else {
                    input.classList.remove("d-none");
                }
            });
        });

        btnCancel.addEventListener("click", function() {
            btnSave.classList.add("d-none");
            btnCancel.classList.add("d-none");
            btnEdit.classList.remove("d-none");

            gradeCells.forEach(cell => {
                const textSpan = cell.querySelector(".grade-text");
                const input = cell.querySelector(".grade-input");
                
                if (input) input.classList.add("d-none");
                if (textSpan) textSpan.classList.remove("d-none");
            });
        });

        btnSave.addEventListener("click", function() {
            const updates = [];
            let hasError = false;

            gradeCells.forEach(cell => {
                const row = cell.closest("tr");
                const califId = row.getAttribute("data-calificacion-id");
                const input = cell.querySelector(".grade-input");
                
                if (input) {
                    const val = input.value;
                    if (val === "" || val < 0 || val > 100) {
                        hasError = true;
                        input.classList.add("is-invalid");
                    } else {
                        input.classList.remove("is-invalid");
                        updates.push({ id: califId, calificacion: val });
                    }
                }
            });

            if (hasError) {
                alert("Por favor, asegúrese de que todas las calificaciones estén entre 0 y 100, y no estén vacías.");
                return;
            }

            fetch("{% url 'alumno-actualizar-calificaciones' object.matricula %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ calificaciones: updates })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Recargar la página para reflejar los cambios
                    window.location.reload();
                } else {
                    alert("Hubo un error al guardar: " + data.error);
                }
            })
            .catch(error => {
                alert("Error de red al intentar guardar.");
            });
        });
    });
</script>
{% endblock %}"""
with open(alumno_detail_path, 'w', encoding='utf-8') as f:
    f.write(alumno_detail_content)

print("Kardex inline editing implemented successfully.")
