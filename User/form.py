from django import forms

class PictureUpload(forms.Form):
    file = forms.FileField()
    type = forms.IntegerField()