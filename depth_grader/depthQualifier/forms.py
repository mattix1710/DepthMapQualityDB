from django import forms
from depthQualifier.models import SequenceModel

class UploadZipForm(forms.ModelForm):
    # # zip file
    # srcFile = forms.FileField(widget=forms.ClearableFileInput())
    # # sequence title
    # title = forms.CharField(max_length=20)
    # # description - textarea
    # desc = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':20}))

    class Meta:
        # def __init__(self, *args, **kwargs):
        #     super(UploadZipForm, self).__init__(*args, **kwargs)
        #     self.fields['title'].label = 'Nazwa sekwencji'
        #     self.fields['desc'].label = 'Opis sekwencji'
        #     self.fields['src'].label = 'Archiwum ZIP z sekwencją'

        labels = {
            'title': 'Nazwa sekwencji',
            'desc': 'Opis sekwencji',
            'src': 'Archiwum ZIP z sekwencją',
        }

        model = SequenceModel
        fields = ('title', 'desc', 'src')