from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('report',views.report, name='report'),
    path('info', views.info, name='info'),
    path('grades', views.grades, name='grades'),
    path('financial', views.financial, name='financial')   
]