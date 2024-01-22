from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sucursal, UsuarioSucursal, Categoria, Subcategoria, Participante, Evento, User


class UsuarioSucursalInline(admin.StackedInline):
    model = UsuarioSucursal
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioSucursalInline,)

admin.site.register(User, CustomUserAdmin)

admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Participante)
admin.site.register(Evento)

