# blog/models.py

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    """
    A basic Post model for a blog.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If slug is empty, auto-generate from title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the URL to access a particular blog post instance.
        For example: /blog/my-post-slug/
        """
        return reverse('post_detail', kwargs={'slug': self.slug})
