## Hola Luis, no te me pierdas

Este archivo habla un poco sobre las buenas prácticas al momento de contribuir al proyecto, también explica un poco el cómo está estructurado para que no te pierdas mucho en los archivos.

+ `.env`: En este archivo deben de ir las variables de entorno del proyecto y algunas de las cosas que pueden llegar a cambiar entre máquinas (Nombre de la bd, usuario, contraseña, puertos, etc). Este **por nada del mundo lo subas al repositorio** porque puede llegar a tener contraseñas o código sensible, talvez no ahora, pero es para que te acostumbres (igual ya está en el git ignore, pero puedes checar el ejemplo en `env.ejemplo`).
+ `.\scripts`: esta carpeta tiene los scripts que hemos usado para meter datos a la bd.
+ `Contraseñas`: Para tener un estándar en cuanto a las contraseñas de los usuarios te dejo con la tabla de cómo están estructuradas:

| Tipo de usuario | Nombre de usuario (`username`) | Contraseña | Rol en el perfil | Grupo Django |
| :--- | :--- | :--- | :--- | :--- |
| **Superusuario** | `root` | *(la que creaste localmente)* | `CONTROL_ESCOLAR` | `Administrador` |
| **Control escolar** | `control_escolar` | `Control123!` | `CONTROL_ESCOLAR` | `Administrador` |
| **Coordinador** | `coordinador` | `Coord123!` | `COORDINADOR` | `Coordinador` |
| **Profesores** | Su nómina en minúsculas (ej. `emp_001`, `emp_002`) | `Profesor123!` | `PROFESOR` | `Profesor` |
| **Alumnos** | Su matrícula en minúsculas (ej. `23isc001`, `23iau015`) | `Alumno123!` | `ALUMNO` | `Estudiante` |

+ `Ramas en Github`: Esto no es del todo importante, pero trata de acostumbrarte a usar bien las ramas. El orden es el siguiente:
  - `main`: En esta rama solo debe de estar el código ya funcional, no se debería de mover para nada.
  - `develop`: Normalmente estaremos usando esta para trabajar, subir cambios, traer cambios, etc.
  - `fix (opcional)`: Esta no es necesaria en este momento, pero en teoría se debería usar para cuando se debería arreglar algo o así.
