from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from . import views

app_name = "baselinedata-api"

urlpatterns = [
    path('react-select-sql-counters', views.SqlCounterList.as_view()),
    path('instances/', views.SqlInstanceList.as_view()),
    path('cpu/<int:instance_key>', views.CpuView.as_view()),
    path('waitstats/<int:instance_key>', views.WaitStatsView.as_view()),
    path("sqlcounters/<int:instance_key>/", view=views.SqlCounterStatsView.as_view()),
    path("whoisactive/", view=views.WhoIsActiveView.as_view()),

]


