from django.db import models

from Adminapp.models import tbl_package, tbl_service, tbl_category
from Guestapp.models import tbl_login


class tbl_boat(models.Model):
    boatid = models.AutoField(primary_key=True)
    categoryid = models.ForeignKey(tbl_category, on_delete=models.CASCADE, null=True)
    packageid = models.ForeignKey(tbl_package, on_delete=models.CASCADE)
    serviceid = models.ForeignKey(tbl_service, on_delete=models.CASCADE)
    boatname = models.CharField(max_length=30,null=True)
    loginid = models.ForeignKey(tbl_login, on_delete=models.CASCADE, default=None)
    boatamount = models.BigIntegerField(default=None)
    regdate = models.DateField(auto_now_add=True)
    boatimage = models.ImageField()

# Create your models here.
