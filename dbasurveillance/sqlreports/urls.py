from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from . import views



app_name = "instances"
urlpatterns = [

    path("", view=views.InstanceListView.as_view(), name="list"),
    path("<int:pk>/", view=views.InstanceDetailView.as_view(), name="detail"),
    path("cpu/<int:instance_key>/", view=views.cpu_stats, name="plotly_cpu"),
    path("sqlcounters/<int:instance_key>/", view=views.sql_counter_stats, name="json_sqlcounters"),
    path("whoisactive/", view=views.return_who_is_active_data, name="json_who_is_active"),
    path("virtualfilestats/<int:instance_key>/", view=views.virtual_file_stats, name="json_who_is_active"),
    path("waitstats/<int:instance_key>/", view=views.wait_stats, name="json_wait_stats"),
    path("storedprocs_by_db/<int:instance_key>", view=views.storedprocs_by_db, name="storedprocs_by_db"),
    path("procedure_stats/", view=views.procedure_stats, name="procedure_stats"),
    path("sql_counters_by_area/", view=views.sql_counters_by_area, name="sql_counters_by_area"),




]
