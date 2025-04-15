# common/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('enrollment', views.enrollment_view, name='enrollment_page'),
    path('donation', views.donation_view, name='donation_page'),
    path('contact', views.contact_view, name='contact_page'),
    path('article/<str:topic>/', views.article_view, name='article_detail'),

]