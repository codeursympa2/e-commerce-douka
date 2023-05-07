from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import ReadOnlyPasswordHashField


User=get_user_model()

class RegistrerFormUserAdmin(forms.ModelForm):
   password= forms.CharField(widget=forms.PasswordInput)
   password_2= forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
   
   class Meta:
       model=User
       fields=['email','firstname','lastname','tel','admin','staff']
       verbose_name = 'Utilisateur'
       verbose_name_plural = 'Utilisateurs'
       
   def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("l'e-mail est dejà pris")
        return email   
     
   def clean(self):
       '''
        Vérifiez que les deux mots de passe correspondent.
       '''
       cleaned_data = super().clean()
       password=cleaned_data.get('password')
       password_2=cleaned_data.get('password_2')
       
       if password is not None and password != password_2:
           self.add_error("password_2","Les deux mots  de passes doivent être identiques")
       
       return  cleaned_data  
   def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
           user.save()
        
        return user
        
class UserAdminChangeForm(forms.ModelForm):
    """Un formulaire pour mettre à jour les utilisateurs. Inclut tous les champs sur
    l'utilisateur, mais remplace le champ du mot de passe par celui de l'administrateur
    champ d'affichage du hachage du mot de passe.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password','firstname','lastname','tel' , 'admin','staff']

    def clean_password(self):
    # Indépendamment de ce que l'utilisateur fournit, renvoie la valeur initiale.
    # Cela se fait ici, plutôt que sur le terrain, car le
    # le champ n'a pas accès à la valeur initiale
        return self.initial["password"]     
    
class LoginFormUser(forms.Form):
   email=forms.EmailField(label='Addresse  email')
   password = forms.CharField(widget=forms.PasswordInput(),label='Mot de passe') 
   
class RegisterFormUser(forms.Form):
    lastname=forms.CharField(label="Nom")
    firstname=forms.CharField(label="Prénom")
    tel=forms.CharField(label="Numéro de téléphone")
    email=forms.EmailField(label="Adresse email")
    password=forms.CharField(widget=forms.PasswordInput(),label="Mot de passe")
    password_confirm=forms.CharField(widget=forms.PasswordInput(),label="Confirmation mot de passe")
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        
        email_filter=User.objects.filter(email=email)
        
        if email_filter.exists():
            self.add_error('email','Cet email est dejà prise.')
            
        return email    
            
    def clean(self):
        cleaned_data = super().clean()
        password=self.cleaned_data.get('password')
        password_confirm=self.cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            self.add_error('password_confirm','Les deux mots de passes doivent être identique.' )
        return cleaned_data    
               
   
               