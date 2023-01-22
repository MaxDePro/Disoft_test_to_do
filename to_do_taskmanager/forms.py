from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    # images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Task
        fields = ('title', 'task_text', 'status', 'author', 'assigned_to', 'images')
        # widgets = {'images': forms.CheckboxSelectMultiple()}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'task_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description Task'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Status'}),
            'author': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Author'}),
            'assigned_to': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Assigned to'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave your comment'}),
        }