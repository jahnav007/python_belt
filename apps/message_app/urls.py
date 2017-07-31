from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^quotes$', views.quotes),
    url(r'^sub_quote$', views.sub_quote),
    url(r'^add_fav/(?P<quoteID>\d+)$', views.add_fav),
    url(r'^delete_fav/(?P<quoteID>\d+)$', views.delete_fav),
    url(r'^indv_user/(?P<userID>\d+)$', views.indv_user),

]
