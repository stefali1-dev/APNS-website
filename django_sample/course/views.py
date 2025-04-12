from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from .models import Course, Cart, CartItem, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.course.price * item.quantity for item in cart_items)
        return render(request, 'courses/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('courses:cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('courses:cart')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.course.price * item.quantity for item in cart_items)
        return render(request, 'courses/checkout.html', {'total': total})

    def post(self, request):
        # Handle payment integration (Stripe/PayPal) here
        # For now, create an order
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.course.price * item.quantity for item in cart_items)
        
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_status='pending'
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                course=item.course,
                price=item.course.price
            )
        cart_items.delete()  # Clear cart after order
        return redirect('courses:payment_success')

class PaymentSuccessView(TemplateView):
    template_name = 'courses/payment_success.html'

class PaymentFailureView(TemplateView):
    template_name = 'courses/payment_failure.html'