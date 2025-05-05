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
    path('add-pet/', views.add_pet, name='add_pet'),
    path('buy/', views.buy_pets, name='buy_pets'),
    path('success/', views.pet_success, name='pet_success'),
    path('payment/<int:pet_id>/', views.payment_view, name='payment'),
    path('adoption/', views.adoption, name='adoption'),
    path('daycare/', views.daycare_view, name='daycare'),
    path('approved-daycare-requests/', views.approved_daycare_requests, name='approved_daycare_requests'),
    path('add_adoption/', views.add_adoption_pet, name='add_adoption'),
    path('adoption/<int:pet_id>/', views.apply_adoption, name='adoption'),
    path('accept-daycare-request/<int:id>/', views.accept_daycare_request, name='accept_daycare_request'),
    path('profile/', views.user_profile, name='user_profile'),
    
]

#for images and files uploaded by users
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
