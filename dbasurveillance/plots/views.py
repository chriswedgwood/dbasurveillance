from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.db import connection

def my_custom_sql():
    cursor = connection.cursor()
    cursor.execute("SELECT   InstanceName,SqlServer,SystemIdle,Other,CaptureDateTime\
  FROM [DBADW].[dbo].[FactCPU] F \
  JOIN [DBADW].[dbo].[DimInstances] D ON F.[InstanceKey]= D.InstanceKey\
  WHERE sqlserver>0\
  Order by InstanceName,Capturedatetime asc")
    row = cursor.fetchall()
    return row


def output_json(request):
    data = []
    results = my_custom_sql()
    instances = [result[0] for result in results]
    instance_set = set(instances)
    for instance in instance_set:
        trace = {"type": 'line', "mode": "lines", "name": str(instance)}
        trace["x"] = [result[4].strftime("%Y-%m-%d %H:%M:%S") for result in results if result[0] == instance]
        trace["y"] = [result[1] for result in results if result[0] == instance]
        data.append(trace)

    return JsonResponse(data, safe=False)



