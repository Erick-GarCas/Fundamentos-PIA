import os
import django
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_project.settings')
django.setup()

try:
    tpl = get_template('citas_listar.html')
    print('Template loaded OK:', tpl.origin)
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Error:', e)
