from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getData/$', views.get_data, name='get_data'),
    url(r'^call-api/$', views.call_api, name='call_api'),
    url(r'^addData/$', views.add_data, name='add_data'),
    url(r'^editData/(?P<id>\d+)/$', views.edit_data, name='edit_data'),
    url(r'^hapusData/(?P<id>\d+)/$', views.hapus_data, name='hapus_data'),
]
