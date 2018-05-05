
from django.urls import include, path
from django.conf.urls import url
from . import views
from . import models

app_name = 'parkdata'
urlpatterns = [
    # path('', views.index, name='index'),
    path('predict',views.predict, name = 'predict'),
    path('<int:parkingdata_id>/', views.detail, name='detail'),
    # path('detail/',views.detail,name = 'detial'),
    # path('search/', view.search,),
    # path('runJob/',views.runJob),
    url(r'^runJob/$',views.run_job),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# from django.conf.urls import url
# from Api import views
#
# urlpatterns = [
#     url(r'^runJob/$',views.run_job),
# ]

# Serializers define the API representation.


# Routers provide an easy way of automatically determining the URL conf.

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
