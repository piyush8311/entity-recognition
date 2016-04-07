
from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='home'),
  url(r'^result/$', views.result  , name='result'),
]