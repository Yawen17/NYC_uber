from django import forms  
from .models import Input, MONTHS

class InputForm(forms.ModelForm):  

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}

    month = forms.ChoiceField(choices=MONTHS, required=True,
                              widget=forms.Select(attrs = attrs))
    class Meta:
        model = Input
        fields = ['month']
