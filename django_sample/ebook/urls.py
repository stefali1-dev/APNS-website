# urls.py
from django.urls import path

from ebook import views
from .views import EBookListView, EBookDetailView


urlpatterns = [
    path('', EBookListView.as_view(), name='ebooks_list'),
    path('<slug:slug>/', EBookDetailView.as_view(), name='ebook_detail'),
    path('<slug:slug>/trimite/', views.send_ebook, name='send_ebook')
]