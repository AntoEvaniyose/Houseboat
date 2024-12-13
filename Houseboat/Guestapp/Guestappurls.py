from django.urls import path
from Guestapp import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
    path('ownerreg/', views.ownerreg, name='ownerreg'),
    path('selectlocation/', views.selectlocation, name='selectlocation'),
    path('customerreg/', views.customerreg, name='customerreg'),
    path('selectlocation/', views.selectlocation, name='selectlocation'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),

]
