from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name="myadmin_index"),


	url(r'^login$',views.login,name="myadmin_login"),
	url(r'^dologin$',views.dologin,name="myadmin_dologin"),
	url(r'^logout$',views.logout,name="myadmin_logout"),
	url(r'^verify$',views.verify,name="myadmin_verify"),

	url(r'^users$', views.usersindex, name="myadmin_usersindex"),
	url(r'^usersadd$', views.usersadd, name="myadmin_usersadd"),
	url(r'^usersinsert$', views.usersinsert, name="myadmin_usersinsert"),
	url(r'^usersdel/(?P<id>[0-9]+)$', views.usersdel, name="myadmin_usersdel"),
	url(r'^usersedit/(?P<id>[0-9]+)$', views.usersedit, name="myadmin_usersedit"),
	url(r'^usersupdate/(?P<id>[0-9]+)$', views.usersupdate, name="myadmin_usersupdate"),
]
