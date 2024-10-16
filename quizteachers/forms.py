from django.forms import modelformset_factory
from django import forms
from .models import Quiz, Question, QuestionText, QuestionMCQ

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['teacher', 'title', 'year']
        labels = {
            'teacher': 'Teacher',
            'title': 'Quiz Title',
            'year': 'Year',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_type', 'question_text']
        labels = {
            'quiz': 'Quiz',
            'question_type': 'Type of Question',
            'question_text': 'Question Text',
        }

class QuestionTextForm(forms.ModelForm):
    class Meta:
        model = QuestionText
        fields = ['question', 'answer']
        labels = {
            'question': 'Question',
            'answer': 'Text Answer',
        }

class QuestionMCQForm(forms.ModelForm):
    class Meta:
        model = QuestionMCQ
        fields = ['question', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']
        labels = {
            'question': 'Question',
            'option_1': 'Option 1',
            'option_2': 'Option 2',
            'option_3': 'Option 3',
            'option_4': 'Option 4',
            'correct_option': 'Correct Option',
        }

# Formsets
QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)
QuestionTextFormSet = modelformset_factory(QuestionText, form=QuestionTextForm, extra=1)
QuestionMCQFormSet = modelformset_factory(QuestionMCQ, form=QuestionMCQForm, extra=1)