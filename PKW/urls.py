from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',  views.main, name='main'),
    url(r'^login/$', views.loguj),
    url(r'^zalogowany/$', views.zalogowany),
    url(r'^filtr/$', views.filtr),
    url(r'^wyloguj/$', views.wyloguj),
    url(r'^edytuj/$', views.edytuj),
    url(r'^data_edycja/$', views.data_edycji),
]