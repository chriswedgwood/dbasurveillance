# Create your views here.
import pyodbc

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from dbasurveillance.sqlreports.views import unpack_dates
from .models import SqlCounter
from .serializers import SqlCounterSerializer


class SqlCounterList(generics.ListAPIView):
    queryset = SqlCounter.objects.all()
    serializer_class = SqlCounterSerializer


class SqlCounterDetail(generics.RetrieveAPIView):
    queryset = SqlCounter.objects.all()
    serializer_class = SqlCounterSerializer

def return_data_frame_from_procedure(request, stored_procedure):
    frames = []
    conn = pyodbc.connect(settings.PANDAS_CONNECTION_STRING)
    date_ranges = unpack_dates(request)
    sp_call = '{ CALL '+stored_procedure+' (?,?,?,?)}'
    for i, date_range in enumerate(date_ranges):
        params = (1, date_range[0], date_range[1], str(i))
        sql = sp_call
        df = pd.read_sql(sql=sql, con=conn, params=params)
        frames.append(df)

    return pd.concat(frames)
class CpuView(APIView):


    def get(self, request):
        return Response({'some': 'data'})
