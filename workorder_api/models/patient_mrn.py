from django.db import models


class Mrn(models.Model):
    mrn = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    arabic_first_name = models.CharField(max_length=255,null=True,blank=True)
    arabic_last_name = models.CharField(max_length=255,null=True,blank=True)
    mobile_number = models.CharField(max_length=15,null=True,blank=True)
    language = models.CharField(max_length=100,null=True,blank=True)
    ward_code = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = 'workorder_api_mrn'
    