
from django.contrib import admin
from django.urls import path,include

from django.conf import settings;
from django.conf.urls.static import static
from core import views
urlpatterns = [
    path('darini/', admin.site.urls,name="darini"),
    path('home',views.HomeView.as_view(),name="home"),
    path('contact',views.ContactView.as_view(),name="contact"),
    path('',include('cart.urls')),
    path('auth/',include('utilisateurs.urls')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)