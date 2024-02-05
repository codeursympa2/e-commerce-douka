from django.db import models
from django.contrib.auth import get_user_model

#
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.shortcuts import reverse

from ckeditor.fields import RichTextField

from bleach import clean

User=get_user_model()

class Address(models.Model):
    ADDRESS_CHOICES=(
        ('B','Billing'),
        ('S','Shipping'),
    )
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=150)
    address_line_2=models.CharField(max_length=150)
    city=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)
    address_type=models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.zip_code}"

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

class ColourVariation(models.Model):
    
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SizeVariation(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    
   title = models.CharField(max_length=40)
   slug = models.SlugField(unique=True)
   desc = RichTextField()
   price= models.IntegerField(default=0)
   image = models.ImageField(upload_to='product_images')
   created = models.DateTimeField(auto_now_add=True)
   updated=models.DateTimeField(auto_now=True)
   active = models.BooleanField(default=False)
   avalaible_colours=models.ManyToManyField(ColourVariation,)
   avalaible_sizes=models.ManyToManyField(SizeVariation)
   
   def __str__(self):
       return self.title
   #Redirection avec url [slug]
   def get_absolute_url(self):
       return reverse("product-detail",kwargs={'slug':self.slug})
   def get_price(self):
       return  self.price
   
   class Meta:
        ordering = ['-id']

class OrderItem(models.Model):
    
    quantity=models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order=models.ForeignKey("Order",related_name="item",on_delete=models.CASCADE)
    colour = models.ForeignKey(ColourVariation, on_delete=models.CASCADE)
    size=models.ForeignKey(SizeVariation, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    
    @property
    def get_raw_total_item_price(self):
        return self.quantity * self.product.price
    @property
    def get_prix_unitaire(self):
        return self.product.price
    @property
    def get_total_item_price(self):
        return self.get_row_total_item_price
    

class Order(models.Model):
    
    user=models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=True)
    ordered_date=models.DateField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    
    billing_address=models.ForeignKey(Address, related_name='billing_address',blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address=models.ForeignKey(Address, related_name='shipping_address',blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.reference_number
    
    class Meta:
        managed = True
        verbose_name = 'order'
        verbose_name_plural = 'orders'
    
    @property
    def reference_number(self):
         return f"ORDERS-{self.pk}"
     
    @property
    def get_raw_subtotal(self):
        total=0
        for order_item in self.item.all():
            total+=order_item.get_raw_total_item_price
            
        # Convertir le total en chaîne de caractères avec le format décimal
        return '{:.2f}'.format(total * 0.0020)
    
    # def get_sub_total(self):
    #     subtotal=self.get_raw_subtotal()
    #     return subtotal
            

   
class Payment(models.Model):
    
    order=models.ForeignKey(Order,related_name='payment', on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=20,choices=(
        ('P','Paypal'),
        ('O','Orange Money')
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    succesful=models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.reference_number
    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"

#On s'assure de la transformation du champs slug en slug.
def pre_save_product_receiver(sender,instance, *args, **kwargs):
    if not instance.slug: 
        instance.slug=slugify(instance.title)

#Avant chaque enregistrement d'un produit.
pre_save.connect(pre_save_product_receiver,sender=Product) 
