from django.db import models
class tbl_district(models.Model):
    districtid = models.AutoField(primary_key=True)
    districtname = models.CharField(max_length=30)

class tbl_location(models.Model):
    locationid = models.AutoField(primary_key=True)
    districtid = models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    locationname = models.CharField(max_length=100)

class tbl_category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=100)
    image = models.ImageField()

class tbl_package(models.Model):
    packageid = models.AutoField(primary_key=True)
    categoryid = models.ForeignKey(tbl_category, on_delete=models.CASCADE,null=True)
    packagename = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    days = models.CharField(max_length=30)


class tbl_service(models.Model):
    serviceid = models.AutoField(primary_key=True)
    packageid = models.ForeignKey(tbl_package, on_delete=models.CASCADE,null=True)
    servicename = models.CharField(max_length=100)
    serviceamount = models.BigIntegerField()



# Create your models here.
