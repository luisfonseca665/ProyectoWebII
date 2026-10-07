# Alcances y Limitaciones del Sistema SICENET

Es muy común que en una evaluación los profesores intenten buscar los "huecos" de tu sistema. Si te preguntan *"¿Qué pasa si el alumno hace X cosa?"*, es mejor ser honesto y explicar que es una limitación controlada por el alcance del proyecto escolar, en lugar de mentir y que te pidan demostrarlo.

Aquí tienes exactamente qué valida tu sistema (lo que SÍ hace) y qué dejamos fuera (lo que NO hace).

---

## ✅ LO QUE EL SISTEMA SÍ HACE (ALCANCES Y VALIDACIONES)

Estas son las defensas fuertes de tu sistema. Presúmelas si te preguntan por validaciones:

1. **Límite de Créditos Académicos:**
   * **SÍ revisa** que un alumno no pueda meter más de **36 créditos** en un solo semestre. Si la suma de las materias que eligió supera este número, el sistema aborta la inscripción y le lanza un mensaje de error.
   
2. **Control de Cupos por Aula:**
   * **SÍ revisa** el límite físico del salón. Si un grupo tiene cupo máximo de 30, y el alumno 31 intenta inscribirse, el sistema le niega el acceso diciendo "El grupo ya no cuenta con cupo".

3. **Prevención de Materias Duplicadas:**
   * **SÍ revisa** que un alumno no pueda inscribirse al Grupo A de "Matemáticas" y al Grupo B de "Matemáticas" al mismo tiempo.
   * **SÍ revisa** a nivel Base de Datos (con `UniqueConstraint`) que un alumno no pueda estar dos veces en el mismo grupo exacto.

4. **Bloqueo de Materias ya Aprobadas:**
   * **SÍ revisa** el Kardex del estudiante. Si un alumno ya pasó "Fundamentos de Programación" (calificación mayor o igual a 70), el sistema automáticamente oculta esa materia de su lista de opciones para que no la vuelva a cursar por error.

5. **Protección de Rutas y Roles (Seguridad):**
   * **SÍ revisa** estricta y obligatoriamente el Rol. Un Alumno JAMÁS podrá entrar a la vista de "Capturar Calificaciones", ni escribiendo la URL manualmente, ya que los *Mixins* de Django lo interceptan y lanzan un error 403 de acceso prohibido.

6. **Integridad de Base de Datos:**
   * **SÍ revisa** la orfandad de los datos. Si un administrador quiere borrar la Carrera de "Sistemas", pero la carrera tiene 200 alumnos, la base de datos RESTINGE el borrado para no destruir información vital.

7. **Creación Automática de Cuentas:**
   * **SÍ automatiza** el acceso. Cuando el administrador da de alta un Alumno nuevo, no necesita crearle un usuario y contraseña aparte; el sistema le genera su cuenta en el mismo instante y le asigna su Matrícula como contraseña inicial.

---

## ❌ LO QUE EL SISTEMA NO HACE (LIMITACIONES CONOCIDAS)

Si el evaluador te pregunta por alguna de estas, **tu respuesta debe ser**: *"Esa funcionalidad quedó fuera del alcance inicial del prototipo por cuestiones de tiempo, pero la arquitectura de la base de datos está preparada para implementarlo en una futura versión (v2.0)."*

1. **Sistema de Seriación (Materias Prerrequisito):**
   * **NO revisa** si el alumno pasó "Cálculo Diferencial" antes de meter "Cálculo Integral". Actualmente, un alumno de primer semestre podría ver materias de octavo si pertenecen a su carrera y aún no las ha aprobado. El sistema confía en el criterio del alumno/coordinador al armar la carga.

2. **Cruce de Horarios:**
   * **NO revisa** colisiones de tiempo. Si el alumno inscribe una materia de 8:00 a 9:00 am y otra materia en el mismo horario, el sistema lo permite. Actualmente, el campo de horario (`horario = models.CharField`) es solo un texto descriptivo, no un objeto calculable de fechas.

3. **Promoción Automática de Semestre:**
   * **NO actualiza** el número de semestre del alumno automáticamente. Cuando acaba el ciclo escolar, el sistema no sube solos a los de 1ro a 2do semestre. Eso debe hacerlo Control Escolar editando el perfil.

4. **Oportunidades o Intentos (Historial de Recursamiento):**
   * **NO lleva un registro** complejo de "1ra oportunidad", "2da oportunidad", "Curso de Verano". Si el alumno reprueba y repite, simplemente se crea un nuevo registro de inscripción para ese semestre, pero el Kardex no agrupa las "N" oportunidades.

5. **Recuperación de Contraseñas por Correo:**
   * **NO tiene** un botón de *"Olvidé mi contraseña"* que mande correos automáticos. Si a un alumno se le olvida su clave, tiene que ir a ventanilla y el Administrador usa la función `CambiarPasswordAlumnoView` desde el panel.

6. **Cancelación Automática de Grupos Pequeños:**
   * **NO cierra** los grupos de forma automática si no alcanzan un mínimo de alumnos (ej. "Mínimo 5 alumnos para abrir el grupo"). Esto queda a revisión humana por parte del coordinador.

