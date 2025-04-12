from django.contrib import admin

from users.models import EmailSubscription, Profile

# Register your models here.
admin.site.register(EmailSubscription)
admin.site.register(Profile)