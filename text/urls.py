from django.urls import path
from . import views

urlpatterns = [
    path("", views.TextList.as_view(), name="text_list"),
    path("texts/<int:pk>/", views.TextDetail.as_view(), name="text_detail"),
]
