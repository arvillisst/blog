from django.urls import path
from . import views

app_name='tutorial'
urlpatterns = [
    path('tutorials/', views.CategoryView.as_view(), name='tutorials'),
    path('tutorials/<slug:category_slug>/<slug:slug>/', views.TutorialDetailView.as_view(), name='tutorial_detail'),
    path('user-reaction-tutorial/', views.UserReactionView.as_view(), name='user_reaction_tutorial'),
    path('add-comment-tutorial/', views.CreateCommentView.as_view(), name='add_comment_tutorial'),
]