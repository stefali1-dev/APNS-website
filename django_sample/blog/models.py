# blog/models.py

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    """
    Category model for blog posts
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    """
    Updated Post model with category
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=False,
        null=False,
        help_text="Upload an image for the post"
    )

    show_on_landing = models.BooleanField(
        default=False,
        verbose_name="Show on Landing Page",
        help_text="Check to display this post on the main landing page"
    )

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