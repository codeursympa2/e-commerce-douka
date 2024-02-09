from django.urls import path
from django.conf.urls import handler404
from .views import *
handler404="cart.views.handler404"
urlpatterns=[
    path("cart", CartView.as_view(), name="cart"),
    path("", ProductListView.as_view(), name="product-list"),
    path("shop/<slug>", ProductDetailView.as_view(), name="product-detail"),
    path("increase-quantity/<pk>", IncreaseQuantityView.as_view(), name="increase-qt"),
    path("decrease-quantity/<pk>", DecreaseQuantityView.as_view(), name="decrease-qt"),
    path("<pk>/delete", RemoveFromCartView.as_view(), name="remove-order-item"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/payment/", PaymentView.as_view(), name="payment"),
    
]