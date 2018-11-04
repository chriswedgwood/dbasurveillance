from django.urls import path

from . import views

app_name = "plots"
urlpatterns = [
    path("", view=views.output_json, name="ajax_view"),

]
