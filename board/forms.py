from django import forms
from .models import Topic, Post, Board

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']

class EditPostForm(forms.ModelForm):
    message = forms.CharField(label="My Message", widget=forms.Textarea())
    class Meta:
        model = Post
        fields = ['message']

class CreateBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']