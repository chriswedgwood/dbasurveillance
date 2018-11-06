# Create your views here.
import pyodbc

from django.conf import settings
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from dbasurveillance.sqlreports.views import unpack_dates
from .models import SqlCounter
from .serializers import SqlCounterSerializer
from django.http import JsonResponse
import pandas as pd
conn = pyodbc.connect(settings.PANDAS_CONNECTION_STRING)


class SqlCounterList(generics.ListAPIView):
    queryset = SqlCounter.objects.all()
    serializer_class = SqlCounterSerializer


class SqlCounterDetail(generics.RetrieveAPIView):
    queryset = SqlCounter.objects.all()
    serializer_class = SqlCounterSerializer


def return_data_frame_from_procedure(request, stored_procedure):
    frames = []

    date_ranges = unpack_dates(request)
    sp_call = '{ CALL '+stored_procedure+' (?,?,?,?)}'
    for i, date_range in enumerate(date_ranges):
        params = (1, date_range[0], date_range[1], str(i))
        sql = sp_call
        df = pd.read_sql(sql=sql, con=conn, params=params)
        frames.append(df)

    return pd.concat(frames)


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

        return JsonResponse(data, safe=False)


def cpu_by_instance(request, instance_key):
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
