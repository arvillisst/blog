from django.urls import path
from . import views


urlpatterns = [
    path('subscribe/', views.NewsletterSingUpView.as_view(), name='subscribe'),
    path('unsubscribe/', views.NewsletterUnsubscribeView.as_view(), name='unsubscribe'),
]