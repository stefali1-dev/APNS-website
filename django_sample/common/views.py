from django.shortcuts import render

from blog.models import Post

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from users.models import EmailSubscription

# Create your views here.
# views.py
def landing_page(request):
    featured_posts = Post.objects.filter(show_on_landing=True).order_by('-created_at')[:3]  # Get 6 posts max
    return render(request, 'common/landing_page.html', {'featured_posts': featured_posts})

@require_POST
def subscribe(request):
    email = request.POST.get('email', '')
    try:
        EmailSubscription.objects.create(email=email)
        response = JsonResponse({'status': 'success'})
        # Setăm cookie pentru 30 de days DACA s-a abonat
        response.set_cookie('email_subscribed', 'true', max_age=30*24*60*60)
        return response
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def enrollment_view(request):
    context = {
        'contact_phone': '0740 123 456',  # Poți să extragi din baza de date sau setări
        'contact_email': 'voluntari@asociatianutrition.ro',
    }
    return render(request, 'common/enrollment_page.html', context)

def donation_view(request):
    return render(request, 'common/donation_page.html')

def contact_view(request):
    return render(request, 'common/contact_page.html')

def article_view(request, topic):
    template_path = f'common/articles/{topic.lower()}.html'
    return render(request, template_path)