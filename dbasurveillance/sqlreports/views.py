from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
import pandas as pd
from pandas import DataFrame
from dbasurveillance.sqlreports.models import Instance, SqlCounter, DatabaseFiles, StoredProcedures
from .forms import NameForm, ParentForm
from dbasurveillance.users.models import User
from rest_framework import viewsets
from dbasurveillance.sqlreports.serializers import UserSerializer

from django.conf import settings

import pyodbc

# !/usr/bin/env python3
from datetime import datetime, timedelta

VIRTUAL_FILE_STATS = ["TotalReads", "TotalWrites", "AverageReadLatencyMs", "AverageWriteLatencyMs"]


class InstanceListView(ListView):
    model = Instance


class InstanceDetailView(DetailView):
    model = Instance

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        start_date_a = self.request.GET.get('start_date_a', None)
        end_date_a = self.request.GET.get('end_date_a', None)
        start_date_b = self.request.GET.get('start_date_b', None)
        end_date_b = self.request.GET.get('end_date_b', None)

        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        context["form"] = NameForm()
        categories = SqlCounter.objects.filter(instance=self.object.name, area='instance').values('category','area').distinct()
        counters = SqlCounter.objects.filter(instance=self.object.name, area='instance').values('counter','category','area').distinct()
        context["instance_areas"] = SqlCounter.objects.filter(instance=self.object.name).values('area').distinct()
        context["databases"] = DatabaseFiles.objects.filter(instance=self.object.name).values('database').distinct()
        context["virtual_file_stats"] = VIRTUAL_FILE_STATS
        context["procedures"] = StoredProcedures.objects.filter(instance=self.object.name).values('name').distinct()
        context["ParentForm"] = ParentForm(
            initial={'start_date_a': start_date_a, 'end_date_a': end_date_a, 'start_date_b': start_date_b,
                     'end_date_b': end_date_b})

        counters_by_category = {category['category']: [] for category in categories}
        for counter in counters:
            counters_by_category[counter['category']].append(counter['counter'])

        context["counters_by_category"] = counters_by_category

        return context


def calculate_date_for_report(input_date, primary_date, delta=0):
    if primary_date and not input_date:
        date = datetime.today() - timedelta(days=delta)
        return date.strftime('%Y-%m-%d %H:%M:%S')

    if not primary_date and not input_date:
        return None

    return input_date


def unpack_dates(request):
    start_date_a = calculate_date_for_report(request.GET.get('start_date_a'),  True, 90)
    end_date_a = calculate_date_for_report(request.GET.get('end_date_a'), True, 0)
    start_date_b = calculate_date_for_report(request.GET.get('start_date_b'), False)
    end_date_b = calculate_date_for_report(request.GET.get('end_date_b'), False)

    if start_date_b is None:
        return [(start_date_a, end_date_a)]

    return [(start_date_a, end_date_a), (start_date_b, end_date_b)]


def cpu_stats(request, instance_key):
    data = []
    frames = []
    conn = pyodbc.connect(settings.PANDAS_CONNECTION_STRING)
    date_ranges = unpack_dates(request)
    sp_call = '{ CALL ' + 'CpuDataByTimeFrame' + ' (?,?,?,?)}'
    for i, date_range in enumerate(date_ranges):
        params = (instance_key, date_range[0], date_range[1], str(i))
        sql = sp_call
        df = pd.read_sql(sql=sql, con=conn, params=params)
        frames.append(df)

    df_results = pd.concat(frames)
    windows = list(df_results.Trace.unique())

    x_column = 'TimeMins'
    if len(windows) == 1:
        df_results["CaptureDateTime"] = df_results['CaptureDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        x_column = 'CaptureDateTime'

    for window in windows:
        df_window = df_results[df_results['Trace'] == window]

        for i, column in enumerate(df_window):
            if i >= 3:
                trace = {"type": 'line', "mode": "lines", "name": column+window}
                trace["x"] = list(df_window[x_column])
                trace["y"] = list(df_window[column])
                data.append(trace)
    return JsonResponse(data, safe=False)


def sql_counter_stats(request, instance_key):
    data = []
    frames = []
    conn = pyodbc.connect(settings.PANDAS_CONNECTION_STRING)
    date_ranges = unpack_dates(request)
    sp_call = '{ CALL ' + 'SqlCountersByTimeFrame' + ' (?,?,?,?)}'
    for i, date_range in enumerate(date_ranges):
        params = (instance_key, date_range[0], date_range[1], str(i))
        sql = sp_call
        df = pd.read_sql(sql=sql, con=conn, params=params)
        frames.append(df)

    df_results = pd.concat(frames)
    windows = list(df_results.Trace.unique())

    x_column = 'TimeMins'
    if len(windows) == 1:
        df_results["CaptureDateTime"] = df_results['CaptureDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        x_column = 'CaptureDateTime'

    for window in windows:
        df_window = df_results[df_results['Trace'] == window]

        for i, column in enumerate(df_window):
            if i >= 3:
                trace = {"type": 'line', "mode": "lines", "name": column+window}
                trace["x"] = list(df_window[x_column])
                trace["y"] = list(df_window[column])
                data.append(trace)
    return JsonResponse(data, safe=False)





def get_sql_counters_data_frame(instance_key, sql_counters):
    sql_counters = sql_counters or list(SqlCounter.objects.order_by().values_list('counter', flat=True).distinct())
    query_counters = "'" + "','".join(sql_counters) + "'"

    sql = '''select F.CaptureDate,SC.SqlCounter,SC.InstanceArea,F.value from [DBADW].[dbo].[DimInstances] I
                      JOIN [DBADW].[dbo].[FactSQLCounters] F ON F.InstanceKey=I.InstanceKey
                      JOIN [DBADW].[dbo].[DimSqlCounters] SC ON Sc.SqlCounterKey = F.SqlCounterKey
                      Where  1=1 and InstanceArea = 'Instance' and  I.InstanceKey=%s and SC.SqlCounter in (%s)''' % (instance_key, query_counters)
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    df = DataFrame(row)
    df.columns = ['CaptureDate', 'SqlCounter', 'InstanceArea', 'Value']
    return df


def return_sql_counters_data(request, instance_key):
    data = []
    sql_counters = request.POST.getlist('multiselect[]')
    df_results = get_sql_counters_data_frame(instance_key, sql_counters)

    df_instance_counter = df_results[['SqlCounter', 'InstanceArea']].drop_duplicates()
    df_results["CaptureDate"] = df_results['CaptureDate'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    for counter in df_results.SqlCounter.unique():
        if counter in sql_counters:
            df_counter = df_results.loc[df_results['SqlCounter'] == counter]
            trace = {"type": 'line', "mode": "lines", "name": counter}
            trace["x"] = list(df_counter["CaptureDate"])
            trace["y"] = list(df_counter["Value"])
            data.append(trace)

    return JsonResponse(data, safe=False)


def rounded_to_the_last_5_minute_epoch(date):
    rounded = date - (date - datetime.min) % timedelta(minutes=5)
    return rounded


def get_who_is_active_data_frame(date, instance_key):
    cursor = connection.cursor()
    if len(date) > 16:
        date_time_in = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        date += ':00'
        date_time_in = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    date_to_5 = rounded_to_the_last_5_minute_epoch(date_time_in)
    cursor.execute('''SELECT REPLACE(REPLACE(ParentSqlText,'<?query --',''),'--?>','') ParentSqlText, REPLACE(REPLACE(SqlText,'<?query --',''),'--?>','')  
                      SqlText,F.CaptureDatetime,F.cnt, [max_cpu], [max_tempdb], [reads], [writes], [physical_reads], [BlockedSessionCount] 
                      FROM [DBADW].[dbo].[FactWhoIsActive] F JOIN [DBADW].[dbo].[DimWhoIsActive] D
                      On F.Whokey = D.Whokey
                      WHERE InstanceKey=%s and  CaptureDateTime = %s ''', [instance_key, date_to_5])
    row = cursor.fetchall()
    df = DataFrame(row)
    return df


@csrf_exempt
def return_who_is_active_data(request):
    data = []
    df_results = get_who_is_active_data_frame(request.GET['date'], request.GET['instance'])
    # data.append([list(df_results)])
    data.append(list(df_results.values.tolist()))

    return JsonResponse(data, safe=False)


def get_virtual_file_stats_from_sql(instance_key):
    cursor = connection.cursor()
    cursor.execute('''SELECT   CaptureDate CaptureDateTime  ,DatabaseName ,SUM(NumofReads) TotalReads,SUM(NumofWrites) TotalWrites,
                      AVG(MsPerRead) AverageReadLatencyMs,AVG(MsPerWrite) AverageWriteLatencyMs
                      FROM [DBADW].[dbo].[FactVirtualFileStats] F 
                      JOIN [DBADW].[dbo].DimDataBaseFiles D ON D.DatabaseFilesKey=F.FileKey
                      WHERE InstanceKey = %s
                      GROUP BY CaptureDate ,DatabaseName
                      ORDER BY CaptureDate''', [instance_key])
    row = cursor.fetchall()
    df = DataFrame(row)
    df.columns = [columns[0] for columns in cursor.description]
    df["CaptureDateTime"] = df['CaptureDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    return df


def virtual_file_stats(request, instance_key):
    data = []
    df_results = get_virtual_file_stats_from_sql(instance_key)
    databases = request.POST.getlist('multiselect[]') or df_results.DatabaseName.unique()
    virtual_file_stats_dropdown = request.POST.getlist('multiselect2[]') or VIRTUAL_FILE_STATS
    columns_to_exclude = list(set(VIRTUAL_FILE_STATS) - set(virtual_file_stats_dropdown))
    for database in databases:
        for i, column in enumerate(df_results):
            if i >= 2 and column in virtual_file_stats_dropdown:
                trace = {"type": 'line', "mode": "lines", "name": database + '-' + column}
                df_database = df_results.loc[df_results['DatabaseName'] == database]
                trace["x"] = list(df_database["CaptureDateTime"])
                trace["y"] = list(df_database[column])
                data.append(trace)
    return JsonResponse(data, safe=False)


def wait_stats(request, instance_key):
    data = []
    cursor = connection.cursor()
    cursor.execute('''SELECT   A.Capturedate CaptureDateTime,B.WaitStat,CASt(Round((A.waitms*1.0/SQ.TotalWaitMs*1.0)*100,0) as INT) WaitPercentAge
                      FROM [DBADW].[dbo].[FactWaitStats] A
                      JOIn [DBADW].[dbo].[DimWaitStats] B ON B.WaitStatsKey=A.WaitStatsKey
                      LEFT JOIN (  select capturedate,InstanceKey, SUM([WaitMs]) TotalWaitMs
                      FROM [DBADW].[dbo].[FactWaitStats] A
                      GROUP By  capturedate,InstanceKey) SQ
                      ON SQ.capturedate=A.capturedate and SQ.InstanceKey = A.InstanceKey
                      WHERE A.InstanceKey = %s
                      order by A.capturedate desc''', [instance_key])
    row = cursor.fetchall()
    df = DataFrame(row)
    df.columns = [columns[0] for columns in cursor.description]
    df["CaptureDateTime"] = df['CaptureDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    capture_date_times = df.CaptureDateTime.unique()
    waits = df.WaitStat.unique()
    for wait in waits:
        df_waits = df.loc[df['WaitStat'] == wait]
        trace = {"type": 'bar', "name": wait}
        trace["x"] = list(df_waits['CaptureDateTime'])
        trace["y"] = list(df_waits['WaitPercentAge'])
        data.append(trace)
    return JsonResponse(data, safe=False)


def storedprocs_by_db(request, instance_key):
    database = request.GET['database_name']
    instance = Instance.objects.get(key=instance_key).name
    procedures = StoredProcedures.objects.filter(database=database, instance=instance).order_by('name')
    response = ''
    for procedure in procedures:
        response += '<option value="' + str(procedure.key) + '">' + procedure.name + '</option>'
    data = {'key': instance_key}
    return HttpResponse(response)


def procedure_stats(request):
    procedure_key = request.POST.getlist('procedure[]')[0]
    data = []
    cursor = connection.cursor()
    cursor.execute('''SELECT CaptureDate CaptureDateTime,D.ProcedureName,F.ExecutionCount,F.TotalElapsedTime/F.ExecutionCount/1000 AvgExecutionTimeMs ,
                      F.TotalLogicalReads/F.ExecutionCount AvgLogicalReads,F.TotalLogicalWrites/F.ExecutionCount AvgLogicalWrites,F.TotalPhysicalReads/F.ExecutionCount AvgPhysicalReads
                      FROM [DBADW].[dbo].[FactStoredProcedures] F 
                      JOIN [DBADW].[dbo].[DimStoredProcedures] D
                      ON F.StoredProcedureKey=D.StoredProcedureKey
                      Where D.StoredProcedureKey = %s 
                      Order by 1 asc''', [procedure_key])
    row = cursor.fetchall()
    df = DataFrame(row)
    df.columns = [columns[0] for columns in cursor.description]
    df["CaptureDateTime"] = df['CaptureDateTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    for i, column in enumerate(df):
        if i >= 2:
            trace = {"type": 'scatter', "name": column}
            trace["x"] = list(df["CaptureDateTime"])
            trace["y"] = list(df[column])
            # trace["marker"] = {'size': list(df["ExecutionCount"])}
            data.append(trace)

    return JsonResponse(data, safe=False)


def sql_counters_by_area(request):
    areas = request.POST.getlist('multiselectSqlCounterInstanceArea[]') or SqlCounter.objects.filter(instance=1).values(
        'area').distinct()
    counters = SqlCounter.objects.filter(area__in=areas).values('counter').distinct()
    response = ''
    for counter in counters:
        response += '<option value="' + counter['counter'] + '">' + counter['counter'] + '</option>'
    return HttpResponse(response)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
