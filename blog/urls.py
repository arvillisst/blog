from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchArticleView.as_view(), name='search'),
    path('news/subscribe/', views.SubscribeView.as_view(), name='subscribe_news'),
    path('contact/write-us/', views.contact_view, name='contact'),
    path('thanks/', views.thanks, name='thanks'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<slug>/', views.TagIndexView.as_view(), name='tagged'),
    
    path('<slug:category>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('user-reaction/', views.UserReactionView.as_view(), name='user_reaction'),
    path('add-comment/', views.CreateCommentView.as_view(), name='add_comment'), 
    
    path('import-csv/', views.import_csv),
]