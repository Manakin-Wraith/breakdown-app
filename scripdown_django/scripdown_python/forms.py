from django import forms
from .models import Script

class ScriptUploadForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['title', 'content']