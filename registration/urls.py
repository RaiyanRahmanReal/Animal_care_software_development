from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin path
    path('admin/', admin.site.urls),
    
    # Authentication paths
    path('', views.signuppage, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('home/', views.homepage, name='home'),
    path('logout/', views.logoutpage, name='logout'),
    
    # Pet-related paths
   
    path('adoption/', views.adoption, name='adoption'),
 
    path('daycare/', views.daycare_view, name='daycare'),
    path('approved-daycare-requests/', views.approved_daycare_requests, name='approved_daycare_requests'),
    path('add_adoption/', views.add_adoption_pet, name='add_adoption'),
    path('adoption/<int:pet_id>/', views.apply_adoption, name='adoption'),

    
]

#for images and files uploaded by users
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
