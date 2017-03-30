from django import forms
from .models import Snippet


class SnippetForm(forms.ModelForm):
    model = Snippet

    class Meta:
        fields = ('created', 'title', 'code', 'linenos', 'language', 'style')