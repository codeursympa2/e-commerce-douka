from django.shortcuts import render
from django.contrib.auth import logout,login
from django.shortcuts import redirect,render,reverse
from .forms import LoginFormUser,RegisterFormUser
from django.views.generic import FormView
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

User=get_user_model()

def logout_view(request):
    logout(request)
    return redirect('product-list')



class Login_view(FormView):
    form_class=LoginFormUser
    template_name = 'users/login.html'
   
    def get(self, request):
        if request.user.is_authenticated == True:
            return redirect('product-list')
        else:
            return super(Login_view(), self).get(request)
        
        
    def get_success_url(self):
        return reverse('product-list')
    
    def form_valid(self,form):
        email_user=form.cleaned_data.get('email')
        password_user=form.cleaned_data.get('password')

        user=authenticate(username=email_user,password=password_user)
        
        if user is not None:
            login(self.request,user)
            self.get_success_url()
            messages.info(self.request,"Connexion reussie.")

        else:    
            messages.error(self.request,"Adresse email ou mot de passe invalid")
            return redirect('login')
        return super(Login_view, self).form_valid(form)
    

class Register_view(FormView):
    
  template_name='users/register.html'
  form_class=RegisterFormUser
  
  
  def get(self, request):
        if request.user.is_authenticated == True:
            return redirect('product-list')
        else:
            return super(Register_view(), self).get(request)
  
  
  def get_success_url(self):
      return reverse('login')
  
  def form_valid(self,form):
      
      User.firstname=form.cleaned_data.get('firstname')
      User.lastname=form.cleaned_data.get('lastname')
      User.email=form.cleaned_data.get('email')
      User.tel=form.cleaned_data.get('tel')
     
      
      User.objects.create_user_simple(User.email,form.cleaned_data.get('password'),User.firstname,User.lastname,User.tel)
      
      messages.info(self.request,"Compte crée avec succès");
      
      return super(Register_view, self).form_valid(form)