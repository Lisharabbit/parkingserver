
from django.urls import include, path
from django.conf.urls import url
from . import views
from . import models

app_name = 'parkdata'
urlpatterns = [
   
    path('predict',views.predict, name = 'predict'),
    path('lastweekdata',views.lastWeekdata, name = 'lastWeekdata'),
    path('suggestbays',views.suggestbays, name = 'suggestbays'),
]

