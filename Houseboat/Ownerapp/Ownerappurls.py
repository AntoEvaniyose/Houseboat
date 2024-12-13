from django.urls import path
from Ownerapp import views

urlpatterns = [
   path('', views.ownerhome,name='ownerhome'),
   path('boatreg/', views.boatreg, name='boatreg'),
   path('viewboat/', views.viewboat, name='viewboat'),
   path('editboat/<id>/', views.editboat, name='editboat'),
   path('fillcategory/', views.fillcategory, name='fillcategory'),
   path('deleteboat/<id>/', views.deleteboat, name='deleteboat'),
   path('choosepackage/', views.choosepackage, name='choosepackage'),
   path('chooseservices/', views.chooseservices, name='chooseservices'),
   path('editchoosepackage/', views.editchoosepackage, name='editchoosepackage'),
   path('editchooseservices/', views.editchooseservices, name='editchooseservices'),
   path('requestbycustomers/', views.requestbycustomers, name='requestbycustomers'),
   path('verifycustomer/<id>', views.verifycustomer, name='verifycustomer'),
   path('rejectcustomer/<id>', views.rejectcustomer, name='rejectcustomer'),
   path('viewacceptedcustomers/', views.viewacceptedcustomers, name='viewacceptedcustomers'),
   path('rejectedcustomers/<id>', views.rejectedcustomers, name='rejectedcustomers'),
   path('paymentview/', views.paymentview, name='paymentview'),
   path('logout/', views.logout, name='logout'),
   path('ownerchangepassword',views.ownerchangepassword,name='ownerchangepassword'),
   path('ownerprofile/', views.ownerprofile, name='ownerprofile'),
   path('editownerprofile/<id>', views.editownerprofile, name='editownerprofile'),
   path('ownlocation/', views.ownlocation, name='ownlocation'),



]