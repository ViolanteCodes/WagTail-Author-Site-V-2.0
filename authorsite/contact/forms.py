from django import forms

class ContactForm(forms.Form):
    your_name = forms.CharField(max_length = 100)
    your_email = forms.EmailField()
    subject = forms.CharField(max_length = 100)
    your_message = forms.CharField(widget = forms.Textarea)