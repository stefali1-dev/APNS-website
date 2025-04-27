# common/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home', views.landing_page, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('enrollment', views.enrollment_view, name='enrollment'),
    path('donation', views.donation_view, name='donation'),
    path('contact', views.contact_view, name='contact'),
    path('volunteers/', views.volunteers_view, name='volunteers'),
    path('webinars/', views.webinars_view, name='webinars'),
    path('article/<str:topic>/', views.article_view, name='article_detail'),

]