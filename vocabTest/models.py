from django.db import models

# Create your models here.

    
class Question(models.Model):
    #questionWord = models.CharField(max_length=30)
    choice_1 = models.CharField(max_length=200)
    choice_2 = models.CharField(max_length=200)
    choice_3 = models.CharField(max_length=200)
    choice_4 = models.CharField(max_length=200)
    choice_5 = models.CharField(max_length=200)
    right_choice = models.IntegerField()
    
    def __str__(self):
        return self.choice_1

class Word(models.Model):
    right_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)
    word = models.CharField(max_length=30)
    creation_date = models.DateTimeField('date made')
    definition = models.CharField(max_length=200)
    num_asked = models.IntegerField()
    num_correct = models.IntegerField()
    last_wrong_choice = models.CharField(max_length=200, null=True, blank=True)
    is_problem = models.BooleanField()
    
    # calculate if the word is frequently wrong and should be marked as such
    def is_a_problem(self):
        try:
            if float(self.num_correct) / float(self.num_asked) <= 0.75:
                print(self.num_correct)
                self.is_problem = True;
            else:
                self.is_problem = False;
        except ZeroDivisionError:
            self.is_problem = False;
    
    def __str__(self):
        return self.word
        
class LevenshteinPair(models.Model):
    word_1 = models.ForeignKey(Word, related_name='word_1', unique=False)
    word_2 = models.ForeignKey(Word, related_name='word_2', unique=False)
    
    def __str__(self):
        return self.word_1.word + self.word_2.word