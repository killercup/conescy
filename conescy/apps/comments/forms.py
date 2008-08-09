from django import forms

class CommentForm(forms.Form):
    """A form to validate a comment made by a visitor (not for logged in users)."""
    name = forms.CharField(required=True, max_length=100)
    mail = forms.EmailField(required=True)
    url = forms.URLField(required=False)
    content = forms.CharField(required=True)
