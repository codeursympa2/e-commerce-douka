from django import forms
from .models import *
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User


User=get_user_model()

class AddToCartForm(forms.ModelForm):
                                        #Vidage du champs color
    colour=forms.ModelChoiceField(queryset=ColourVariation.objects.none(),label='Couleur')
    size=forms.ModelChoiceField(queryset=SizeVariation.objects.none(),label='Taille')
    
    
    class Meta:
        model=OrderItem
        fields=['quantity','colour','size']
    #Au chargement du formulaire
    def __init__(self, *args, **kwargs):
        #Recupération de l'id
        product_id=kwargs.pop('id_product')
        
        product=Product.objects.get(id=product_id)
        
        super().__init__(*args, **kwargs)
        
        #Ajout des couleurs disponibles du produit au champs
        self.fields['colour'].queryset=product.avalaible_colours.all()
        self.fields['size'].queryset=product.avalaible_sizes.all()
        
class AddressForm(forms.Form):
   
   
   shipping_address_line_1=forms.CharField(required=False,label="Adresse de livraison 1")
   shipping_address_line_2=forms.CharField(required=False,label="Adresse de livraison 2")
   shipping_zip_code=forms.CharField(required=False,label="Code postal de livraison 1")
   shipping_city=forms.CharField(required=False,label="Ville de livraison 1")
   
   billing_address_line_1= forms.CharField(required=False,label="Adresse de facturation 1")
   billing_address_line_2 = forms.CharField(required=False,label="Adresse de facturation 2")
   billing_zip_code = forms.CharField(required=False,label="Code postal de facturation 1")
   billing_city=forms.CharField(required=False,label="Ville de facturation 2")
   
   #On vide les champs    
   selected_shipping_address=forms.ModelChoiceField(
       Address.objects.none(),required=False,
       label="Selectionner une adresse de facturation"
   ) 
      
   selected_billing_address=forms.ModelChoiceField(
       Address.objects.none(),required=False,
       label="Selectionner une adresse de livraison"
       
   )      
   
   def __init__(self, *args, **kwargs):
        user_id=kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user=User.objects.get(id=user_id)
        shipping_address_qs=Address.objects.filter(
                user=user,
                address_type='S'
            )
        billing_address_qs=Address.objects.filter(
                user=user,
                address_type='B'
            )
        
        self.fields['selected_shipping_address'].queryset=shipping_address_qs
        self.fields['selected_billing_address'].queryset=billing_address_qs
    
   def clean(self):
       data=self.cleaned_data
       
       selected_shipping_address= data.get('selected_shipping_address',None)
       if selected_shipping_address is None:
           if not data.get('shipping_address_line_1',None):
               self.add_error('shipping_address_line_1','Ce champs est obligatoire.')
           if not data.get('shipping_address_line_2',None):
               self.add_error('shipping_address_line_2','Ce champs est obligatoire.')
           if not data.get('shipping_zip_code',None):
               self.add_error('shipping_zip_code','Ce champs est obligatoire.')
           if not data.get('shipping_city',None):
               self.add_error('shipping_city','Ce champs est obligatoire.')
               
       selected_billing_address= data.get('selected_billing_address',None)
       if selected_billing_address is None:
           if not data.get('billing_address_line_1',None):
               self.add_error('billing_address_line_1','Ce champs est obligatoire.')
           if not data.get('billing_address_line_2',None):
               self.add_error('billing_address_line_2','Ce champs est obligatoire.')
           if not data.get('billing_zip_code',None):
               self.add_error('billing_zip_code','Ce champs est obligatoire.')
           if not data.get('billing_city',None):
               self.add_error('billing_city','Ce champs est obligatoire.')