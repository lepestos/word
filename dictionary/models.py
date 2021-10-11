from datetime import datetime
from decimal import Decimal

from django.db import models
from django.urls import reverse


class Word(models.Model):
    german = models.CharField(max_length=64)
    english = models.CharField(max_length=64, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    relevance = models.DecimalField(decimal_places=3, max_digits=7,
                                    default=950.000)
    articles = [
        ('der', 'der'),
        ('das', 'das'),
        ('die', 'die')
    ]
    genders = [
        ('m', 'masculine'),
        ('n', 'neuter'),
        ('f', 'feminine')
    ]
    word_classes = [
        ('n', 'noun'),
        ('v', 'verb'),
        ('adv', 'adverb'),
        ('adj', 'adjective'),
    ]

    article = models.CharField(choices=articles, max_length=4,
                               blank=True, default='')
    gender = models.CharField(choices=genders, max_length=16,
                              blank=True, default='')
    word_class = models.CharField(choices=word_classes, max_length=16,
                                  blank=True, default='')

    class Meta:
        ordering = ('-relevance',)

    def __str__(self):
        article = str(self.article) if self.article is not None else ''
        return str(article) + ' ' + str(self.german)

    def get_absolute_url(self):
        return reverse('word_detail', kwargs={'pk': self.pk})

    def change_relevance(self, decrease: bool, time_coeff: float, bias_coeff: float = 1) -> None:
        if decrease:
            if time_coeff >= 0.5:
                coeff = min(1.0, 0.95 + time_coeff/50)
            else:
                coeff = 0.95
            self.relevance -= Decimal(1-coeff) * self.relevance * Decimal(bias_coeff)
        else:
            self.relevance += (Decimal(1000) - self.relevance) * Decimal(0.75) * Decimal(bias_coeff)
        self.save()


class Group(models.Model):
    name = models.CharField(max_length=128)
    words = models.ManyToManyField('Word', related_name='groups',
                                   blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'pk': self.pk})
