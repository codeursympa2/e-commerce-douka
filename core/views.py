from django.shortcuts import render,reverse
from django.views import generic
from .forms import *
from django.contrib import  messages
from django.conf import settings

#
from django.core.mail import send_mail


class HomeView(generic.TemplateView):
    template_name='index.html'

class ContactView(generic.FormView):
    template_name='contact.html'
    form_class=ContactForm 
    form_novalidate=True
    
    def get_success_url(self):
        return reverse("contact")
    def form_valid(self,form):
        messages.info(self.request,"Message enregistré avec succès.")
        
        #Recuperation des données
        name=form.cleaned_data.get('name')
        email=form.cleaned_data.get('email')
        message=form.cleaned_data.get('message')
        
        full_message="""
            Message de {name}, {email} <p>
            ___________________________
            
            {message}
        """
        
        #Envoie d'email
        send_mail(
            subject="Message reçu",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactView, self).form_valid(form)