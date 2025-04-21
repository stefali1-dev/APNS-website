
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('common.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('ebook/', include('ebook.urls')),
    path('courses/', include('course.urls')),
    path('volunteers/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
