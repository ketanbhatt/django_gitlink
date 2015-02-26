from django.conf.urls import patterns, url
from gitlink import views
from gitlink.views import MyView

urlpatterns = patterns('',
        url(r'^$', views.gitlink, name='gitlink'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^sel_repo/$', views.sel_repo, name='sel_repo'),
        url(r'^payload/$', views.payload, name='payload'),
        url(r'^view_payloads/$', views.view_payloads, name='view_payloads'),
        url(r'^mine/$', MyView.as_view(), name='my-view')
        )
