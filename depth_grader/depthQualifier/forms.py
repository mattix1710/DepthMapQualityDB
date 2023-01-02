from django import forms
from depthQualifier.models import MethodProposal#,SequenceModel

# class UploadZipForm(forms.ModelForm):
#     # # zip file
#     # srcFile = forms.FileField(widget=forms.ClearableFileInput())
#     # # sequence title
#     # title = forms.CharField(max_length=20)
#     # # description - textarea
#     # desc = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':20}))

#     error_css_class = 'error-field'
#     required_css_class = 'required_field'
#     title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-title", "placeholder": "Sequence title"}))
#     desc = forms.CharField(widget=forms.Textarea(attrs={"class": "form-desc", "placeholder": "Sequence description"}))

#     class Meta:
#         # def __init__(self, *args, **kwargs):
#         #     super(UploadZipForm, self).__init__(*args, **kwargs)
#         #     self.fields['title'].label = 'Nazwa sekwencji'
#         #     self.fields['desc'].label = 'Opis sekwencji'
#         #     self.fields['src'].label = 'Archiwum ZIP z sekwencją'

#         labels = {
#             'title': 'Nazwa sekwencji',
#             'desc': 'Opis sekwencji',
#             'src': 'Sequence ZIP archive',
#         }

#         model = SequenceModel
#         fields = ('title', 'desc', 'src')
        
class UploadMethodZipForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required_field'
    method_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-title", "placeholder": "i.e. MyMethod"}))
    desc = forms.CharField(widget=forms.Textarea(attrs={"class": "form-desc", "placeholder": "Method description, i.e. link to the article about this method..."}))

    class Meta:
        # def __init__(self, *args, **kwargs):
        #     super(UploadZipForm, self).__init__(*args, **kwargs)
        #     self.fields['title'].label = 'Nazwa sekwencji'
        #     self.fields['desc'].label = 'Opis sekwencji'
        #     self.fields['src'].label = 'Archiwum ZIP z sekwencją'

        # labels = {
        #     'method_name': 'Nazwa sekwencji',
        #     'desc': 'Opis sekwencji',
        #     'src': 'ZIP archive containing depth maps',
        # }

        # use current model as a template for a form
        model = MethodProposal
        fields = ['method_name', 'desc', 'src']