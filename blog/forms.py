from django import forms
from django.shortcuts import get_object_or_404
from .models import Post, Comment

class CreatePostForm(forms.Form):
    title   = forms.CharField(label="Title")
    content = forms.CharField(label="Post")

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)

class CommentForm(forms.Form):
    comment = forms.CharField(label='')

class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


# def bounded_update_form(request, key):
#     item = get_object_or_404(Post, key=key)
#     form = UpdatePostForm(instance=item)
#     return form

# def bounded_comment_form(request, key):
#     item = get_object_or_404(Comment, key=key)
#     form = UpdateCommentForm(instance=item)
#     return form