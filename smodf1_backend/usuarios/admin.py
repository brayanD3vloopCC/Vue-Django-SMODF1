from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('correo', 'nickname', 'nombre_completo', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('correo', 'email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'nombre_completo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'email', 'nickname', 'nombre_completo', 'password1', 'password2'),
        }),
    )
    search_fields = ('correo', 'email', 'nickname', 'nombre_completo')
    ordering = ('correo',)

admin.site.register(Usuario, UsuarioAdmin) 