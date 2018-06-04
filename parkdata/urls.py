
from django.urls import include, path
from django.conf.urls import url
from . import views
from . import models

app_name = 'parkdata'
urlpatterns = [
   
    path('predict',views.predict, name = 'predict'),# url for visualise predicted data
    path('lastweekdata',views.lastWeekdata, name = 'lastWeekdata'),# url for visualise historical data
    path('suggestbays',views.suggestbays, name = 'suggestbays'),# url for recommend parking lots
]

