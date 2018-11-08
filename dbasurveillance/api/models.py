from django.db import models

# Create your models here.


class SqlCounter(models.Model):
    key = models.AutoField(db_column='SqlCounterKey', primary_key=True)  # Field name made lowercase.
    instance = models.CharField(db_column='InstanceName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    counter = models.CharField(db_column='SqlCounter', max_length=200, blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='InstanceArea', max_length=200, blank=True, null=True)  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=128, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Startdate', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimSqlCounters'


class SqlInstance(models.Model):
    key = models.AutoField(db_column='InstanceKey', primary_key=True)  # Field name made lowercase.
    instance = models.CharField(db_column='InstanceName', max_length=128)  # Field name made lowercase.
    virtual_server_name = models.CharField(db_column='VirtualServerName', max_length=128)  # Field name made lowercase.
    clustered = models.BooleanField(db_column='Clustered')  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=128)  # Field name made lowercase.
    edition = models.CharField(db_column='Edition', max_length=100)  # Field name made lowercase.
    product_level = models.CharField(db_column='ProductLevel', max_length=100)  # Field name made lowercase.
    product_version = models.CharField(db_column='ProductVersion', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimInstances'

