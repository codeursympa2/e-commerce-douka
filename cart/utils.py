from .models import Order
#Sauvegarde ou recupération de la commande en session
def get_or_set_order_session(request):  
    #Récupération
    order_id= request.session.get("order_id",None)
    order=Order()
    
    if order_id is None:
        #Insertion
        order.save()
        request.session['order_id']=order.id
    else:
        try:
            order=Order.objects.get(id=order_id,ordered=False)
        except Order.DoesNotExist:
            #Insertion
            order.save()
            request.session['order_id']= order.id
            
    #On ajoute l'utilisateur courant a la commande       
    if request.user.is_authenticated and order.user is None:
        order.user=request.user
        order.save()
        
    return order