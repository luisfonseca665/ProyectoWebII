# Enciclopedia de Código SICENET: Análisis Exhaustivo

Este documento es el desglose técnico definitivo. Aquí se explica **absolutamente todo**: cada clase, método, atributo y función de tu sistema para que tengas un dominio milimétrico de tu código.

---

## 1. BASE DE DATOS: `catalog/models.py`
Los "Modelos" son clases de Python que Django transforma en tablas de Base de Datos. Cada atributo de la clase se convierte en una columna de la tabla.

### Clase `Carrera`
Representa las carreras disponibles en la institución.
*   **Atributos (Columnas):**
    *   `codigo` (CharField): Cadena de texto única (máximo 20 caracteres). Es el identificador oficial (ej. ISC-2023).
    *   `nombre` (CharField): Nombre completo (ej. Ing. Sistemas).
    *   `creditos` (PositiveIntegerField): Entero positivo. Los créditos totales para titularse.
    *   `duracion` (PositiveIntegerField): Cantidad de semestres que dura.
*   **Métodos:**
    *   `__str__(self)`: Función mágica de Python que define cómo se lee el objeto al imprimirlo (devuelve el nombre de la carrera).
    *   `get_absolute_url(self)`: Genera el link (ruta) directo para ver los detalles de una carrera específica luego de crearla o editarla.

### Clase `Materia`
*   **Atributos:**
    *   `carrera` (ForeignKey): Llave foránea. Conecta esta materia con una `Carrera`. Si la carrera se borra, las materias se borran (CASCADE).
    *   `codigo` (CharField), `nombre` (CharField), `unidades` (PositiveIntegerField), `creditos` (PositiveIntegerField).

### Clase `Perfil`
Controla el control de acceso basado en roles (RBAC).
*   **Atributos:**
    *   `usuario` (OneToOneField): Vincula este Perfil 1 a 1 con la tabla secreta `User` de Django (la que guarda passwords y maneja el login).
    *   `rol` (CharField): Guarda una opción del diccionario `ROLES` ('CONTROL_ESCOLAR', 'COORDINADOR', 'PROFESOR', 'ALUMNO').

### Clase `Alumno` y `Profesor`
*   **Atributos Especiales:**
    *   `matricula` / `numero_empleado` (CharField): Usan el parámetro `primary_key=True`. Esto significa que Django no va a crear una columna 'ID' autonumérica (1, 2, 3), sino que el ID real en la base de datos es el texto de la matrícula.
    *   `carrera` (ForeignKey, on_delete=RESTRICT): En Alumnos, la carrera está restringida; no se puede borrar la carrera de sistemas si hay alumnos inscritos.
    *   `estatus` (CharField): Guarda 'A' (Activo), 'B' (Baja) usando la tupla `ESTATUS`.

### Clase `Grupo`
Representa el aula virtual donde se da clase.
*   **Atributos:**
    *   `materia` y `profesor` (ForeignKeys): Un grupo tiene 1 materia y 1 profesor. El profesor tiene `on_delete=SET_NULL`, si el profe renuncia, el grupo no se borra, solo queda sin profe asignado.
    *   `clave` (CharField): El nombre del grupo (Ej. 'A', '1A').
    *   `cupo` y `numAlumnos`: Para el algoritmo de inscripción.
    *   `alumnos` (ManyToManyField): Conecta a los alumnos. Django usaría una tabla oculta, pero nosotros usamos el parámetro `through='Calificacion'` para decirle a Django: *"Usa mi tabla manual 'Calificacion' para relacionarlos"*.

### Clase `Calificacion` (Tabla Intermedia)
*   **Atributos:**
    *   `alumno` y `grupo` (ForeignKeys en CASCADE): Si el grupo o el alumno se borran, esta calificación desaparece.
    *   `calificacion_final` (DecimalField): Guarda números con decimales. Usa `validators=[MinValueValidator(0), MaxValueValidator(100)]` para evitar que un profe ponga "150" de calificación.
*   **Meta clase:** `UniqueConstraint(fields=['alumno', 'grupo'])` asegura a nivel base de datos que un alumno no pueda inscribirse 2 veces al mismo grupo.

---

## 2. EL CEREBRO: `catalog/views.py`
Las vistas reciben la petición HTTP del usuario, consultan la base de datos, y devuelven un archivo HTML.

### A) Los Mixins de Seguridad
Son clases "vigilantes" que se inyectan en las vistas mediante herencia múltiple.
*   `AdminRequiredMixin`, `CoordinadorRequiredMixin`, etc.: Heredan de `UserPassesTestMixin`. Tienen una función obligatoria llamada `test_func(self)` que devuelve `True` o `False`.
*   **Cómo funcionan:** Alguien intenta entrar a una vista. Django pausa, corre `test_func()`. La función evalúa `user.perfil.rol == 'CONTROL_ESCOLAR'`. Si es falso, Django patea al usuario devolviendo un error HTTP 403 Forbidden.

### B) Funciones de Sincronización
*   `sincronizar_usuario_profesor(profesor)` y `sincronizar_usuario_alumno(alumno)`:
    *   **Paso 1:** Toman al objeto Alumno o Profesor recién guardado.
    *   **Paso 2:** Llaman a `User.objects.get_or_create(username=matricula)`. Esta función devuelve una tupla `(objeto, booleano_creado)`. Busca en la DB si existe la cuenta de login. Si no, la crea.
    *   **Paso 3:** Si la cuenta se acaba de crear (`if created:`), le asigna la matrícula como contraseña por defecto usando el método `set_password()`, que hace un hash (encripta) la contraseña antes de mandarla al disco duro.
    *   **Paso 4:** Usa `Perfil.objects.get_or_create()` para garantizar que esa cuenta tenga su rol respectivo.

### C) Vistas Generales de Catálogo (CRUD)
Las clases genéricas (Class-Based Views) te ahorran horas de programación.
*   **ListView (Listar):** (Ej. `CarreraListView`). Su único parámetro obligatorio es `model = Carrera`. Django agarra todo en `Carrera.objects.all()` y lo manda a la plantilla como un bucle.
    *   *Optimización:* En `GrupoListView`, sobreescribimos el método `get_queryset(self)`. En vez de hacer un `all()`, usamos `Grupo.objects...annotate()`. `.annotate()` es una función avanzada que le dice a la base de datos SQL que cuente (`Count`) las filas internamente en la misma consulta, resolviendo el problema de lentitud N+1.
*   **DetailView (Ver uno):** Requiere un ID en la URL (ej. `<int:pk>`). Entra a la DB, hace un `SELECT * WHERE id=pk`, y lo muestra en la plantilla. En `AlumnoDetailView` sobreescribimos `get_context_data` para, además de mandar los datos del alumno, inyectar también sus `Calificaciones`.
*   **CreateView / UpdateView (Crear/Editar):** 
    *   Parámetros clave: `form_class` (El archivo forms.py que se va a usar) y `success_url` (A dónde redirigir al terminar exitosamente usando `reverse_lazy`).
    *   Sobreescribimos `form_valid(self, form)`: Este método se ejecuta cuando el usuario da clic en "Guardar" y los datos pasaron los filtros de seguridad. En las vistas de profesor/alumno, aquí mandamos a llamar a `sincronizar_usuario(...)` para que se cree la cuenta a la par.
*   **DeleteView (Eliminar):** Por seguridad Django nunca borra a la primera. Siempre redirige a `confirm_delete.html` donde el usuario hace un POST para confirmar. En `GrupoMasivoDeleteView`, sobreescribimos `form_valid()` para hacer un **Borrado Lógico**: en vez de aplicar `delete()`, tomamos los objetos y les ponemos `activo = False`.

### D) La Lógica Pesada: `InscripcionMateriasView`
Esta es la vista más compleja de todo tu sistema.
*   **`dispatch(self, request)`:** Es el método "Portero". Se ejecuta antes de cualquier otra cosa. Revisa quién es el que inició sesión. Si es el alumno, asigna su propio usuario a la sesión. Si es el Coordinador, lee la URL (el parámetro `matricula`) y carga el perfil de ese alumno en memoria. Luego suma todos los créditos actuales con `aggregate(total=Sum('creditos'))`. Si ya tiene 36, lo batea desde aquí.
*   **`get_context_data(self)`:** Prepara la pantalla antes de mandarla al HTML. Usa `exclude()` en las consultas SQL para filtrar los grupos que pertenecen a materias que el alumno ya aprobó (`calificacion_final__lt=70`) para que ni siquiera le aparezcan en las opciones a seleccionar.
*   **`post(self, request)`:** Recibe los datos del formulario (las casillas marcadas).
    1. Revisa que el ID de la materia no se repita en su lista (para no meter Matemáticas dos veces).
    2. Suma los créditos actuales con los nuevos. Si supera 36, lanza `messages.error()` y aborta la transacción.
    3. Si pasa todo: Inicia un bucle `for` sobre los grupos. Verifica `if grupo.numAlumnos < grupo.cupo:`. Si hay lugar, hace el `.get_or_create` de la `Calificacion`, e incrementa el contador del grupo. 

### E) Descarga del Kardex (`exportar_kardex_excel`)
*   **Function-Based View:** Usa la palabra reservada `def` en vez de `class`.
*   **Proceso:** 
    1. Importa `openpyxl`. Genera un libro de Excel en memoria virtual de la RAM (`wb = openpyxl.Workbook()`).
    2. Hace un `filter` de la base de datos seleccionando las calificaciones donde `calificacion_final__gt=0` (que ya fueron evaluadas).
    3. Hace bucles for (`for row_idx, calif in enumerate(...)`) llenando manualmente `ws.cell(...)` con la calificación, pintándola de rojo si reprueba usando el módulo de estilos `Font` y `PatternFill`.
    4. El truco maestro: `response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')`. Esto engaña al navegador para que en vez de abrir un HTML web normal, interprete la petición como una descarga de un archivo binario.

### F) Funcionalidad de Profesores (`CapturarCalificacionesView`)
*   Recibe un GET para mostrar la tabla de alumnos. El `get_context_data` hace un `.select_related('alumno')` (que es un equivalente a un `INNER JOIN` en SQL) para traer al alumno sin desgastar la base de datos.
*   En el `post(self, request)`, la vista recibe todas las casillas de texto con calificaciones (vienen como `calificacion_14`, `calificacion_15`, etc.). El código busca estas llaves generadas dinámicamente, convierte el texto a decimal (`float(valor)`), y ejecuta un `.save()` en el modelo `Calificacion` para actualizar la base de datos.

---

## 3. EL CONMUTADOR: `catalog/urls.py`
*   `path()`: Función de Django que toma 3 argumentos principales.
    1. La URL como cadena ('alumnos/nuevo/').
    2. La Vista que la va a manejar (`views.AlumnoCreateView.as_view()`).
    3. El nombre de la ruta (`name='alumno-create'`). Se usa el nombre porque si mañana cambian las URLs a '/estudiantes/nuevo', Django lo resuelve en automático basándose en el "nombre de fantasía" y el sistema no se rompe.
*   **URLs Dinámicas:** Se declaran con símbolos `< >`.
    *   `<str:pk>` (Cadena): Le dice al servidor "Aquí viene texto, tómalo y pásalo a la vista como un parámetro llamado PK". Lo usamos en profesores y alumnos.
    *   `<int:pk>` (Entero): Asegura que solo entren números, y si alguien escribe letras, da un error 404 Automático. Se usa en ID's normales.

---
**Cualquier pregunta en la evaluación se resume a esto:** "El usuario interactúa con la **Vista**, la Vista toma la inteligencia artificial del **ORM** para hablar con los **Modelos** de SQL de manera segura, y empuja el resultado hacia la **Plantilla** HTML."
