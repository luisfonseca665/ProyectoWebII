import os
import re

base_dir = r"c:\Users\garci\Documentos\ITSUR\7 Semestre\Programacion Web II\ProyectoWebII\catalog"
templates_dir = os.path.join(base_dir, 'templates')
catalog_templates_dir = os.path.join(templates_dir, 'catalog')

# 1. Update form_generico.html (bg-success)
form_generico_path = os.path.join(templates_dir, 'form_generico.html')
if os.path.exists(form_generico_path):
    with open(form_generico_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('bg-primary', 'bg-success')
    with open(form_generico_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Update pagina_maestra.html (Remove navbar search, add simple-datatables)
pagina_maestra_path = os.path.join(templates_dir, 'pagina_maestra.html')
if os.path.exists(pagina_maestra_path):
    with open(pagina_maestra_path, 'r', encoding='utf-8') as f:
        pm_content = f.read()

    # Remove the search form
    search_form_regex = r'<form class="d-flex" role="search">.*?</form>'
    pm_content = re.sub(search_form_regex, '', pm_content, flags=re.DOTALL)

    # Add Simple DataTables CSS in head
    if 'simple-datatables' not in pm_content:
        head_insert_pos = pm_content.find('</head>')
        dt_css = '\n    <link href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css" rel="stylesheet" type="text/css">\n'
        pm_content = pm_content[:head_insert_pos] + dt_css + pm_content[head_insert_pos:]

        # Add Simple DataTables JS before body end
        body_insert_pos = pm_content.find('</body>')
        dt_js = """
    <script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" type="text/javascript"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const tables = document.querySelectorAll(".datatable");
            tables.forEach(function(table) {
                new simpleDatatables.DataTable(table, {
                    searchable: true,
                    labels: {
                        placeholder: "Buscar...",
                        perPage: "registros por página",
                        noRows: "No se encontraron registros",
                        info: "Mostrando del {start} al {end} de {rows} registros",
                    }
                });
            });
        });
    </script>
"""
        pm_content = pm_content[:body_insert_pos] + dt_js + pm_content[body_insert_pos:]

    with open(pagina_maestra_path, 'w', encoding='utf-8') as f:
        f.write(pm_content)

# 3. Add .datatable class to all tables in lists and details
def add_datatable_class(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Replace class="table ..." with class="table ... datatable"
            if '<table class="table ' in content and 'datatable' not in content:
                content = content.replace('<table class="table ', '<table class="table datatable ')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

add_datatable_class(templates_dir)
add_datatable_class(catalog_templates_dir)

print("Updates to templates completed successfully.")
