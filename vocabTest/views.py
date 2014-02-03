from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from django.template import RequestContext, loader

from django.utils import timezone

#models
from vocabTest.models import Word, Question, LevenshteinPair

#other python libraries
from random import choice, randint

'''session variables:
questions_asked: number of questions asked in the quiz so far
total_questions: number of questions to be asked in the quiz
correct: was the last question answered correctly
problem_quiz: does the user want to review words that they struggle with
'''

# Create your views here.
def index(request):
    request.session['questions_asked'] = 0;
    request.session['problem_quiz'] = False;
    request.session['total_questions'] = 50;
    request.session['correct'] = None;
    return render(request, 'vocabTest/index.html');

def viewWords(request):
    # obtain the full list of words CHANGE TO GET REQUESTS
    words = Word.objects.all().order_by('word')
    return render(request, 'vocabTest/viewwords.html', {'words':words});
    
def quiz(request, **kwargs):
    try:
        # if the problematic quiz was chosen
        request.session['problem_quiz'] = kwargs['problem']
    except:
        #do nothing otherwise
        pass;
    #print(request.session['problem_quiz'])
    #handles when to stop the quiz
    if request.session['questions_asked'] <request.session['total_questions']:
        return generateQuestion(request);
    else:
        return index(request);
	
def generateQuestion(request):
    # obtain the full list of words CHANGE TO GET REQUESTS
    words = Word.objects.all()
    
    # determine word to be asked
    if request.session['problem_quiz']:
        
        if not Word.objects.filter(is_problem=True):
            return render(request, 'vocabTest/index.html', {'error_message':'you don\'t have any words you suck at!'})
        questionWord = choice(Word.objects.filter(is_problem=True))
    else:
        questionWord = choice(words)
    questionWord.num_asked+=1

    # decide what slot the correct choice will occupy
    rightChoice = randint(1,5);
    
    # make an empty set to hold the options
    answerChoices = [];
    
    # add the levenhstein pair option if applicable
    #try:
    #    questionWord.LevenhsteinPair_set
    try:
        lev = choice(LevenshteinPair.objects.filter(word_1=questionWord))
        answerChoices.append(lev.word_2.definition);
    except IndexError:
        pass;
    
    # add the last wrong choice user made if applicable
    if questionWord.last_wrong_choice is not None and questionWord.last_wrong_choice not in answerChoices:
        answerChoices.append(questionWord.last_wrong_choice)
    
    #generate incorrect options
    while len(answerChoices) != 4:
        tempChoice = choice(words);
        if tempChoice.definition is not questionWord.definition and tempChoice.definition not in answerChoices:
            answerChoices.append(tempChoice.definition);
    
    #insert the correct choice; have to adjust for index
    answerChoices.insert(rightChoice-1,questionWord.definition)
    
    #create the question
    question = Question(choice_1 = answerChoices[0],
    choice_2 = answerChoices[1],
    choice_3 = answerChoices[2],
    choice_4 = answerChoices[3],
    choice_5 = answerChoices[4],
    right_choice = rightChoice)
    question.save()
    
    #set the word to the question
    questionWord.right_question = question
    questionWord.save()
    
    #update the question counter
    request.session['questions_asked'] +=1
    
    if request.session['correct']==True:
        message = 'correct'
    elif request.session['correct']==False:
        message = 'incorrect'
    else:
        message = ''
    
    return render(request, 'vocabTest/quiz.html', {'word':questionWord, 'question':question, 'choices':[question.choice_1, question.choice_2, question.choice_3, question.choice_4, question.choice_5], 'question_message':message})

def addWordForm(request):
    return render(request, 'vocabTest/addword.html');

def addWord(request):
    newWord = request.POST['word']
    newDef = request.POST['definition']
    if newWord.strip() == "":
        return render(request, 'vocabTest/addword.html', {'error_message':'you did not enter a word'})
    elif newDef.strip() == "":
        return render(request, 'vocabTest/addword.html', {'error_message':'you did not enter a definition'})
    #check if the word is already in the database
    elif Word.objects.filter(word=newWord):
        return render(request, 'vocabTest/addword.html', {'error_message':'Word already exists in database'})
    else:
        # passed all the requirements, make new word
        tempWord = Word(word=newWord, definition=newDef, num_asked=0, num_correct=0, is_problem = False, creation_date = timezone.now())
        tempWord.save()
        
        #calculate the levenshtein pairs
        wordlist = Word.objects.all()    
        for i in wordlist:
            if i.word != newWord:
                test = calculateLevenshtein(i.word, newWord)
                if test/len(max(i.word, newWord)) <= 0.50:
                    #create two pairs
                    lev = LevenshteinPair(word_1 = i, word_2 = tempWord);
                    lev.save()
                    lev = LevenshteinPair(word_1 = tempWord, word_2 = i);
                    lev.save()
        
        
        return render(request, 'vocabTest/addword.html', {'add_message':'Word: {0} added'.format(newWord)})
    
def calculateLevenshtein(word1, word2):
    #only works in one direction
    if len(word1) > len(word2):
        word1,word2 = word2,word1
    #create and initialize a 2d array
    cost = 100
    total = [[0 for i in range(len(word2))] for j in range(len(word1))]
    for i in range(len(word1)):
        for j in range(len(word2)):
            # calculate the cost of the current location
            if word1[i] != word2[j]:
                cost = 1
            else:
                cost = 0
            
            # base cases
            if i==0 and j==0:
                total[i][j] = cost
            elif i==0 and j!=0:
                total[i][j] = total[i][j-1] + cost
            elif i!=0 and j==0:
                total[i][j] = total[i-1][j] + cost
            else:
                total[i][j] = min(total[i-1][j], total[i-1][j-1], total[i][j-1]) + cost
    return total[len(word1)-1][len(word2)-1]    
    
def answer(request, question_id):
    #obtain the relevant question
    q = get_object_or_404(Question, pk=question_id)
    wordUpdate = q.word_set.all()
    ans = wordUpdate[0]
    try:
        #convert to int, substring the first part
        if q.right_choice == int(request.POST['choice'][0]):
            request.session['correct']=True
            ans.num_correct = ans.num_correct + 1
            print("CORRECT {0}".format(ans.num_correct))
        else:
            # set the last wrong choice, substring after the choice number
            ans.last_wrong_choice = request.POST['choice'][1:len(request.POST['choice'])]
            request.session['correct']=False
            print("INCORRECT")
    except:
        #user gave invalid input
        return render(request, 'vocabTest/quiz.html', {'word':wordUpdate[0], 'question':q, 'choices':[q.choice_1, q.choice_2, q.choice_3, q.choice_4, q.choice_5], 'error_message':'You didn\'t select an option'})
        
    ans.is_a_problem()
    ans.save()
    
    #delete the question
    q.delete()
    
    return quiz(request);
    
    