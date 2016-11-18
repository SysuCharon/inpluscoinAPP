from django.conf.urls import patterns, include, url

from django.contrib import admin
from wx import views as wx
from web import views as web
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'inpluscoinAPP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', wx.Main, name='main'),
    url(r'^test/test$', wx.Test, name='test'),
    url(r'^wx$', wx.handleRequest, name='wx'),
    # need wx`s views.py

    # for web
    url(r'^$', web.index, name='index'),
    url(r'^regist$', web.regist, name='regist'),
    url(r'^login$', web.login, name='login'),
    url(r'^input$', web.input, name='input'),
    url(r'^display$', web.display, name='display'),
    url(r'^detail$', web.detail, name='detail'),
)
