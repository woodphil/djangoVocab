from django.contrib import admin
from vocabTest.models import Word, Question, LevenshteinPair

# Register your models here.
admin.site.register(Word)
admin.site.register(Question)
admin.site.register(LevenshteinPair)