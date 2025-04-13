from django.shortcuts import render

from blog.models import Post

# Create your views here.
# views.py
def landing_page(request):
    featured_posts = Post.objects.filter(show_on_landing=True).order_by('-created_at')[:3]  # Get 6 posts max
    return render(request, 'common/landing_page.html', {'featured_posts': featured_posts})

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