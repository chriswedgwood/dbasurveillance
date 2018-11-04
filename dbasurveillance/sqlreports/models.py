from django.db import models

# Create your models here.
from dbasurveillance.users.models import User

class Instance(models.Model):
    key = models.AutoField(db_column='InstanceKey', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='InstanceName', max_length=128)  # Field name made lowercase.
    virtual_server_name = models.CharField(db_column='VirtualServerName', max_length=128)  # Field name made lowercase.
    clustered = models.BooleanField(db_column='Clustered')  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=128)  # Field name made lowercase.
    edition = models.CharField(db_column='Edition', max_length=100)  # Field name made lowercase.
    product_level = models.CharField(db_column='ProductLevel', max_length=100)  # Field name made lowercase.
    product_version = models.CharField(db_column='ProductVersion', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimInstances'


class SqlCounter(models.Model):
    key = models.AutoField(db_column='SqlCounterKey', primary_key=True)  # Field name made lowercase.
    instance = models.CharField(db_column='InstanceName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    counter = models.CharField(db_column='SqlCounter', max_length=200, blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='InstanceArea', max_length=200, blank=True, null=True)  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=128, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=128, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Startdate', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimSqlCounters'


class Van(models.Model):
    title = models.CharField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.BooleanField()

    def __str__(self):
        return self.title


class Appointment(models.Model):
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=100,null=True,blank=True)
    van = models.ForeignKey(Van, on_delete=models.SET_NULL, blank=True, null=True,related_name='appointments_by_van')
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='booked_by')
    porters = models.TextField(max_length=1000)
    collection_address = models.TextField(max_length=1000)
    delivery_address = models.TextField(max_length=1000)
    storage = models.TextField(max_length=1000)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " : " + str(self.date)


class DatabaseFiles(models.Model):
    key = models.AutoField(db_column='DatabaseFilesKey', primary_key=True)  # Field name made lowercase.
    instance = models.CharField(db_column='ServerName', max_length=200)  # Field name made lowercase.
    database = models.CharField(db_column='DatabaseName', max_length=200)  # Field name made lowercase.
    logical_file_name = models.CharField(db_column='LogicalFileName', max_length=255)  # Field name made lowercase.
    physical_file_name = models.CharField(db_column='PhysicalFileName', max_length=255)  # Field name made lowercase.
    mount_point = models.CharField(db_column='MountPoint', max_length=500)  # Field name made lowercase.
    application_area = models.CharField(db_column='ApplicationArea', max_length=500)  # Field name made lowercase.
    start_date = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    end_date = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimDatabaseFiles'


class StoredProcedures(models.Model):
    key = models.AutoField(db_column='StoredProcedureKey', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='ProcedureName', max_length=200)  # Field name made lowercase.
    database = models.CharField(db_column='DatabaseName', max_length=200)  # Field name made lowercase.
    instance = models.CharField(db_column='Instancename', max_length=200)  # Field name made lowercase.
    friendly_instance = models.CharField(db_column='FriendlyInstanceName', max_length=200)  # Field name made lowercase.
    friendly_host = models.CharField(db_column='FriendlyHostName', max_length=200)  # Field name made lowercase.
    virtual_server_name = models.CharField(db_column='VirtualServerName', max_length=200)  # Field name made lowercase.
    query_plan = models.TextField(db_column='QueryPlan', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    query_plan_count = models.IntegerField(db_column='QueryPlanCount', blank=True, null=True)  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=200)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimStoredProcedures'
