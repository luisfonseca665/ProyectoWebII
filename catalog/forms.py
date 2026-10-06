from django import forms
from django.contrib.auth.models import User, Group
from .models import Carrera, Materia, Alumno, Profesor, Grupo, Perfil


class RegistroUsuarioForm(forms.ModelForm):
    rol = forms.ChoiceField(
        choices=[('Administrador', 'Control Escolar (Administrador)'), ('Coordinador', 'Coordinador')],
        required=True, 
        label="Rol a asignar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=True, 
        label="Contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            rol_name = self.cleaned_data['rol']
            # Crear perfil
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.rol = rol_name
            perfil.save()
            # Asignar grupo de django
            grupo, _ = Group.objects.get_or_create(name=rol_name)
            user.groups.add(grupo)
        return user


class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['codigo', 'nombre', 'creditos', 'duracion']
        labels = {
            'codigo': 'Código / Clave',
            'nombre': 'Nombre de la Carrera',
            'creditos': 'Total de Créditos',
            'duracion': 'Duración (Semestres)',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ISC'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ingeniería en Sistemas Computacionales'}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 14}),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['carrera', 'codigo', 'nombre', 'unidades', 'creditos']
        labels = {
            'carrera': 'Carrera',
            'codigo': 'Código de la Materia',
            'nombre': 'Nombre de la Materia',
            'unidades': 'Número de Unidades',
            'creditos': 'Créditos',
        }
        widgets = {
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. AED-1026'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Estructura de Datos'}),
            'unidades': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class ProfesorCreateForm(forms.ModelForm):
    """Formulario para dar de alta un profesor. Omite el usuario y estatus, asignándolos automáticamente."""
    class Meta:
        model = Profesor
        fields = ['numero_empleado', 'nombre', 'apellidos', 'email', 'especialidad']
        labels = {
            'numero_empleado': 'Número de Empleado',
            'nombre': 'Nombre(s)',
            'apellidos': 'Apellidos',
            'email': 'Correo Institucional',
            'especialidad': 'Especialidad / Departamento',
        }
        widgets = {
            'numero_empleado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. EMP-010'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@itsur.edu.mx'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ciencias Básicas'}),
        }


class ProfesorUpdateForm(forms.ModelForm):
    """Formulario para editar un profesor. El número de empleado no se modifica para preservar integridad."""
    numero_empleado = forms.CharField(
        label="Número de Empleado",
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light'})
    )

    class Meta:
        model = Profesor
        fields = ['numero_empleado', 'nombre', 'apellidos', 'email', 'especialidad', 'estatus']
        labels = {
            'nombre': 'Nombre(s)',
            'apellidos': 'Apellidos',
            'email': 'Correo Institucional',
            'especialidad': 'Especialidad / Departamento',
            'estatus': 'Estatus',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-select'}),
        }


class AlumnoCleanMixin:
    def clean(self):
        cleaned_data = super().clean()
        semestre = cleaned_data.get('semestre')
        carrera = cleaned_data.get('carrera')

        if semestre and carrera:
            if semestre < 1:
                self.add_error('semestre', 'El semestre no puede ser menor a 1.')
            elif semestre > carrera.duracion:
                self.add_error('semestre', f'El semestre no puede superar la duración máxima de la carrera ({carrera.duracion} semestres).')
        
        return cleaned_data


class AlumnoCreateForm(AlumnoCleanMixin, forms.ModelForm):
    """Formulario para dar de alta un alumno. Omite el usuario y estatus, asignándolos automáticamente."""
    class Meta:
        model = Alumno
        fields = ['matricula', 'carrera', 'nombre', 'apellidos', 'semestre']
        labels = {
            'matricula': 'Matrícula',
            'carrera': 'Carrera',
            'nombre': 'Nombre(s)',
            'apellidos': 'Apellidos',
            'semestre': 'Semestre',
        }
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 23ISC099'}),
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 14}),
        }


class AlumnoUpdateForm(AlumnoCleanMixin, forms.ModelForm):
    """Formulario para editar un alumno. La matrícula no se modifica para preservar integridad."""
    matricula = forms.CharField(
        label="Matrícula",
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light'})
    )

    class Meta:
        model = Alumno
        fields = ['matricula', 'carrera', 'nombre', 'apellidos', 'semestre', 'estatus']
        labels = {
            'carrera': 'Carrera',
            'nombre': 'Nombre(s)',
            'apellidos': 'Apellidos',
            'semestre': 'Semestre',
            'estatus': 'Estatus',
        }
        widgets = {
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 14}),
            'estatus': forms.Select(attrs={'class': 'form-select'}),
        }


class GrupoMultiForm(forms.Form):
    """Nos ayuda a registrar un grupo nuevo asignándole varias materias al mismo tiempo."""
    clave = forms.CharField(
        label="Clave del Grupo (Ej. 1A)",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1A'})
    )
    cupo = forms.IntegerField(
        label="Cupo Máximo",
        min_value=1,
        initial=35,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    materias = forms.ModelMultipleChoiceField(
        label="Selecciona las Materias para este grupo",
        queryset=Materia.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text="Selecciona las casillas de todas las materias que formarán parte de este grupo."
    )

class GrupoForm(forms.ModelForm):
    """Formulario clásico para editar los detalles de una materia dentro de un grupo (profesor, horario, etc)."""
    class Meta:
        model = Grupo
        fields = ['materia', 'profesor', 'clave', 'cupo', 'horario']
        labels = {
            'materia': 'Materia',
            'profesor': 'Profesor Asignado',
            'clave': 'Clave del Grupo',
            'cupo': 'Cupo Máximo',
            'horario': 'Horario de Clase',
        }
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-select'}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 701-A'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'horario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Lun-Mie-Vie 10:00-12:00'}),
        }
