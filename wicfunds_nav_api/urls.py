from django.conf.urls import url
from . import views

app_name = 'wicfunds_nav_api'

urlpatterns = [
    url('get_arb_performance$', views.get_arb_performance, name='get_arb_performance'),
    url('get_aed_performance$', views.get_aed_performance, name='get_aed_performance'),
    url('get_taco_performance$', views.get_taco_performance, name='get_taco_performance'),
    url('get_taq_performance$', views.get_taq_performance, name='get_taq_performance'),
    url('index', views.index, name='index'),
]
