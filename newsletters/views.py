from django.shortcuts import render
from .models import NewsletterUser
from .forms import NewsLetterUserSignUpForm
from django.views.generic import View


class NewsletterSingUpView(View):
    template_name = 'newsletters/sign_up.html'

    def post(self, request, *args, **kwargs):
        form = NewsLetterUserSignUpForm(request.POST or None)

        if form.is_valid():
            instance = form.save(commit=False)

            if NewsletterUser.objects.filter(email=instance.email).exists():
                print('Такой емейл уже существует')
            else:
                instance.save()
        context = {}
        context['form_newsletter'] = form
        return render(request, self.template_name, context)


class NewsletterUnsubscribeView(View):
    template_name = 'newsletters/unsubscribe.html'

    def post(self, request, *args, **kwargs):
        form = NewsLetterUserSignUpForm(request.POST or None)

        if form.is_valid():
            instance = form.save(commit=False)

            if NewsletterUser.objects.filter(email=instance.email).exists():
                NewsletterUser.objects.filter(email=instance.email).delete()

            else:
                print('Емей не найден')
        context = {}
        context['form_newsletter'] = form
        return render(request, self.template_name, context)





