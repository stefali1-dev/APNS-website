# views.py
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from django_sample.settings import DEFAULT_FROM_EMAIL
from .models import EBook, Category
from django.http import JsonResponse
from django.core.mail import send_mail
import json


class EBookListView(ListView):
    model = EBook
    template_name = 'ebook/ebook_list.html'
    context_object_name = 'ebooks'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply search filter
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        # Apply category filter
        category = self.request.GET.getlist('category')
        if category:
            queryset = queryset.filter(category__id__in=category)
        
        # Apply price filter
        price_filter = self.request.GET.getlist('price')
        if price_filter:
            if 'free' in price_filter and 'paid' in price_filter:
                pass  # Both selected, no filtering needed
            elif 'free' in price_filter:
                queryset = queryset.filter(is_free=True)
            elif 'paid' in price_filter:
                queryset = queryset.filter(is_free=False)
        
        # Apply format filter
        format_filter = self.request.GET.getlist('format')
        if format_filter:
            queryset = queryset.filter(format__in=format_filter)
        
        # Apply sorting
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'newest':
            queryset = queryset.order_by('-published_date')
        elif sort == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort == 'title_desc':
            queryset = queryset.order_by('-title')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class EBookDetailView(DetailView):
    model = EBook
    template_name = 'ebook/ebook_detail.html'
    context_object_name = 'ebook'
    slug_url_kwarg = 'slug'


import json
from django.http             import JsonResponse
from django.shortcuts        import get_object_or_404
from django.core.mail        import EmailMultiAlternatives
from django.template.loader  import render_to_string
from django.conf             import settings
from .models                 import EBook

def send_ebook(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodă nepermisă'}, status=405)

    ebook = get_object_or_404(EBook, slug=slug)

    # Parse JSON
    try:
        payload = json.loads(request.body.decode('utf-8'))
        recipient = payload.get('email')
    except ValueError:
        return JsonResponse({'error': 'Date JSON invalide'}, status=400)

    if not recipient:
        return JsonResponse(
            {'error': 'Vă rugăm să introduceți o adresă de email validă'},
            status=400
        )

    # Construim link-ul absolut către fișier
    link_ebook = request.build_absolute_uri(ebook.file.url)

    # Context pentru template-ul HTML
    context = {
        'ebook': ebook,
        'link': link_ebook,
    }

    # Conținut text
    text_content = (
        f"Bună!\n\n"
        f"Poți descărca e‑book‑ul „{ebook.title}” aici:\n"
        f"{link_ebook}\n\n"
        "Toate cele bune,\n"
        "Echipa Asociației pentru Promovarea Nutriției Sănătoase"
    )

    # Conținut HTML (din template-ul emails/ebook.html)
    html_content = render_to_string('ebook/emails/ebook.html', context)

    # Pregătim EmailMultiAlternatives
    subject = f"Descarcă „{ebook.title}” gratuit"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient]

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.extra_headers = {'Reply-To': DEFAULT_FROM_EMAIL}

    # Trimitem email-ul
    try:
        msg.send(fail_silently=False)
    except Exception as e:
        # Aici poți loga e (de ex. logger.error(str(e)))
        return JsonResponse(
            {'error': 'Eroare la trimiterea email‑ului. Încearcă din nou mai târziu.'},
            status=500
        )

    return JsonResponse({'success': True})
