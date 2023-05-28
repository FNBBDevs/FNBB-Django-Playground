from django import forms

class CreatePostForm(forms.Form):
    title  = forms.CharField(label="Title")
    content = forms.CharField(label="Post")

class UpdatePostForm(forms.Form):
    title  = forms.CharField(label="Title", required=False)
    content = forms.CharField(label="Post", required=False)
