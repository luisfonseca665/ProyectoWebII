import os

for root, dirs, files in os.walk('catalog/templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace("request.user.groups.all.0.name == 'Estudiante'", "request.user.perfil.rol == 'ALUMNO'")
            new_content = new_content.replace("request.user.groups.all.0.name == 'Profesor'", "request.user.perfil.rol == 'PROFESOR'")
            new_content = new_content.replace("request.user.groups.all.0.name == 'Administrador'", "request.user.perfil.rol == 'Administrador'")
            new_content = new_content.replace("request.user.groups.all.0.name == 'Coordinador'", "request.user.perfil.rol == 'Coordinador'")
            new_content = new_content.replace("request.user.groups.all.0.name|default:\"Admin\"", "request.user.perfil.rol|default:\"Admin\"")
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {filepath}')
