from django.contrib import admin
from .models import Word, Group


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass