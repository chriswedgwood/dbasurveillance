from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from . import views

app_name = "baselinedata-api"

urlpatterns = [
    path('', views.SqlCounterList.as_view()),
    path('<int:pk>/', views.SqlCounterDetail.as_view()),
    path('cpu/<int:instance_key>', views.CpuView.as_view())
]


