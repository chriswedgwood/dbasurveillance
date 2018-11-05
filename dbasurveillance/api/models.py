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
