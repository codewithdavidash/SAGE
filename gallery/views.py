from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Added pagination engines
from .models import GalleryImage
from .forms import GalleryImageForm

def gallery_index(request):
    """
    Displays the public exhibition masonry grid.
    Handles optional category filters, keyword search parameters, 
    and lazy-loading dynamic page windows.
    """
    images_list = GalleryImage.objects.all().order_by('-uploaded_at')
    
    # --- 1. Category Filtering Matrix ---
    selected_category = request.GET.get('category', '').strip().upper()
    if selected_category and selected_category != 'ALL':
        images_list = images_list.filter(category=selected_category)
        
    # --- 2. Live Keyword Text Search View Engine ---
    search_query = request.GET.get('q', '').strip()
    if search_query:
        images_list = images_list.filter(
            Q(title__icontains=search_query) | 
            Q(category__icontains=search_query)
        )
        
    # --- 3. Dynamic Window Pagination Segment ---
    # Set target sizing threshold (e.g., 12 items per virtual window load batch)
    paginator = Paginator(images_list, 12) 
    page_number = request.GET.get('page')
    
    try:
        images = paginator.page(page_number)
    except PageNotAnInteger:
        # If page param is missing or corrupted, default to first archival frame
        images = paginator.page(1)
    except EmptyPage:
        # If the requested batch index exceeds boundaries, deliver last frame
        images = paginator.page(paginator.num_pages)
        
    context = {
        'images': images,  # Now a specialized Page object instead of a raw QuerySet
        'current_category': selected_category or 'ALL',
        'search_query': search_query,
    }
    return render(request, 'gallery/gallery.html', context)

@login_required
def curator_dashboard(request):
    """
    Central operational hub for the curator to view all plates,
    with entry points to Create, Update, and Delete actions.
    """
    images_list = GalleryImage.objects.all().order_by('-uploaded_at')
    
    # Dashboard pagination keeps processing overhead lightweight for management
    paginator = Paginator(images_list, 20)
    page_number = request.GET.get('page')
    
    try:
        images = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        images = paginator.page(1)
        
    return render(request, 'gallery/dashboard.html', {'images': images})

@login_required
def upload_image(request):
    """
    CREATE: A protected view to upload new images to Sage.
    Triggers the Pillow text-watermark generation automatically on save.
    """
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('curator_dashboard')
    else:
        form = GalleryImageForm()
        
    return render(request, 'gallery/upload.html', {'form': form, 'is_edit': False})

@login_required
def edit_image(request, pk):
    """
    UPDATE: Allows modification of an existing artifact's title or image asset.
    """
    image_instance = get_object_or_404(GalleryImage, pk=pk)
    
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=image_instance)
        if form.is_valid():
            form.save()
            return redirect('curator_dashboard')
    else:
        form = GalleryImageForm(instance=image_instance)
        
    return render(request, 'gallery/upload.html', {'form': form, 'image': image_instance, 'is_edit': True})

@login_required
def delete_image(request, pk):
    """
    DELETE: Removes a specified artifact permanently from the collection records.
    """
    image_instance = get_object_or_404(GalleryImage, pk=pk)
    
    if request.method == 'POST':
        image_instance.delete()
        return redirect('curator_dashboard')
        
    return render(request, 'gallery/delete_confirm.html', {'image': image_instance})