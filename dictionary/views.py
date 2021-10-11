from random import shuffle, randint
import json

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .models import Word, Group
from .forms import WordForm, GroupForm
from .web_scrappers import duden_definitions


class WordListView(ListView):
    model = Word
    paginate_by = 20


class WordDetailView(DetailView):
    model = Word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Word.objects.get(pk=pk).delete()
        return redirect('index')


class WordUpdateView(UpdateView):
    model = Word
    template_name_suffix = '_update'
    fields = ['german', 'english', 'definition',
              'word_class', 'gender', 'relevance']


class GroupDetailView(DetailView):
    model = Group


class GroupListView(ListView):
    model = Group


class GroupUpdateView(UpdateView):
    model = Group
    template_name_suffix = '_update'
    fields = ['name', 'words']


g_to_art = {
    'm': 'der',
    'n': 'das',
    'f': 'die',
}


def add_word_view(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = cd['gender']
            if g:
                cd['article'] = g_to_art[g]
            w = Word.objects.create(**cd)
            w.save()
            return redirect('add_word')
    else:
        form = WordForm()
        return render(request, 'dictionary/add_word.html',
                      {'form': form})


def add_group_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GroupForm()
        return render(request, 'dictionary/add_group.html',
                      {'form': form})


eng_prefix = {
    'v': 'to ',
    'n': 'the ',
    'adv': '',
    'adj': '',
}


def practice_eg_view(request, lp, pk=None):
    if request.method == "GET":
        if pk is not None:
            group = Group.objects.get(pk=pk)
            words = list(group.words.all())
            rng = [int(x) for x in request.GET['range'].split('-')]
            words = words[rng[0]-1:rng[1]]
            shuffle(words)
        else:
            group = None
            words = list(Word.objects.all()[0:10])
            shuffle(words)
            words += list(Word.objects.all()[10:30])
            total = Word.objects.count()
            for i in range(6):
                words.insert(randint(0, 29+i), Word.objects.all()[randint(0, total-1)])

        ger_words = [word.article + ' ' + word.german if word.article
                     else word.german for word in words]
        eng_words = [eng_prefix[word.word_class] + word.english for word in words]
        if lp == 'ge':
            language = 'English'
            target_words, source_words = eng_words, ger_words
        else:
            language = 'German'
            target_words, source_words = ger_words, eng_words

        return render(request, 'dictionary/practice_eg.html',
                      {'group': group,
                       'target_words': json.dumps(target_words),
                       'source_words': json.dumps(source_words),
                       'language': language})
    else:
        data = request.POST
        german = data.get('word')
        if german[:3] in ['der', 'das', 'die']:
            german = german[4:]
        decrease = True if data.get('correct') == 'true' else False
        time_delta = float(data.get('time_delta'))
        word = Word.objects.filter(german=german)[0]
        if lp == 'eg':
            rel_len = len(word.article + word.german) + 1
        else:
            rel_len = len(eng_prefix[word.word_class] + word.english)
        time_coeff = time_delta / rel_len
        bias_coeff = 1 if pk is None else 0.2
        word.change_relevance(decrease, time_coeff, bias_coeff)
        return HttpResponse(200)


def group_add_words_view(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'GET':
        words = set(group.words.all())
        other_words = sorted(set(Word.objects.all()).difference(words),
                             key=lambda x: x.timestamp, reverse=True)
        return render(request, 'dictionary/group_add_words.html',
                      {'group': group,
                       'words': words,
                       'other_words': other_words})
    else:
        data = request.POST
        words = data.getlist('words[]')
        ids = [Word.objects.filter(german=word)[0].pk for word in words]
        group.words.set(ids)
        return HttpResponse(200)


def practice_menu_view(request, pk=None):
    if pk is None:
        return render(request, 'dictionary/general_practice_menu.html')
    group = Group.objects.get(pk=pk)
    return render(request, 'dictionary/practice_menu.html',
                  {'group': group})


def duden_definitions_view(request, pk):
    word = Word.objects.get(pk=pk)
    definitions = duden_definitions(word.german)
    return render(request, 'dictionary/duden_definitions.html',
                  {'word': word,
                   'definitions': definitions})
