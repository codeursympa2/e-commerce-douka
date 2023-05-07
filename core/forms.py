from django import forms

class ContactForm(forms.Form):
   name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
       'placeholder':'Saisir votre nom'
   }),required=False)
   email = forms.EmailField(widget=forms.TextInput(attrs={
       'placeholder':'Saisir votre adresse email'
   }),)
   message = forms.CharField(widget=forms.TextInput(attrs={
       'placeholder':'Saisir votre message'
   }),)