from django.db import models

from Adminapp.models import  tbl_location


class tbl_login(models.Model):
    loginId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=25)
    role = models.CharField(max_length=15)
    status = models.CharField(max_length=20)



class tbl_owner(models.Model):
    ownerid = models.AutoField(primary_key=True)
    ownername = models.CharField(max_length=100)
    locationid = models.ForeignKey(tbl_location, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    licenseno = models.BigIntegerField()
    contactno = models.BigIntegerField()
    regdate = models.DateField(auto_now_add=True)
    loginid = models.ForeignKey(tbl_login, on_delete=models.CASCADE)


class tbl_customer(models.Model):
    customerid = models.AutoField(primary_key=True)
    customername = models.CharField(max_length=100)
    housename = models.CharField(max_length=100)
    locationid = models.ForeignKey(tbl_location, on_delete=models.CASCADE)
    pincode = models.IntegerField()
    emailid = models.EmailField(max_length=100)
    phoneno = models.BigIntegerField()
    regdate = models.DateField(auto_now_add=True)
    loginid = models.ForeignKey(tbl_login, on_delete=models.CASCADE)



# Create your models here.
