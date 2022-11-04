from socket import fromshare
from django import forms
from snippets.models import Snippet
from snippets.models import Comment


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ("title", "code", "description")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("TEXT",)
