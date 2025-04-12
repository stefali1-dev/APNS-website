from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Profile

def profile_list(request):
    profiles = Profile.objects.all().order_by('-created_at')
    return render(request, 'users/profile_list.html', {'profiles': profiles})

# def profile_detail(request, pk):
#     profile = get_object_or_404(Profile, pk=pk)
#     return render(request, 'users/profile_detail.html', {'profile': profile})