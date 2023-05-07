from django.contrib import admin
from .models import *

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import RegistrerFormUserAdmin , UserAdminChangeForm

User = get_user_model()


# Supprimer le modèle de groupe de l'administrateur. Nous ne l'utilisons pas.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = UserAdminChangeForm #Formulaire de modification de l'utilisateur
    add_form = RegistrerFormUserAdmin    #Formulaire de création de l'utilisateur
 
    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['email','firstname','lastname','tel','staff','admin']
    list_filter = ['admin','staff']
    fieldsets = (
    ('Identifiants de connexion', {'fields': ('email', 'password',)}),
    ('Informations personnelles', {'fields': ('firstname','lastname','tel')}),
    ('Permissions', {'fields': ('admin','staff',)}),
    )
    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('firstname','lastname','tel','email', 'password', 'password_2','admin','staff')}
    ),
    )
    search_fields = ['email','firstname','lastname','tel']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)   