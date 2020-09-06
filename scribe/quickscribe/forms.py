from django import forms

from .models import Novel

YES_NO_CHOICES = [
    (True, "Yes"),
    (False, "No"),
]

class Novel_Form(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ["name", "author", "artist", "year", "publisher", "licensed", "coo_status", "fully_translated", "genres", "tags", "language"]
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "Please enter the novel's title",}),
            'author': forms.TextInput(attrs={"placeholder": "Please enter the novel's author",}),
            'artist': forms.TextInput(attrs={"placeholder": "Please enter the novel's artist",}),
            'publisher': forms.TextInput(attrs={"placeholder": "Please enter the novel's publisher",}),
            'coo_status': forms.Textarea(attrs={"placeholder": "Please enter the novel's status in country of origin",}),
            'language': forms.RadioSelect(),
        }
