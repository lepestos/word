from django.urls import path
from . import views

urlpatterns = [
    path('words/', views.WordListView.as_view(), name='index'),
    path('word/<int:pk>/', views.WordDetailView.as_view(), name='word_detail'),
    path('word/<int:pk>/update/', views.WordUpdateView.as_view(), name='word_update'),
    path('group/<int:pk>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('add_word/', views.add_word_view, name='add_word'),
    path('add_group/', views.add_group_view, name='add_group'),
    path('group/<int:pk>/update/', views.GroupUpdateView.as_view(), name='group_update'),
    path('group/<int:pk>/practice/<str:lp>/', views.practice_eg_view, name='practice_eg'),
    path('practice/<str:lp>/', views.practice_eg_view, name='general_practice_eg'),
    path('group/<int:pk>/add_words/', views.group_add_words_view, name='group_add_words'),
    path('group/<int:pk>/practice_menu', views.practice_menu_view, name='practice_menu'),
    path('practice_menu/', views.practice_menu_view, name='general_practice_menu'),
    path('word/<int:pk>/duden_examples/', views.duden_definitions_view, name='duden_definitions'),
]
