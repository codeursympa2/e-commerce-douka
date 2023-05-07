from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser
)
#Le nom de la classe n'a pas d'importance
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Crée et enregistre un utilisateur avec l'e-mail et le mot de passe donnés.
        """
        if not email:
         raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')

        user = self.model(
        email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password):
        """
        Crée et enregistre un utilisateur du staff avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(
        email,
        password=password,)
        
        user.staff = True
        user.save(using=self._db)
        return user   
    
    def create_admin(self, email, password,firstname,lastname,tel,admin,staff):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(
        email,
        password=password,
        )
        user.firstname=firstname
        user.lastname=lastname
        user.tel=tel
        user.staff = staff
        user.admin = admin
        user.save(using=self._db)
        return user
    
    def create_user_simple(self, email, password,firstname,lastname,tel):
        """
        Crée et enregistre un  simple utilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(
        email,
        password=password,
        )
        user.firstname=firstname
        user.lastname=lastname
        user.tel=tel
        user.staff = False
        user.admin = False
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """ accrochez le nouveau gestionnaire à notre modèle
    class User(AbstractBaseUser):  de l'étape 2 
    on est pas obligé de mettre objects on peut mettre anrichidine mais à la manipulation
    de l'objet User on doit avoir par exemple User.anrichidine.all()
    """
    objects = UserManager()  
    email = models.EmailField(
        verbose_name='adresse email',
        max_length=255,
        unique=True,
    )
    
    firstname=models.CharField(max_length=30,null=True,blank=True,verbose_name='Nom')
    lastname=models.CharField(max_length=30,null=True,blank=True,verbose_name='Prénom')
    tel=models.CharField(max_length=9,null=True,blank=True,verbose_name='Numéro de téléphone')
    
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password sont requis par défaut. Champs requiis pour la connexion
    
    def get_full_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.email
    def get_short_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.email
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il une autorisation spécifique ?"
        # Réponse la plus simple possible : Oui, toujours. Voir l'application
        return True
    def has_module_perms(self, app_label):
        "L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application ?`app_label`?"
        # Réponse la plus simple possible : Oui, toujours
        return True
    
    @property
    def is_staff(self):
        "L'utilisateur est-il un membre du personnel ?"
        return self.staff
    @property
    def is_admin(self):
        "L'utilisateur est-il un membre administrateur ?"
        return self.admin
    
  
        
