"""
    exemple:
           [context] [kwargs]
               |      |
        <p>article.name</p>
"""

from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.contrib import messages
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *

from .utils import *

from .forms import *

class ProductListView(generic.ListView):
    
    model = Product
    template_name = "cart/product_list.html"
    paginate_by = 6
    
    def get_queryset(self, **kwargs):
        q = self.request.GET.get('q', None)
        products = self.model.objects.all()
        if q:
            products = products.filter(title__contains=q)
        return products
    
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q', None)
        context = super().get_context_data(**kwargs)
        
        query=self.model.objects.all()
        
        if q:
            context["search"] = q
            query=self.get_queryset();
        
        paginator = Paginator(query, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            pagi = paginator.page(page)
        except PageNotAnInteger:
            pagi = paginator.page(1)
        except EmptyPage:
            pagi = paginator.page(paginator.num_pages)
            
        context['products'] = pagi   
        return context

class ProductDetailView(generic.FormView):
    template_name='cart/detail_product.html'
    form_class=AddToCartForm
    
    #Renvoie l'objet
    def get_object(self):
        return get_object_or_404(Product,slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('cart') 
    
    #Recupere les valeurs disponible injecté par une requete
    # dans le contexte actuel [L'enregistrement actuel]
    def get_form_kwargs(self):
        kwargs= super(ProductDetailView, self).get_form_kwargs()
        #Recupération de l'id du produit dans le formulaire
        kwargs['id_product']=self.get_object().id
        return kwargs
    
    def form_valid(self,form):
        #Sauvegarde dans la session le produit
        order=get_or_set_order_session(self.request)
        
        product=self.get_object()
        
        #Recherche du produit dans la commande utilisateur
        item_filter=order.item.filter(
            product=product,
            colour=form.cleaned_data['colour'],
            size=form.cleaned_data.get('size')
            
        )
        
        #Si le produit est dejà dans la commande 
        if item_filter.exists():
            item=item_filter.first()            
            item.quantity=item.quantity+form.cleaned_data.get('quantity')
            item.save()
        else:
            #L'enregistrement avec commit=False vous permet d'obtenir un objet modèle, 
            #puis vous pouvez ajouter vos données supplémentaires et 
            #l'enregistrer.
            new_item=form.save(commit=False)
            new_item.product=product
            new_item.order=order
            new_item.save()
        
        return super(ProductDetailView, self).form_valid(form)
    
    #Affichage du produit courant
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        context["product"]= self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name = "cart/cart.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Vérifie si l'utilisateur est administrateur
            if  request.user.is_staff:
                # Obtient l'URL précédente (ou une URL par défaut si aucune n'est disponible)
                previous_url = request.META.get('HTTP_REFERER', reverse('product-list'))
                return redirect(previous_url)
            else:
                return super().get(request, *args, **kwargs)
        else:
            previous_url = "login" 
            return redirect(previous_url)       
       
        
    #get_or_set_order_session(self.request)
    def get_context_data(self, *args, **kwargs):
        context = super(CartView,self).get_context_data(**kwargs)
        
        orders=OrderItem.objects.filter(order=get_or_set_order_session(self.request)).order_by('-id')
        context["order_items"] = orders
        
        def get_count_order(self):
            return "produits" if orders.count() > 1 else "produit"
        
        context['order_plural_single']=get_count_order(self)
        
        def get_sous_prix_total(self):
           return sum(
                (order_item.quantity * order_item.product.price)
                for order_item in orders)        
        context['prix_total']=get_sous_prix_total(self)
      
        def get_prix_total(self):
            sousTotal=get_sous_prix_total(self)
            
            #total=sousTotal-discounts+tax+delivery
            
            return sousTotal
        return context 
 
class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(OrderItem,id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart")
    
class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(OrderItem,id=kwargs['pk'])
        
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart")

class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(OrderItem,id=kwargs['pk'])
        order_item.delete()
        return redirect('cart')

class CheckoutView(generic.FormView):
    template_name='cart/checkout.html'
    form_class=AddressForm
  
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Vérifie si l'utilisateur est administrateur
            if  request.user.is_staff:
                # Obtient l'URL précédente (ou une URL par défaut si aucune n'est disponible)
                previous_url = request.META.get('HTTP_REFERER', reverse('product-list'))
                return redirect(previous_url)
            else:
                return super().get(request, *args, **kwargs)
        else:
            previous_url = "login" 
            return redirect(previous_url)  
    
    def get_success_url(self):
        return reverse('payment')
    
    def form_valid(self,form):
        order=get_or_set_order_session(self.request)
        
        selected_shipping_address=form.cleaned_data.get('selected_shipping_address')
        selected_billing_address=form.cleaned_data.get('selected_billing_address')
        
        #  S'il ya l'addresse (Shipping Addresse)
        if selected_shipping_address:
            order.shipping_address=selected_shipping_address
        else:
            # On crée un object addresse et on insert les données du formulaire
            address=Address.objects.create(
                user=self.request.user,
                address_line_1=form.cleaned_data.get('shipping_address_line_1'),
                address_line_2=form.cleaned_data.get('shipping_address_line_2'),
                city=form.cleaned_data.get('shipping_zip_code'),
                zip_code=form.cleaned_data.get('shipping_city'),
                address_type='S'
            )    
            order.shipping_address=address
         #  S'il ya l'addresse (Billing Addresse)
        if selected_billing_address:
            order.billing_address=selected_billing_address
        else:
            # On crée un object addresse et on insert les données du formulaire
            address=Address.objects.create(
                user=self.request.user,
                address_line_1=form.cleaned_data.get('billing_address_line_1'),
                address_line_2=form.cleaned_data.get('billing_address_line_2'),
                city=form.cleaned_data.get('billing_zip_code'),
                zip_code=form.cleaned_data.get('billing_city'),
                address_type='B'

            )    
            order.billing_address=address    
            
        # On sauvegarde la commande
        order.save()
            
        messages.info(self.request,"Vous avez ajouté vos adresses avec succès.")
        return super(CheckoutView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs=super(CheckoutView,self).get_form_kwargs()
        kwargs['user_id']=self.request.user.id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CheckoutView,self).get_context_data(**kwargs)
        
        order_items= OrderItem.objects.filter(order=get_or_set_order_session(self.request)).order_by('-id')
        context["order_items"] = order_items
        
        order_price_total=0
        
        for order in order_items:
            order_price_total+=order.get_raw_total_item_price
        
        context["order_price_total"] = order_price_total

        return context
    
class PaymentView(generic.TemplateView):
    template_name = "cart/payment.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Vérifie si l'utilisateur est administrateur
            if  request.user.is_staff:
                # Obtient l'URL précédente (ou une URL par défaut si aucune n'est disponible)
                previous_url = request.META.get('HTTP_REFERER', reverse('product-list'))
                return redirect(previous_url)
            else:
                return super().get(request, *args, **kwargs)
        else:
            previous_url = "login" 
            return redirect(previous_url)  
    
    def get_context_data(self, **kwargs):
        context=super(PaymentView, self).get_context_data(**kwargs)
        context["order"]=get_or_set_order_session(self.request)
        return context

def handler404(request,exception):
    return render(request,'404.html',{},status=404)