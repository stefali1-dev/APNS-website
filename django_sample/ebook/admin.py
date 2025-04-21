from django.contrib import admin
from tinymce.widgets import TinyMCE

from ebook.models import Category
from .models import EBook
from django.db import models

admin.site.register(Category)

@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)
    list_display = ('title', 'display_authors', 'category', 'price', 'is_free', 'published_date')
    list_filter = ('category', 'is_free', 'format', 'published_date')
    search_fields = ('title', 'authors__name', 'category__name')
    date_hierarchy = 'published_date'
    
    # TinyMCE configuration
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    
    # Custom field display
    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Autori'
    
    # Custom form field configuration for specific fields
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['short_description', 'full_description', 'toc']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 100, 'rows': 20},
                mce_attrs={
                    'plugins': 'advlist autolink lists link image charmap print preview anchor'
                               'searchreplace visualblocks code fullscreen insertdatetime media table'
                               'paste code help wordcount',
                    'toolbar': 'undo redo | formatselect | bold italic backcolor |'
                               'alignleft aligncenter alignright alignjustify |'
                               'bullist numlist outdent indent | removeformat | help',
                    'content_style': 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
                    'images_upload_url': '/upload_image/'
                }
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    # Optional: Customize fieldsets for better layout
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'authors', 'category')
        }),
        ('Conținut', {
            'fields': ('short_description', 'full_description', 'toc'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Detalii tehnice', {
            'fields': ('cover_image', 'file', 'price', 'is_free', 'format', 'page_count'),
            'classes': ('collapse',),
        }),
        ('Date publicare', {
            'fields': ('published_date',),
        }),
    )
