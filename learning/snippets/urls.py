from django.urls import path
from snippets import views

urlpatterns = [
    path('',views.api_root),
    path('snippets/', views.Snippet_list.as_view(),name = 'snipper-list',),
    path('snippets/<int:pk>/', views.Snippet_detail.as_view()),
    path('users/', views.UserList.as_view(), name = 'user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
]