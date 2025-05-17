from django.db import migrations
from django.contrib.auth.hashers import make_password

def assign_default_user(apps, schema_editor):
    # Obtener los modelos
    Project = apps.get_model('api', 'Project')
    Usuario = apps.get_model('usuarios', 'Usuario')
    
    # Obtener o crear un usuario por defecto
    try:
        default_user = Usuario.objects.get(email='admin@example.com')
    except Usuario.DoesNotExist:
        default_user = Usuario.objects.create(
            email='admin@example.com',
            nombre_completo='Administrador',
            nickname='admin',
            is_staff=True,
            is_superuser=True,
            password=make_password('admin123')  # Usar make_password en lugar de set_password
        )
    
    # Asignar el usuario por defecto a todos los proyectos sin usuario
    Project.objects.filter(user__isnull=True).update(user=default_user)

def reverse_assign_default_user(apps, schema_editor):
    # No hacemos nada en la reversión
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_alter_projectimage_options_and_more'),
        ('usuarios', '0001_initial'),  # Asegúrate de que esta sea la migración correcta
    ]

    operations = [
        migrations.RunPython(assign_default_user, reverse_assign_default_user),
    ] 