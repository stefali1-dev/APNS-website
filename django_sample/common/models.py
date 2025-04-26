# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Volunteer(models.Model):
    """Model representing a volunteer for the nutrition association."""
    
    CATEGORY_CHOICES = [
        ('nutritionist', _('Nutriționist')),
        ('medic', _('Medic')),
        ('specialist', _('Specialist')),
        ('coordonator', _('Coordonator')),
        ('student', _('Student')),
    ]
    
    name = models.CharField(_('Nume'), max_length=100)
    title = models.CharField(_('Titlu'), max_length=100)
    photo = models.ImageField(_('Fotografie'), upload_to='volunteers/')
    bio = models.TextField(_('Biografie'))
    category = models.CharField(_('Categorie'), max_length=50, choices=CATEGORY_CHOICES, default='nutritionist')
    website = models.URLField(_('Website'), blank=True, null=True)
    email = models.EmailField(_('Email'), blank=True, null=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True, null=True)
    facebook = models.URLField(_('Facebook'), blank=True, null=True)
    instagram = models.URLField(_('Instagram'), blank=True, null=True)
    priority = models.PositiveIntegerField(_('Prioritate'), default=0, help_text=_('Voluntarii cu prioritate mare vor apărea primii'))
    is_active = models.BooleanField(_('Activ'), default=True)
    created_at = models.DateTimeField(_('Creat la'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Actualizat la'), auto_now=True)
    
    class Meta:
        verbose_name = _('Voluntar')
        verbose_name_plural = _('Voluntari')
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.name