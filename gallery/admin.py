from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('title', 'preview_thumbnail', 'uploaded_at')
    
    # Adds a search bar for the titles
    search_fields = ('title',)
    
    # Adds a sidebar filter on the right to filter by upload date
    list_filter = ('uploaded_at',)
    
    # Read-only fields configuration
    readonly_fields = ('preview_large', 'uploaded_at')

    def preview_thumbnail(self, obj):
        """Generates a small thumbnail for the admin list view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #ccc;" />', 
                obj.image.url
            )
        return "No Image"
    preview_thumbnail.short_description = "Thumbnail"

    def preview_large(self, obj):
        """Generates a larger preview for the detail view page."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; height: auto; border: 1px solid #ccc;" />', 
                obj.image.url
            )
        return "No Image"
    preview_large.short_description = "Image Preview"

    # Rearranges the layout inside the image editing page
    fieldsets = (
        (None, {
            'fields': ('title', 'image')
        }),
        ('Metadata & Preview', {
            'fields': ('preview_large', 'uploaded_at'),
        }),
    )