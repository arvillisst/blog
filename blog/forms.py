from django import forms
# from snowpenguin.django.recaptcha2.fields import ReCaptchaField
# from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
# from captcha.fields import ReCaptchaField

class SubscriberForm(forms.Form):
    
    email = forms.CharField(label='', widget=forms.TextInput(attrs={
        'name': 'EMAIL',
        'type': 'email',
        'required': "",
        'onfocus': 'this.placeholder = ""',
        'onblur': 'this.placeholder = "Ваш Email"',
        'placeholder': 'Ваш Email'
    }))


class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'name': 'query',
        'placeholder': 'Поиск'
    }))


class CommentForm(forms.Form):

    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'onfocus': 'this.placeholder = ""',
        'onblur': 'this.placeholder = "Имя"',
        'placeholder': 'Имя'
    }))
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control mb-10',
        'rows': 5,
        'name': 'message',
        'onfocus': 'this.placeholder = ""',
        'onblur': 'this.placeholder = "Комментарий"',
        'required': "",
        'placeholder': 'Комментарий'
    }))
    honeypot = forms.CharField(required=False, label='Ловушка для спамеров')



class ContactForm(forms.Form):

    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'id': 'name',
        'placeholder': 'Ваше имя'
    }))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={
        'name': 'email',
        'type': 'email',
        'class': 'form-control',
        'required': "",
        'placeholder': 'Ваш Email'
    }))
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'id': 'name',
        'placeholder': 'Тема'
    }))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 1,
        'name': 'message',
        'id': 'message',
        'placeholder': 'Сообщение'
    }))
