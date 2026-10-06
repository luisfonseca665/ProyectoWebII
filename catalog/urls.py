from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Autenticación
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario-create'),

    path('', views.HomeView.as_view(), name='home'),
    
    # Rutas para la carga academica y la inscripcion
    path('mi-carga/', views.CargaAcademicaView.as_view(), name='carga-academica'),
    path('carga/<str:matricula>/', views.CargaAcademicaView.as_view(), name='carga-academica-coordinador'),
    path('inscripcion/', views.InscripcionMateriasView.as_view(), name='inscripcion-estudiante'),
    path('inscripcion/<str:matricula>/', views.InscripcionMateriasView.as_view(), name='inscripcion-coordinador'),

    # Rutas para las carreras
    path('carreras/', views.CarreraListView.as_view(), name='carreras'),
    path('carreras/nueva/', views.CarreraCreateView.as_view(), name='carrera-create'),
    path('carreras/<int:pk>/', views.CarreraDetailView.as_view(), name='carrera-detail'),
    path('carreras/<int:pk>/editar/', views.CarreraUpdateView.as_view(), name='carrera-update'),
    path('carreras/<int:pk>/eliminar/', views.CarreraDeleteView.as_view(), name='carrera-delete'),

    # Rutas para las materias
    path('materias/', views.MateriaListView.as_view(), name='materias'),
    path('materias/nueva/', views.MateriaCreateView.as_view(), name='materia-create'),
    path('materias/<int:pk>/', views.MateriaDetailView.as_view(), name='materia-detail'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia-update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia-delete'),

    # Rutas para los alumnos
    path('alumnos/', views.AlumnoListView.as_view(), name='alumnos'),
    path('alumnos/nuevo/', views.AlumnoCreateView.as_view(), name='alumno-create'),
    path('alumnos/<str:pk>/', views.AlumnoDetailView.as_view(), name='alumno-detail'),
    path('alumnos/<str:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno-update'),
    path('alumnos/<str:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno-delete'),
    path('alumnos/<str:pk>/exportar-kardex/', views.exportar_kardex_excel, name='alumno-exportar-kardex'),

    # Rutas para los profesores 
    path('profesores/', views.ProfesorListView.as_view(), name='profesores'),
    path('profesores/nuevo/', views.ProfesorCreateView.as_view(), name='profesor-create'),
    path('profesores/<str:pk>/', views.ProfesorDetailView.as_view(), name='profesor-detail'),
    path('profesores/<str:pk>/editar/', views.ProfesorUpdateView.as_view(), name='profesor-update'),
    path('profesores/<str:pk>/eliminar/', views.ProfesorDeleteView.as_view(), name='profesor-delete'),

    # Rutas para los profesores
    path('grupos/', views.GrupoListView.as_view(), name='grupos'),
    path('grupos/nuevo/', views.GrupoCreateView.as_view(), name='grupo-create'),
    path('grupos/<str:clave>/', views.GrupoClaveDetailView.as_view(), name='grupo-clave-detail'),
    path('grupos/<str:clave>/editar-materias/', views.GrupoMasivoUpdateView.as_view(), name='grupo-update-masivo'),
    path('grupos/<str:clave>/eliminar/', views.GrupoMasivoDeleteView.as_view(), name='grupo-delete-masivo'),

    # Rutas para los grupos de los profes 
    path('grupo-materia/<int:pk>/editar/', views.GrupoUpdateView.as_view(), name='grupo-update'),
    path('mis-grupos/', views.MisGruposView.as_view(), name='mis-grupos'),
    path('grupo/<int:pk>/calificaciones/', views.CapturarCalificacionesView.as_view(), name='capturar-calificaciones'),
]