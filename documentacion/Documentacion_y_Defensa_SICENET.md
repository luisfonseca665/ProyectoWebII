# Documentación Exhaustiva y Defensa de Proyecto: SICENET

Esta es tu guía definitiva. Contiene la documentación técnica del código, el paso a paso de qué hace cada parte, y una simulación rigurosa de evaluación para que tengas todas las respuestas preparadas.

---

## PARTE 1: FLUJO DE TRABAJO (ARQUITECTURA MVT)

Cuando te pregunten cómo funciona tu proyecto de forma general, debes explicar la arquitectura **MVT (Modelo - Vista - Plantilla)** de Django.

**Cómo explicarlo paso a paso:**
> "El sistema opera mediante la arquitectura MVT. Todo comienza cuando el **Navegador** hace una petición (por ejemplo, acceder a `/alumnos/`). 
> 1. Primero, el archivo **`urls.py`** intercepta esa petición, actúa como un conmutador y dirige el tráfico hacia la **Vista** correspondiente (`views.py`).
> 2. La **Vista** es el controlador principal. Contiene la lógica de negocio. Esta le hace una solicitud al **Modelo** (`models.py`) para extraer la información.
> 3. El **Modelo** transforma esa solicitud en una consulta SQL (gracias al ORM de Django), consulta la base de datos PostgreSQL/SQLite y devuelve los datos a la Vista.
> 4. Finalmente, la Vista toma esos datos y los inyecta en una **Plantilla (`.html`)**, que se renderiza y se envía de regreso al Navegador para que el usuario la vea."

---

## PARTE 2: DOCUMENTACIÓN DEL CÓDIGO (QUÉ HACE Y CÓMO LO HACE)

Aquí tienes la explicación técnica de las partes más críticas del sistema. 

### 1. El Archivo `urls.py` (Las Rutas)
Este archivo es el mapa del sistema. 
*   **¿Qué hace?** Asocia una dirección URL (ej. `alumnos/nuevo/`) con una función en Python (Vista).
*   **¿Cómo lo hace?** Usa la lista `urlpatterns`. Cada línea `path()` evalúa la URL escrita. 
*   **El parámetro `<pk>`:** Notarás que algunas rutas tienen `<str:pk>` y otras `<int:pk>`. `pk` significa *Primary Key*. Para alumnos usamos `<str:pk>` porque su llave es la **Matrícula** (que es texto). Para carreras o grupos usamos `<int:pk>` porque sus llaves son números (ID 1, 2, 3...).

### 2. El Archivo `models.py` (La Base de Datos)
*   **¿Qué hace?** Crea las tablas SQL sin tener que escribir código SQL.
*   **Modelos Principales:**
    *   `Perfil`: Extiende el modelo `User` de Django para agregarle roles (`ALUMNO`, `PROFESOR`, `CONTROL_ESCOLAR`, `COORDINADOR`). Se vincula con un `OneToOneField`.
    *   `Materia` y `Carrera`: Tablas de catálogo. Se vinculan con una `ForeignKey`.
    *   `Calificacion`: Es una **tabla pivote o intermedia**. Une a un `Alumno` con un `Grupo` y guarda el valor numérico de la calificación final.
*   **Los métodos `on_delete`:** Usamos `CASCADE` (borrado en cascada) para borrar la calificación si se borra el grupo. Usamos `RESTRICT` para evitar que alguien borre una carrera si aún tiene alumnos inscritos en ella.

### 3. El Archivo `views.py` (La Lógica)
*   **Vistas Basadas en Clases (CBV):** Usamos `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`. Nos ahorran reescribir lógica estándar de crear, leer, actualizar y eliminar.
*   **¿Cómo protegemos la seguridad?** Usamos **Mixins**. Por ejemplo, la clase `AdminRequiredMixin`. Esto evalúa si `request.user.perfil.rol == 'CONTROL_ESCOLAR'`. Si el usuario no tiene ese rol, Django bloquea el acceso con un error 403 (Prohibido).
*   **Sincronización de Usuarios:** Las funciones `sincronizar_usuario_alumno` y `profesor` automatizan la creación de cuentas. Cuando registras a un profesor en el formulario, estas funciones crean su usuario de acceso de Django por debajo usando `User.objects.get_or_create`.
*   **Validación de Inscripción:** En `InscripcionMateriasView`, el método `post()` valida que la suma de los créditos de las materias previas (`aggregate(Sum)`) más los créditos de las nuevas selecciones no superen los **36 créditos** permitidos por semestre.

---

## PARTE 3: SIMULACIÓN DE EXAMEN ORAL (PREGUNTAS DEL EVALUADOR)

Voy a ponerme mi traje de profesor exigente. Aquí están las preguntas "trampa" que te puedo hacer y la respuesta exacta para sacar un 100.

### 😈 1. "En el código, veo que usaste una función llamada `exportar_kardex_excel` en lugar de una 'Class-Based View'. Si todo tu sistema usa Clases, ¿por qué esta es una función suelta? ¿No es una mala práctica?"

**😎 Tu Respuesta:**
> "No es una mala práctica, profesor; es aplicar la herramienta correcta para el caso de uso. Las Class-Based Views (como `ListView` o `CreateView`) están optimizadas para renderizar archivos HTML o procesar formularios web (CRUD).
> Sin embargo, la función `exportar_kardex_excel` hace algo completamente procedimental: usa la librería externa `openpyxl` para crear un archivo binario `.xlsx` celda por celda, darle color, estilo, y retornar una respuesta HTTP forzando la descarga del archivo. Para un proceso tan secuencial y personalizado que no devuelve una interfaz web, la documentación de Django recomienda usar **Function-Based Views** por su simplicidad y control absoluto línea por línea."

### 😈 2. "Explícame cómo funciona la relación entre Alumno, Grupo y Calificación en la Base de Datos. Si se inscribe a 3 grupos, ¿cómo se guarda?"

**😎 Tu Respuesta:**
> "Se trata de una relación Muchos-a-Muchos (Many-to-Many). Un alumno puede tener muchos grupos y un grupo puede tener muchos alumnos.
> En nuestro archivo `models.py`, en lugar de dejar que Django cree una tabla oculta, definimos un modelo explícito llamado `Calificacion`. Esta actúa como nuestra **Tabla Intermedia**. Cuando el alumno inscribe 3 materias, se crean 3 registros nuevos en la tabla `Calificacion`. Cada registro guarda el ID del alumno, el ID del grupo asignado y tiene un campo adicional para la `calificacion_final` que por defecto está vacío. Las vistas de los profesores interactúan directamente con esta tabla para asignar los promedios."

### 😈 3. "Dices que este sistema es seguro, pero ¿cómo evitas que un Alumno modifique calificaciones si logra adivinar la URL de la vista de captura?"

**😎 Tu Respuesta:**
> "Implementamos una arquitectura robusta de control de acceso (RBAC) apoyada en el middleware de Django. Cada ruta sensible está protegida por un **Mixin** personalizado en las Clases. 
> Por ejemplo, la vista `CapturarCalificacionesView` hereda el mixin `ProfesorRequiredMixin`. Antes de que la vista ejecute siquiera la primera línea de código de negocio, el Mixin intercepta la petición, verifica si el usuario está autenticado y consulta la tabla `Perfil`. Si el `request.user.perfil.rol` no es explícitamente `PROFESOR` o `CONTROL_ESCOLAR`, el request es abortado inmediatamente con un error 403 Forbidden. Un alumno jamás podría entrar ni modificar la información."

### 😈 4. "Pregunta de optimización. Veo que usas `.annotate(num_materias=Count('id'))` en la vista de Listado de Grupos. ¿Para qué sirve eso y por qué no lo contaste con un simple `for` en Python?"

*(Nota: Esta respuesta te va a dar todos los puntos posibles, es de nivel avanzado)*

**😎 Tu Respuesta:**
> "Esa línea la implementamos para resolver el **Problema de Consultas N+1**. 
> Si usáramos un ciclo `for` en Python para recorrer 50 grupos y contar cuántas materias tiene cada uno llamando a sus relaciones, Django habría ejecutado 1 consulta principal y luego 50 consultas secundarias a la base de datos (51 consultas en total para cargar una sola página).
> Al usar la función `.annotate(Count('id'))`, le instruimos al ORM de Django que traslade ese cálculo matemático directamente al motor SQL. Esto hace que la base de datos realice los conteos y agrupaciones de forma interna y nos devuelva toda la información en **una única y sola consulta**. Esto reduce el tiempo de respuesta drásticamente y evita que el servidor colapse cuando tengamos cientos de registros."

---

### Recomendación para tu presentación de mañana
Repasa estas respuestas en voz alta. Habla con seguridad de términos como **Arquitectura MVT**, **Claves Primarias (PK)**, **ORM**, **Tabla Intermedia**, y **Problema N+1**. Si mencionas esos términos técnicos durante tu defensa, no habrá duda de que dominas tu código al 100%. ¡Mucho éxito!
