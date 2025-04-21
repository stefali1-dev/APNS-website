# models.py
from django.db import models
from django.utils.text import slugify

from users.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class EBook(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    authors = models.ManyToManyField(  # Schimbat de la CharField la ManyToMany
        Profile,
        related_name='authored_ebooks',
        verbose_name='Autori'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ebooks')
    short_description = models.TextField(max_length=250)
    full_description = models.TextField()
    toc = models.TextField(verbose_name='Cuprins')
    cover_image = models.ImageField(upload_to='ebooks/covers/', blank=True, null=True)
    file = models.FileField(upload_to='ebooks/files/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    page_count = models.PositiveIntegerField(default=0)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.price == 0:
            self.is_free = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']
