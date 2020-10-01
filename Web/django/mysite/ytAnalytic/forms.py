from django import forms

class UrlForm(forms.Form):
    url_field = forms.CharField(label="", max_length = 200)

class BoolForm(forms.Form):
    #boolean_field = forms.BooleanField() 
    boolean_field = forms.RadioSelect()

class TagForm(forms.Form):
    tag_field = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Filter by Tag'}), max_length = 200)