from django import forms

from .models import Novel, Chapter

class Novel_Form(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['name', 'alt_name', 'description', 'cover', 'author', 'artist', 'year', 'publisher', 'licensed', 'coo_status', 'fully_translated', 'genres', 'tags', 'language']
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "Please enter the novel's title",}),
            'alt_name': forms.Textarea(attrs={"placeholder": "Please enter the novel's alternative titles (if applicable)"}),
            'description': forms.Textarea(attrs={"placeholder": "Please enter the novel's description"}),
            'author': forms.TextInput(attrs={"placeholder": "Please enter the novel's author",}),
            'artist': forms.TextInput(attrs={"placeholder": "Please enter the novel's artist (if applicable)",}),
            'publisher': forms.TextInput(attrs={"placeholder": "Please enter the novel's publisher (if applicable)",}),
            'coo_status': forms.Textarea(attrs={"placeholder": "Please enter the novel's status in country of origin",}),
            'language': forms.RadioSelect(),
        }

class Chapter_Form(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'content']
