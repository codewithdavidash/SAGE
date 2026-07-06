from django import forms
from .models import GalleryImage

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        # --- FIXED: Added category to field registry ---
        fields = ['title', 'category', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-neutral-300 text-black px-4 py-3 text-sm focus:outline-none focus:border-black font-sans transition-colors',
                'placeholder': 'Composition Designation / Title...'
            }),
            # --- FIXED: Tailored premium style dropdown select menu ---
            'category': forms.Select(attrs={
                'class': 'w-full bg-white border border-neutral-300 text-black px-4 py-3 text-sm focus:outline-none focus:border-black font-sans transition-colors uppercase tracking-wider text-xs'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full bg-white border border-neutral-300 text-sm text-neutral-500 p-2 focus:outline-none focus:border-black cursor-pointer file:mr-4 file:py-2 file:px-4 file:border file:border-black file:bg-black file:text-white file:text-xs file:uppercase file:tracking-widest file:font-bold hover:file:bg-neutral-800 file:transition-colors file:cursor-pointer'
            }),
        }