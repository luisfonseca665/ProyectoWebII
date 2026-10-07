import os

for root, dirs, files in os.walk('catalog/templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace("request.user.perfil.rol == 'Administrador'", "request.user.perfil.rol == 'CONTROL_ESCOLAR'")
            new_content = new_content.replace("request.user.perfil.rol == 'Coordinador'", "request.user.perfil.rol == 'COORDINADOR'")
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {filepath}')
