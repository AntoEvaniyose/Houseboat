from django.urls import path
from Customerapp import views

urlpatterns = [
    path('customerhome/', views.customerhome, name='customerhome'),
    path('categoryview/', views.categoryview, name='categoryview'),
    path('packageview/<id>/', views.packageview, name='packageview'),
    path('serviceview/<id>/', views.serviceview, name='serviceview'),
    path('viewboat/<id>', views.viewboat, name='viewboat'),
    path('boatdetails/<id>', views.boatdetails, name='boatdetails'),
    path('requestdetails/<id>/<pa>/<sa>/<am>/', views.requestdetails, name='requestdetails'),
    path('myorders/', views.myorders, name='myorders'),
    path('payment/<id>/', views.payment, name='payment'),
    path('logout/', views.logout, name='logout'),
    path('customerprofile/', views.customerprofile, name='customerprofile'),
    path('editcustomerprofile/<id>/', views.editcustomerprofile, name='editcustomerprofile'),
    path('custlocation',views.custlocation,name='custlocation'),
    path('changepassword',views.changepassword,name='changepassword'),

]
