from django.urls import path
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
    path('alumnos/<str:pk>/exportar-kardex/', views.exportar_kardex_excel, name='alumno-exportar-kardex'),
    path('alumnos/<str:pk>/actualizar-calificaciones/', views.actualizar_calificaciones, name='alumno-actualizar-calificaciones'),

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
