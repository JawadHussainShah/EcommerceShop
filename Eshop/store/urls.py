from django.contrib import admin
from django.urls import path
from store import views


urlpatterns = [
    path('', views.index,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.product_cart, name='cart'),
    path('check-out', views.checkout, name='checkout'),
    path('orders/', views.view_orders, name='orders'),
    path('profile/',views.profile, name='profile'),
    path('changepass/',views.change_pass, name='changepassword'),
    path('email/<str:user>/',views.email_confirm, name='emailconfirm'),
    ]

