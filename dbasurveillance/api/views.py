# Create your views here.
import pyodbc

from django.conf import settings
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from dbasurveillance.sqlreports.views import unpack_dates
from .models import SqlCounter, SqlInstance
from .serializers import SqlCounterSerializer,SqlInstanceSerializer
from django.http import JsonResponse
import pandas as pd
conn = pyodbc.connect(settings.PANDAS_CONNECTION_STRING)
from datetime import datetime, timedelta

class SqlCounterList(generics.ListAPIView):

    serializer_class = SqlCounterSerializer

    def get_queryset(self):
        queryset = SqlCounter.objects.filter(instance='TDC2FAEC03V01\VINS001',area='Instance')
        return queryset


class SqlInstanceList(generics.ListAPIView):
    queryset = SqlInstance.objects.all()
    serializer_class = SqlInstanceSerializer


class CpuView(View):

    def get(self, request, instance_key):
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
        df_results['customdata'] = instance_key
        windows = list(df_results.Trace.unique())

        x_column = 'TimeMins'
        if len(windows) == 1:
            df_results["CaptureDateTime"] = df_results['CaptureDateTime'].apply(
                lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            x_column = 'CaptureDateTime'

        for window in windows:
            df_window = df_results[df_results['Trace'] == window]

            for i, column in enumerate(df_window):
                if i >= 3 and column != 'customdata':
                    trace = {"type": 'line', "mode": "lines", "name": column + window}
                    trace["x"] = list(df_window[x_column])
                    trace["y"] = list(df_window[column])
                    trace["customdata"] = list(df_results['customdata'])


                    data.append(trace)

        return JsonResponse(data, safe=False)


class SqlCounterStatsView(View):

    def get(self, request, instance_key):
        data = []
        frames = []
        sql_counters = self.request.GET.getlist('sqlCounters[]') or []
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
            df_results["CaptureDateTime"] = df_results['CaptureDateTime'].apply(
                lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            x_column = 'CaptureDateTime'

        for window in windows:
            df_window = df_results[df_results['Trace'] == window]

            for i, column in enumerate(df_window):
                if i >= 3:
                    trace = {"type": 'line', "mode": "lines", "name": column + window}
                    trace["x"] = list(df_window[x_column])
                    trace["y"] = list(df_window[column])
                    data.append(trace)


        data = []
        df_instance_counter = df_results[['SqlCounter', 'InstanceArea']].drop_duplicates()

        for counter in df_results.SqlCounter.unique():
            if counter in sql_counters or len(sql_counters) == 0:
                df_counter = df_results.loc[df_results['SqlCounter'] == counter]
                trace = {"type": 'line', "mode": "lines", "name": counter}
                trace["x"] = list(df_counter["CaptureDateTime"])
                trace["y"] = list(df_counter["Value"])
                data.append(trace)

        return JsonResponse(data, safe=False)


class WaitStatsView(View):

    def get(self, request, instance_key):
        data = []

        sql = '''SELECT   A.Capturedate CaptureDateTime,B.WaitStat,CASt(Round((A.waitms*1.0/SQ.TotalWaitMs*1.0)*100,0) as INT) WaitPercentAge
                              FROM [DBADW].[dbo].[FactWaitStats] A
                              JOIn [DBADW].[dbo].[DimWaitStats] B ON B.WaitStatsKey=A.WaitStatsKey
                              LEFT JOIN (  select capturedate,InstanceKey, SUM([WaitMs]) TotalWaitMs
                              FROM [DBADW].[dbo].[FactWaitStats] A
                              GROUP By  capturedate,InstanceKey) SQ
                              ON SQ.capturedate=A.capturedate and SQ.InstanceKey = A.InstanceKey
                              WHERE A.InstanceKey = ?
                              order by A.capturedate desc'''
        params = [instance_key]
        df = pd.read_sql_query(sql=sql, con=conn, params=params)

       # df.columns = [columns[0] for columns in cursor.description]
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


class WhoIsActiveView(View):

    def rounded_to_the_last_5_minute_epoch(self, date_in):
        rounded = date_in - (date_in - datetime.min) % timedelta(minutes=5)
        return rounded

    def get(self, request):
        date = request.GET['date']
        instance_key = request.GET['instance_key']
        data = []
        if len(date) > 16:
            date_time_in = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            date += ':00'
            date_time_in = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        date_to_5 = self.rounded_to_the_last_5_minute_epoch(date_time_in)
        sql = '''SELECT REPLACE(REPLACE(ParentSqlText,'<?query --',''),'--?>','') ParentSqlText, REPLACE(REPLACE(SqlText,'<?query --',''),'--?>','')  
                              SqlText,F.CaptureDatetime,F.cnt, [max_cpu], [max_tempdb], [reads], [writes], [physical_reads], [BlockedSessionCount] 
                              FROM [DBADW].[dbo].[FactWhoIsActive] F JOIN [DBADW].[dbo].[DimWhoIsActive] D
                              On F.Whokey = D.Whokey
                              WHERE InstanceKey=? and  CaptureDateTime = ? '''

        params = [instance_key, date_to_5]
        df = pd.read_sql_query(sql=sql, con=conn, params=params)
        data.append(list(df.values.tolist()))
        return JsonResponse(data, safe=False)