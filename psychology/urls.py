from django.urls import path
from . import views

urlpatterns = [
    path('scat_test', views.scat_test, name='scat_test_page'),
    path('csai2_test', views.csai2_test, name='csai2_test_page'),
    path('poms_test', views.poms_test, name='poms_test_page'),
    path('teosq_test', views.teosq_test, name='teosq_test_page')
]
