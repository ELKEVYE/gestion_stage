from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Admin_profile import views
urlpatterns = [
    # Inclure les URLs de l'application Admin_profile
    path('', views.loginPage, name='login'),  
    # path('logout/', views.logout, name = 'logout'),
    # path('homePage/', views.homePage, name = 'acceuilPage'),
    path("", include("Admin_profile.urls")),  # Redirige vers Admin_profile.urls
     path("", include("stages.urls")), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
