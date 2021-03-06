# Generated by Django 2.0.6 on 2018-09-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlreports', '0009_auto_20180702_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseFiles',
            fields=[
                ('key', models.AutoField(db_column='DatabaseFilesKey', primary_key=True, serialize=False)),
                ('instance', models.CharField(db_column='ServerName', max_length=200)),
                ('database', models.CharField(db_column='DatabaseName', max_length=200)),
                ('logical_file_name', models.CharField(db_column='LogicalFileName', max_length=255)),
                ('physical_file_name', models.CharField(db_column='PhysicalFileName', max_length=255)),
                ('mount_point', models.CharField(db_column='MountPoint', max_length=500)),
                ('application_area', models.CharField(db_column='ApplicationArea', max_length=500)),
                ('start_date', models.DateTimeField(db_column='StartDate')),
                ('end_date', models.DateTimeField(blank=True, db_column='EndDate', null=True)),
            ],
            options={
                'db_table': 'DimDatabaseFiles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SqlCounter',
            fields=[
                ('key', models.AutoField(db_column='SqlCounterKey', primary_key=True, serialize=False)),
                ('instance', models.CharField(blank=True, db_column='InstanceName', max_length=200, null=True)),
                ('counter', models.CharField(blank=True, db_column='SqlCounter', max_length=200, null=True)),
                ('area', models.CharField(blank=True, db_column='InstanceArea', max_length=200, null=True)),
                ('node', models.CharField(blank=True, db_column='Node', max_length=128, null=True)),
                ('category', models.CharField(blank=True, db_column='Category', max_length=128, null=True)),
                ('start_date', models.DateField(blank=True, db_column='Startdate', null=True)),
                ('end_date', models.DateField(blank=True, db_column='EndDate', null=True)),
            ],
            options={
                'db_table': 'DimSqlCounters',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StoredProcedures',
            fields=[
                ('key', models.AutoField(db_column='StoredProcedureKey', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='ProcedureName', max_length=200)),
                ('database', models.CharField(db_column='DatabaseName', max_length=200)),
                ('instance', models.CharField(db_column='Instancename', max_length=200)),
                ('friendly_instance', models.CharField(db_column='FriendlyInstanceName', max_length=200)),
                ('friendly_host', models.CharField(db_column='FriendlyHostName', max_length=200)),
                ('virtual_server_name', models.CharField(db_column='VirtualServerName', max_length=200)),
                ('query_plan', models.TextField(blank=True, db_column='QueryPlan', null=True)),
                ('query_plan_count', models.IntegerField(blank=True, db_column='QueryPlanCount', null=True)),
                ('node', models.CharField(db_column='Node', max_length=200)),
                ('startdate', models.DateTimeField(db_column='StartDate')),
                ('enddate', models.DateTimeField(blank=True, db_column='EndDate', null=True)),
            ],
            options={
                'db_table': 'DimStoredProcedures',
                'managed': False,
            },
        ),
    ]
