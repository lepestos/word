from django.forms import ModelForm
from .models import Word, Group


class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = ['german', 'english', 'definition',
                  'word_class', 'gender']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'words']
