import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import Carrera, Materia, Alumno, Profesor, Grupo, Calificacion, Perfil
from django.db.models import Avg, Count, Sum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import (
    RegistroUsuarioForm, CarreraForm, MateriaForm,
    ProfesorCreateForm, ProfesorUpdateForm,
    AlumnoCreateForm, AlumnoUpdateForm, GrupoForm, GrupoMultiForm,
    CambiarPasswordAlumnoForm
)
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# --- MIXINS DE ROLES ---
# Estos "mixins" son como los guardias de seguridad: revisan qué rol tienes antes 
# de dejarte entrar a una vista. Si no tienes permisos, te regresan.
# Hemos optimizado esta parte para dejar de usar los Grupos Nativos de Django 
# y usar directamente nuestro modelo Perfil, lo cual hace el código más ligero y directo.
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'CONTROL_ESCOLAR')

class CoordinadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'COORDINADOR')

class AdminOrCoordinadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol in ['CONTROL_ESCOLAR', 'COORDINADOR'])

class EstudianteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return hasattr(user, 'perfil') and user.perfil.rol == 'ALUMNO'

class ProfesorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'PROFESOR')

# --- VISTAS EN GENERAL ---

class HomeView(LoginRequiredMixin, TemplateView):
    """
    La pantalla principal del sistema. Aquí nada más sacamos la cuenta total 
    de alumnos, profes, grupos y demás para mostrarlos en las tarjetitas del inicio.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_alumnos'] = Alumno.objects.count()
        context['num_profesores'] = Profesor.objects.count()
        context['num_grupos'] = Grupo.objects.count()
        context['num_carreras'] = Carrera.objects.count()
        context['num_materias'] = Materia.objects.count()
        return context

# SINCRONIZACIÓN AUTOMÁTICA DE USUARIOS
# Estas funciones nos ayudan a que cuando creemos un profesor o alumno en el sistema,
# automáticamente se le cree su cuenta de Django (User) por debajo para que puedan iniciar sesión.
def sincronizar_usuario_profesor(profesor):
    username = profesor.numero_empleado.lower()
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': profesor.nombre,
        'last_name': profesor.apellidos,
        'email': profesor.email,
    })
    if created:
        user.set_password('Profesor123!')
        user.save()
    else:
        user.first_name = profesor.nombre
        user.last_name = profesor.apellidos
        user.email = profesor.email
        user.save()
    
    perfil, _ = Perfil.objects.get_or_create(usuario=user)
    perfil.rol = 'PROFESOR'
    perfil.save()
    
    if profesor.usuario != user:
        profesor.usuario = user
        profesor.save(update_fields=['usuario'])

def sincronizar_usuario_alumno(alumno):
    username = alumno.matricula.lower()
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': alumno.nombre,
        'last_name': alumno.apellidos,
    })
    if created:
        user.set_password(alumno.matricula)
        user.save()
    else:
        user.first_name = alumno.nombre
        user.last_name = alumno.apellidos
        user.save()
    
    perfil, _ = Perfil.objects.get_or_create(usuario=user)
    perfil.rol = 'ALUMNO'
    perfil.save()
    
    if alumno.usuario != user:
        alumno.usuario = user
        alumno.save(update_fields=['usuario'])

# --- CARRERA ---
class CarreraListView(LoginRequiredMixin, ListView):
    model = Carrera
    template_name = 'carrera_list.html'

class CarreraDetailView(LoginRequiredMixin, DetailView):
    model = Carrera
    template_name = 'catalog/carrera_detail.html'

class CarreraCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'form_generico.html'
    success_url = reverse_lazy('carreras')

    def form_valid(self, form):
        messages.success(self.request, f"Carrera '{form.instance.nombre}' creada exitosamente.")
        return super().form_valid(form)

class CarreraUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'form_generico.html'

    def get_success_url(self):
        return reverse_lazy('carrera-detail', args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, f"Carrera '{form.instance.nombre}' actualizada exitosamente.")
        return super().form_valid(form)

class CarreraDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Carrera
    success_url = reverse_lazy('carreras')
    template_name = 'confirm_delete.html'

# --- MATERIA ---
class MateriaListView(LoginRequiredMixin, ListView):
    model = Materia
    template_name = 'materia_list.html'

class MateriaDetailView(LoginRequiredMixin, DetailView):
    model = Materia
    template_name = 'catalog/materia_detail.html'

class MateriaCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'form_generico.html'
    success_url = reverse_lazy('materias')

    def form_valid(self, form):
        messages.success(self.request, f"Materia '{form.instance.nombre}' creada exitosamente.")
        return super().form_valid(form)

class MateriaUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'form_generico.html'

    def get_success_url(self):
        return reverse_lazy('materia-detail', args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, f"Materia '{form.instance.nombre}' actualizada exitosamente.")
        return super().form_valid(form)

class MateriaDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Materia
    success_url = reverse_lazy('materias')
    template_name = 'confirm_delete.html'

# --- ALUMNO ---
class AlumnoListView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = 'alumno_list.html'
    def get_queryset(self):
        return Alumno.objects.annotate(promedio=Avg('calificacion__calificacion_final'))

class AlumnoDetailView(LoginRequiredMixin, DetailView): 
    model = Alumno
    template_name = 'catalog/alumno_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calificaciones'] = Calificacion.objects.filter(alumno=self.object).select_related('grupo__materia', 'grupo__profesor')
        return context

class AlumnoCreateView(LoginRequiredMixin, AdminOrCoordinadorRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoCreateForm
    template_name = 'form_generico.html'
    success_url = reverse_lazy('alumnos')

    def form_valid(self, form):
        form.instance.estatus = 'A'
        response = super().form_valid(form)
        sincronizar_usuario_alumno(self.object)
        messages.success(self.request, f"Alumno '{self.object.nombre} {self.object.apellidos}' ({self.object.matricula}) registrado como Activo exitosamente.")
        return response

class AlumnoUpdateView(LoginRequiredMixin, AdminOrCoordinadorRequiredMixin, UpdateView):
    model = Alumno
    form_class = AlumnoUpdateForm
    template_name = 'form_generico.html'

    def get_success_url(self):
        return reverse_lazy('alumno-detail', args=[self.object.matricula])

    def form_valid(self, form):
        response = super().form_valid(form)
        sincronizar_usuario_alumno(self.object)
        messages.success(self.request, f"Alumno '{self.object.nombre} {self.object.apellidos}' actualizado exitosamente.")
        return response

class AlumnoDeleteView(LoginRequiredMixin, AdminOrCoordinadorRequiredMixin, DeleteView):
    model = Alumno
    success_url = reverse_lazy('alumnos')
    template_name = 'confirm_delete.html'

class CambiarPasswordAlumnoView(LoginRequiredMixin, AdminRequiredMixin, FormView):
    """
    Vista para que Control Escolar (Administrador) le cambie la contraseña a un alumno.
    """
    template_name = 'form_generico.html'
    form_class = CambiarPasswordAlumnoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Hack para mostrar el título en form_generico
        ctx['form'].instance = get_object_or_404(Alumno, matricula=self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        alumno = get_object_or_404(Alumno, matricula=self.kwargs['pk'])
        nueva_pass = form.cleaned_data['nueva_password']
        if alumno.usuario:
            alumno.usuario.set_password(nueva_pass)
            alumno.usuario.save()
            messages.success(self.request, f"Contraseña actualizada para {alumno.matricula}.")
        else:
            messages.error(self.request, "El alumno no tiene un usuario asignado.")
        return redirect('alumno-detail', pk=alumno.matricula)

# --- PROFESOR ---
class ProfesorListView(LoginRequiredMixin, ListView):
    model = Profesor
    template_name = 'profesor_list.html'

class ProfesorDetailView(LoginRequiredMixin, DetailView):
    model = Profesor
    template_name = 'catalog/profesor_detail.html'

class ProfesorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Profesor
    form_class = ProfesorCreateForm
    template_name = 'form_generico.html'
    success_url = reverse_lazy('profesores')

    def form_valid(self, form):
        form.instance.estatus = 'A'
        response = super().form_valid(form)
        sincronizar_usuario_profesor(self.object)
        messages.success(self.request, f"Profesor '{self.object.nombre} {self.object.apellidos}' ({self.object.numero_empleado}) registrado como Activo exitosamente.")
        return response

class ProfesorUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Profesor
    form_class = ProfesorUpdateForm
    template_name = 'form_generico.html'

    def get_success_url(self):
        return reverse_lazy('profesor-detail', args=[self.object.numero_empleado])

    def form_valid(self, form):
        response = super().form_valid(form)
        sincronizar_usuario_profesor(self.object)
        messages.success(self.request, f"Profesor '{self.object.nombre} {self.object.apellidos}' actualizado exitosamente.")
        return response

class ProfesorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Profesor
    success_url = reverse_lazy('profesores')
    template_name = 'confirm_delete.html'

# --- GRUPO ---
class GrupoListView(LoginRequiredMixin, ListView):
    template_name = 'grupo_list.html'
    context_object_name = 'grupos_agrupados'

    def get_queryset(self):
        claves = Grupo.objects.filter(activo=True).values('clave').distinct().order_by('clave')
        grupos_agrupados = []
        for c in claves:
            clave = c['clave']
            grupos = Grupo.objects.filter(clave=clave, activo=True)
            cupo = grupos.first().cupo if grupos.exists() else 0
            grupos_agrupados.append({
                'clave': clave,
                'cupo': cupo,
                'num_materias': grupos.count()
            })
        return grupos_agrupados

class GrupoClaveDetailView(LoginRequiredMixin, CoordinadorRequiredMixin, ListView):
    """Muestra todas las materias asociadas a una clave de grupo."""
    template_name = 'grupo_clave_detail.html'
    context_object_name = 'materias_grupo'
    
    def get_queryset(self):
        return Grupo.objects.filter(clave=self.kwargs['clave'], activo=True).select_related('materia', 'profesor')
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['clave'] = self.kwargs['clave']
        return ctx

from django.views.generic.edit import FormView

class GrupoCreateView(LoginRequiredMixin, CoordinadorRequiredMixin, FormView):
    """Permite crear masivamente las materias de una clave de grupo."""
    template_name = 'form_generico.html'
    form_class = GrupoMultiForm
    success_url = reverse_lazy('grupos')

    def form_valid(self, form):
        clave = form.cleaned_data['clave']
        cupo = form.cleaned_data['cupo']
        materias = form.cleaned_data['materias']
        
        for materia in materias:
            Grupo.objects.create(
                clave=clave,
                cupo=cupo,
                materia=materia,
                horario='Por asignar'
            )
            
        messages.success(self.request, f"Se generaron exitosamente {materias.count()} materias para el grupo '{clave}'.")
        return super().form_valid(form)

class GrupoMasivoUpdateView(LoginRequiredMixin, CoordinadorRequiredMixin, FormView):
    """Permite editar masivamente las materias de una clave de grupo."""
    template_name = 'form_generico.html'
    form_class = GrupoMultiForm
    
    def get_initial(self):
        clave = self.kwargs['clave']
        grupos = Grupo.objects.filter(clave=clave)
        initial = {}
        if grupos.exists():
            initial['clave'] = clave
            initial['cupo'] = grupos.first().cupo
            initial['materias'] = grupos.values_list('materia_id', flat=True)
        return initial

    def form_valid(self, form):
        clave_original = self.kwargs['clave']
        nueva_clave = form.cleaned_data['clave']
        nuevo_cupo = form.cleaned_data['cupo']
        nuevas_materias = form.cleaned_data['materias']
        
        grupos_actuales = list(Grupo.objects.filter(clave=clave_original))
        materias_actuales_ids = [g.materia_id for g in grupos_actuales]
        nuevas_materias_ids = [m.id for m in nuevas_materias]
        
        # Actualizar o eliminar existentes
        for grupo in grupos_actuales:
            if grupo.materia_id not in nuevas_materias_ids:
                # Borrado lógico
                grupo.activo = False
                grupo.save()
            else:
                grupo.clave = nueva_clave
                grupo.cupo = nuevo_cupo
                # Si estaba dado de baja y lo vuelven a seleccionar
                grupo.activo = True
                grupo.save()
                
        # Crear nuevas asignaciones
        for materia in nuevas_materias:
            if materia.id not in materias_actuales_ids:
                Grupo.objects.create(
                    clave=nueva_clave,
                    cupo=nuevo_cupo,
                    materia=materia,
                    horario='Por asignar'
                )
        
        messages.success(self.request, f"Grupo '{nueva_clave}' actualizado exitosamente.")
        return redirect('grupos')

class GrupoMasivoDeleteView(LoginRequiredMixin, CoordinadorRequiredMixin, DeleteView):
    """Elimina todos los registros de una clave de grupo."""
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('grupos')

    def get_object(self):
        return Grupo.objects.filter(clave=self.kwargs['clave'], activo=True).first() # Se usa uno para la confirmación genérica

    def form_valid(self, form):
        clave = self.kwargs['clave']
        Grupo.objects.filter(clave=clave).update(activo=False) # Borrado lógico
        messages.success(self.request, f"Grupo '{clave}' y todas sus materias han sido eliminados lógicamente.")
        return redirect(self.success_url)

class GrupoUpdateView(LoginRequiredMixin, CoordinadorRequiredMixin, UpdateView):
    """Actualiza una materia ESPECÍFICA de un grupo (para ponerle Profesor/Horario)"""
    model = Grupo
    form_class = GrupoForm
    template_name = 'form_generico.html'

    def get_success_url(self):
        return reverse_lazy('grupo-clave-detail', args=[self.object.clave])

    def form_valid(self, form):
        messages.success(self.request, f"Materia '{form.instance.materia.nombre}' del grupo '{form.instance.clave}' actualizada exitosamente.")
        return super().form_valid(form)


# - CARGA ACADÉMICA E INSCRIPCIÓN ---

class DarDeBajaMateriaView(LoginRequiredMixin, CoordinadorRequiredMixin, View):
    """
    Permite a un coordinador dar de baja una materia específica del alumno 
    (solo si no ha sido calificada todavía).
    """
    def post(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        matricula = calificacion.alumno.matricula
        
        if calificacion.calificacion_final is None:
            grupo = calificacion.grupo
            calificacion.delete()
            # Actualizar cupo
            grupo.numAlumnos = grupo.calificacion_set.count()
            grupo.save()
            messages.success(request, "La materia ha sido dada de baja correctamente.")
        else:
            messages.error(request, "No se puede dar de baja una materia que ya tiene calificación final.")
            
        return redirect('carga-academica-coordinador', matricula=matricula)

class CargaAcademicaView(LoginRequiredMixin, ListView):
    model = Calificacion
    template_name = 'carga_academica.html'
    context_object_name = 'inscripciones'

    def get_queryset(self):
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol == 'ALUMNO':
            return Calificacion.objects.filter(alumno__usuario=self.request.user, calificacion_final__isnull=True)
        
        matricula = self.kwargs.get('matricula')
        if matricula and (hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol == 'COORDINADOR'):
            return Calificacion.objects.filter(alumno__matricula=matricula, calificacion_final__isnull=True)
        
        return Calificacion.objects.none()

class InscripcionMateriasView(LoginRequiredMixin, TemplateView):
    """
    Esta es de las vistas más importantes. Aquí manejamos cuando un alumno o un coordinador
    intenta armar la carga académica (meter materias). Valida que no se pasen de créditos
    y que no metan materias repetidas o ya pasadas.
    """
    template_name = 'inscripcion.html'

    def dispatch(self, request, *args, **kwargs):
        if (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ALUMNO'):
            self.alumno = get_object_or_404(Alumno, usuario=request.user)

            creditos_actuales = Calificacion.objects.filter(
                alumno=self.alumno, calificacion_final__isnull=True
            ).aggregate(total=Sum('grupo__materia__creditos'))['total'] or 0
            
            if creditos_actuales >= 36:
                messages.warning(request, "Ya alcanzaste el límite de créditos.")
                return redirect('carga-academica')
                
        elif (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'COORDINADOR'):
            matricula = self.kwargs.get('matricula')
            self.alumno = get_object_or_404(Alumno, matricula=matricula)
        else:
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Quitamos de la lista las materias que el alumno ya pasó o que ya tiene metidas este semestre
        materias_bloqueadas = Calificacion.objects.filter(
            alumno=self.alumno
        ).exclude(calificacion_final__lt=70).values_list('grupo__materia_id', flat=True)

        context['grupos_disponibles'] = Grupo.objects.filter(
            materia__carrera=self.alumno.carrera,
            activo=True
        ).exclude(materia_id__in=materias_bloqueadas).select_related('materia', 'profesor')
        
        creditos_actuales = Calificacion.objects.filter(
            alumno=self.alumno, calificacion_final__isnull=True
        ).aggregate(total=Sum('grupo__materia__creditos'))['total'] or 0
        
        context['alumno'] = self.alumno
        context['creditos_actuales'] = creditos_actuales
        context['creditos_disponibles'] = max(0, 36 - creditos_actuales)
        return context

    def post(self, request, *args, **kwargs):
        grupos_ids = request.POST.getlist('grupos')
        if not grupos_ids:
            messages.warning(request, "No seleccionaste ningún grupo.")
            if (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ALUMNO'):
                return redirect('inscripcion-estudiante')
            return redirect('inscripcion-coordinador', matricula=self.alumno.matricula)

        grupos_seleccionados = list(Grupo.objects.filter(id__in=grupos_ids).select_related('materia'))
        
        # Revisamos que no intente inscribir más de un grupo para la misma materia (por ejemplo, dos grupos de matemáticas)
        materias_ids = [g.materia_id for g in grupos_seleccionados]
        if len(materias_ids) != len(set(materias_ids)):
            messages.error(request, "No puedes inscribir más de un grupo para la misma materia.")
            if (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ALUMNO'):
                return redirect('inscripcion-estudiante')
            return redirect('inscripcion-coordinador', matricula=self.alumno.matricula)

        # Calculamos si con estas nuevas materias va a superar su límite de 36 créditos
        creditos_actuales = Calificacion.objects.filter(
            alumno=self.alumno, calificacion_final__isnull=True
        ).aggregate(total=Sum('grupo__materia__creditos'))['total'] or 0
        
        creditos_nuevos = sum(g.materia.creditos for g in grupos_seleccionados)
        creditos_totales = creditos_actuales + creditos_nuevos

        if creditos_totales > 36:
            messages.error(
                request, 
                f"La selección excede el límite máximo de créditos. "
                f"Puedes meter un máximo de {creditos_totales} créditos."
            )
            if (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ALUMNO'):
                return redirect('inscripcion-estudiante')
            return redirect('inscripcion-coordinador', matricula=self.alumno.matricula)

        # Si todo está bien, los vamos inscribiendo siempre y cuando todavía haya cupo en el grupo
        for grupo in grupos_seleccionados:
            if grupo.numAlumnos < grupo.cupo:
                _, created = Calificacion.objects.get_or_create(alumno=self.alumno, grupo=grupo)
                if created:
                    grupo.numAlumnos = grupo.calificacion_set.count()
                    grupo.save()
            else:
                messages.warning(request, f"El grupo {grupo.clave} de {grupo.materia.nombre} ya no cuenta con cupo.")

        messages.success(request, f"Inscripción realizada con éxito. Has registrado {creditos_nuevos} créditos (Total actual: {creditos_totales} créditos).")
        if (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ALUMNO'):
            return redirect('carga-academica')
        return redirect('carga-academica-coordinador', matricula=self.alumno.matricula)

# --- VISTA EXPORTACIÓN EXCEL ---
@login_required
def exportar_kardex_excel(request, pk):
    """
    Toma todas las calificaciones de un alumno y las formatea bonito en un archivo de Excel (.xlsx) 
    para que Control Escolar o los coordinadores puedan descargarlo y tenerlo en físico/digital.
    """
    alumno = get_object_or_404(Alumno, pk=pk)
    # Solo mostrar calificaciones mayor a 0 (ya que con 0 se asume que apenas las está cursando)
    calificaciones = Calificacion.objects.filter(
        alumno=alumno, 
        calificacion_final__gt=0, 
        calificacion_final__isnull=False
    ).select_related('grupo__materia', 'grupo__profesor')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Kardex_{alumno.matricula}"

    font_title = Font(name="Arial", size=14, bold=True, color="1F4E78")
    font_header = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # Title Header
    ws.merge_cells("A1:G1")
    ws["A1"] = "SISTEMA INTEGRAL DE CONTROL ESCOLAR - KARDEX ACADÉMICO"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="center")

    # Info Section
    ws["A3"] = "Matrícula:"
    ws["B3"] = alumno.matricula
    ws["D3"] = "Nombre:"
    ws["E3"] = f"{alumno.apellidos} {alumno.nombre}"

    ws["A4"] = "Carrera:"
    ws["B4"] = alumno.carrera.nombre
    ws["D4"] = "Semestre:"
    ws["E4"] = alumno.semestre

    ws["A5"] = "Estatus:"
    ws["B5"] = alumno.get_estatus_display()

    prom = calificaciones.aggregate(Avg('calificacion_final'))['calificacion_final__avg']
    ws["D5"] = "Promedio General:"
    ws["E5"] = round(float(prom), 2) if prom else "N/A"

    for r in range(3, 6):
        ws[f"A{r}"].font = Font(bold=True)
        ws[f"D{r}"].font = Font(bold=True)

    # Table Header
    headers = ["Código", "Materia", "Créditos", "Clave Grupo", "Profesor", "Calificación Final", "Estatus"]
    row_idx = 7
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    # Data Rows
    for calif in calificaciones:
        row_idx += 1
        materia = calif.grupo.materia
        profesor = str(calif.grupo.profesor) if calif.grupo.profesor else "Sin asignar"
        calif_val = float(calif.calificacion_final) if calif.calificacion_final is not None else 0.0
        estatus_mat = "Aprobado" if calif_val >= 70 else "Reprobado"

        ws.cell(row=row_idx, column=1, value=materia.codigo).alignment = Alignment(horizontal="center")
        ws.cell(row=row_idx, column=2, value=materia.nombre)
        ws.cell(row=row_idx, column=3, value=materia.creditos).alignment = Alignment(horizontal="center")
        ws.cell(row=row_idx, column=4, value=calif.grupo.clave).alignment = Alignment(horizontal="center")
        ws.cell(row=row_idx, column=5, value=profesor)
        
        c_calif = ws.cell(row=row_idx, column=6, value=calif_val)
        c_calif.alignment = Alignment(horizontal="right")
        
        c_est = ws.cell(row=row_idx, column=7, value=estatus_mat)
        c_est.alignment = Alignment(horizontal="center")
        if calif_val >= 70:
            c_est.font = Font(color="006100", bold=True)
        else:
            c_est.font = Font(color="9C0006", bold=True)

        for col in range(1, 8):
            ws.cell(row=row_idx, column=col).border = border_thin

    # Adjust Column Widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Kardex_{alumno.matricula}.xlsx"'
    wb.save(response)
    return response


def es_coordinador(user):
    return user.groups.filter(name='Coordinador').exists() or user.is_superuser

@require_POST
@user_passes_test(es_coordinador)
def actualizar_calificaciones(request, pk):
    """
    Ruta por donde se reciben datos en formato JSON para actualizar calificaciones 
    rápidamente desde alguna tabla. (AJAX/Fetch API).
    """
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

# --- VISTAS EXCLUSIVAS DEL PROFESOR ---
class MisGruposView(LoginRequiredMixin, ProfesorRequiredMixin, ListView):
    """
    Lista todos los grupos que tiene asignado el profesor que inició sesión.
    Básicamente es su pantalla de inicio.
    """
    model = Grupo
    template_name = 'mis_grupos.html'
    context_object_name = 'grupos'

    def get_queryset(self):
        return Grupo.objects.filter(profesor__usuario=self.request.user, activo=True)

class CapturarCalificacionesView(LoginRequiredMixin, ProfesorRequiredMixin, DetailView):
    """
    Aquí es donde el profesor entra a un grupo en específico y le pone 
    las calificaciones de 0 a 100 a todos los alumnos que están inscritos en él.
    """
    model = Grupo
    template_name = 'capturar_calificaciones.html'
    context_object_name = 'grupo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Traemos a los alumnos inscritos ordenados por apellidos
        context['calificaciones'] = Calificacion.objects.filter(grupo=self.object).select_related('alumno').order_by('alumno__apellidos', 'alumno__nombre')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        calificaciones = Calificacion.objects.filter(grupo=self.object)
        
        for calif in calificaciones:
            # El input del html tendrá el name="calificacion_1", "calificacion_2", etc.
            valor = request.POST.get(f'calificacion_{calif.id}')
            if valor:
                calif.calificacion_final = float(valor)
                calif.save()
                
        messages.success(request, f"Calificaciones del grupo {self.object.clave} guardadas exitosamente.")
        return redirect('mis-grupos')



class UsuarioCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'form_generico.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado exitosamente.")
        return super().form_valid(form)