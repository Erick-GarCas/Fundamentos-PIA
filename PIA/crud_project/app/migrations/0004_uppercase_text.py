from django.db import migrations

def uppercase_text(apps, schema_editor):
    Tratamiento = apps.get_model('app', 'Tratamiento')
    CitaDental = apps.get_model('app', 'CitaDental')
    for t in Tratamiento.objects.all():
        nombre = (t.nombre or '').upper()
        descripcion = (t.descripcion or '')
        descripcion = descripcion.upper() if descripcion else descripcion
        if t.nombre != nombre or t.descripcion != descripcion:
            t.nombre = nombre
            t.descripcion = descripcion
            t.save(update_fields=['nombre', 'descripcion'])
    for c in CitaDental.objects.all():
        nombre = (c.nombre_paciente or '').upper()
        estatus = (c.estatus or '').upper()
        update_fields = []
        if c.nombre_paciente != nombre:
            c.nombre_paciente = nombre
            update_fields.append('nombre_paciente')
        if c.estatus != estatus:
            c.estatus = estatus
            update_fields.append('estatus')
        if update_fields:
            c.save(update_fields=update_fields)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_reservacion'),
    ]

    operations = [
        migrations.RunPython(uppercase_text, migrations.RunPython.noop),
    ]
