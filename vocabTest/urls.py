'''VOCABTEST URLS'''

from django.conf.urls import patterns, url

from vocabTest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^quiz-full$', views.quiz, name='full-quiz'),
    url(r'^quiz-problem$', views.quiz, {'problem':True}, name='problematic-quiz'),
    url(r'^answer/(?P<question_id>\d+)/$', views.answer, name='answer'),
    url(r'^addword/$', views.addWordForm, name='addword'),
    url(r'^addword-proc/$', views.addWord, name='addwordform2'),
    url(r'^viewwords/$', views.viewWords, name='viewwords'),
)