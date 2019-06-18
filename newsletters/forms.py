from django import forms
from .models import NewsletterUser

class NewsLetterUserSignUpForm(forms.ModelForm):

    class Meta:
        model = NewsletterUser
        fields = ['email']
        # widgets = ...

        def clean_email(self):
            email = self.cleaned_data.get('email')
            return email

    email = forms.CharField(label='', widget=forms.TextInput(attrs={
        'name': 'EMAIL',
        'type': 'email',
        'required': "",
        'onfocus': 'this.placeholder = ""',
        'onblur': 'this.placeholder = "Ваш Email"',
        'placeholder': 'Ваш Email'
    }))