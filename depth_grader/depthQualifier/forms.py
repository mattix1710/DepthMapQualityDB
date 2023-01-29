from django import forms
from depthQualifier.models import MethodProposal
        
class UploadMethodZipForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required_field'
    
    class Meta:
        # using current model as a template for a form
        model = MethodProposal
        fields = ['method_name', 'desc', 'src']
        
        widgets = {
            'method_name': forms.TextInput(attrs={"class": "form-title", "placeholder": "i.e. MyMethod"}),
            'desc': forms.Textarea(attrs={"class": "form-desc", "placeholder": "Method description, i.e. link to the article about this method..."})
        }
        
        labels = {  'method_name': 'Method',
                    'desc': 'Description',
                    'src': 'Source files'}