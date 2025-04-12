from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course listing
    path('', views.CourseListView.as_view(), name='course_list'),
    # Course detail
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    # Cart management
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Checkout
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # Payment success/failure
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failure/', views.PaymentFailureView.as_view(), name='payment_failure'),
]