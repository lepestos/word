from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Text


class TextList(ListView):
    model = Text


class TextDetail(DetailView):
    model = Text
