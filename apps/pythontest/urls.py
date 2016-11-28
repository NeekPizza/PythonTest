from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^main$',views.main),
    url(r'^quotes$',views.quotes),
    url(r'^add$',views.add),
    url(r'^add/(?P<id>\d+)$',views.add_list),
    url(r'^remove/(?P<id>\d+)$',views.remove),
    url(r'^users/(?P<id>\d+)$',views.user),
    url(r'^regprocess$', views.regprocess),
    url(r'^loginprocess$', views.loginprocess),
    url(r'^logout$',views.logout),
]
