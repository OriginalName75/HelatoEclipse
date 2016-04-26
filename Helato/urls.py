"""Helato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from ajax_select import urls as ajax_select_urls
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^connexion$', auth_views.login, {'template_name':'BDD/conn.html'}),
    url(r'^deconnexion$', auth_views.logout, {'next_page':'/connexion'}),
    url(r'^administration$', 'BDD.views.administration'),
    
    url(r'^watch/(?P<table>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)$', 'BDD.views.watch'),
    url(r'^watch/(?P<table>\d+)/(?P<filtre>\d+)$', 'BDD.views.watch'),
    url(r'^ajouter/(?P<table>\d+)/(?P<nbajout>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)$', 'BDD.views.ajouter'),
    url(r'^fiche/(?P<table>\d+)/(?P<idP>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)$', 'BDD.views.fiche'),
    url(r'^fiche/(?P<table>\d+)/(?P<idP>\d+)$', 'BDD.views.fiche'),

    url(r'^change/(?P<table>\d+)/(?P<idP>\d+)/(?P<what>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)$', 'BDD.views.change'),
    url(r'^areusure/(?P<table>\d+)/(?P<idP>\d+)/(?P<what>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)/(?P<nor>\d+)/(?P<which>\d+)/$', 'BDD.views.areusure'),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^delete/(?P<table>\d+)/(?P<idP>\d+)/(?P<filtre>\d+)/(?P<page>\d+)/(?P<nbparpage>\d+)/(?P<nomClasser>\d+)/(?P<plusOuMoins>\d+)/(?P<supri>\d+)$', 'BDD.views.delete'),
    url(r'^randomP$', 'BDD.views.randomP'),
    url(r'^f/(?P<plus>\d+)$', 'BDD.views.index'),
    
    #pour que Morgan fasse ses tests
    url(r'^mor$', 'BDD.views.mor'),
    url(r'^morSup$', 'BDD.views.morSup'),
    #jusque l�
    
    url(r'$', 'BDD.views.index'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
