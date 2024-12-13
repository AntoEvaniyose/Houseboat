from django.db import models


from Ownerapp.models import tbl_boat
from Guestapp.models import tbl_customer

class tbl_request(models.Model):
    requestid = models.AutoField(primary_key=True)
    requestdate = models.DateField(auto_now_add=True)
    boatid = models.ForeignKey(tbl_boat, on_delete=models.CASCADE, null=True)
    requeststatus = models.CharField(max_length=100)
    customerid = models.ForeignKey(tbl_customer, on_delete=models.CASCADE, null=True)
    requestremark = models.CharField(max_length=100)
    persons = models.IntegerField()
    fromdate = models.DateField()
    todate = models.DateField()
    totalamount=models.BigIntegerField()


class tbl_payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    requestid = models.ForeignKey(tbl_request, on_delete=models.CASCADE, null=True)
    customerid = models.ForeignKey(tbl_customer, on_delete=models.CASCADE, null=True)
    paymentamount = models.BigIntegerField()
    paymentstatus = models.CharField(max_length=100)
    adminamount = models.BigIntegerField(null=True)
# Create your models here.
