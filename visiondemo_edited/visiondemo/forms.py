from django import forms

class URLForm(forms.Form):
    myinput = forms.CharField(label='My URL', max_length=300)

class UploadFileForm(forms.Form):
    #my_parameter = forms.CharField(max_length=50)
    #file = forms.FileField(label='Upload')
    file = forms.FileField()
    