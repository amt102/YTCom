from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='comdata-home'),
    path('search', views.search, name='search'),
    path('search_sent', views.search_sent, name='search_sent'),
    path('search_sent/<video_id>', views.search_sent_page, name='ss_page'),
    path('lda',views.plotit,name='plotit'),
    path('trial',views.trial,name='trial'),
    path('graph', views.graph, name='graph'),
    path('hate', views.hate, name='hate'),
    path('team',views.team,name='team')
]