from django.shortcuts import render, redirect, get_object_or_404
from . import views
from django.views.generic import ListView
from .forms import QuizForm, QuestionFormSet, QuestionTextFormSet, QuestionMCQFormSet
from .models import Quiz, QuestionText, QuestionMCQ, Question
from django.forms import inlineformset_factory


def home(request):
    return render(request, 'quizteachers/home.html')

def create_quiz(request):
    if request.method == 'POST':
        # Initialize forms and formsets with POST data
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        question_text_formset = QuestionTextFormSet(request.POST)
        question_mcq_formset = QuestionMCQFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()

            # Save Questions
            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz  # Assign the quiz to the question
                question.save()

                # Save text or MCQ answers
                if question.question_type == 'TEXT':
                    for text_form in question_text_formset:
                        if text_form.is_valid() and text_form.cleaned_data.get('question') == question:
                            text_form.save()

                elif question.question_type == 'MCQ':
                    for mcq_form in question_mcq_formset:
                        if mcq_form.is_valid() and mcq_form.cleaned_data.get('question') == question:
                            mcq_form.save()

            return redirect('quiz_list')

    else:
        # Initialize empty forms and formsets
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none())
        question_text_formset = QuestionTextFormSet(queryset=QuestionText.objects.none())
        question_mcq_formset = QuestionMCQFormSet(queryset=QuestionMCQ.objects.none())

    return render(request, 'quizteachers/create_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'question_text_formset': question_text_formset,
        'question_mcq_formset': question_mcq_formset,
    })



def quiz_list(request):
    quizzes = Quiz.objects.all().prefetch_related('questions')
    
    # Create a list to include quiz and counts
    quiz_data = []
    for quiz in quizzes:
        text_count = quiz.questions.filter(question_type='TEXT').count()
        mcq_count = quiz.questions.filter(question_type='MCQ').count()
        quiz_data.append({
            'quiz': quiz,
            'text_count': text_count,
            'mcq_count': mcq_count
        })
    
    return render(request, 'quizteachers/quiz_list.html', {'quiz_data': quiz_data})



def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Debugging: Print statements to check what is fetched
    print(f"Quiz: {quiz}")
    print(f"Questions: {questions}")

    # Initialize dictionaries for question texts and MCQs
    question_texts = {}
    question_mcqs = {}

    # Populate the dictionaries with related objects if they exist
    for question in questions:
        if question.question_type == 'TEXT':
            question_texts[question.id] = list(QuestionText.objects.filter(question=question))
        elif question.question_type == 'MCQ':
            question_mcqs[question.id] = list(QuestionMCQ.objects.filter(question=question))

    return render(request, 'quizteachers/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'question_texts': question_texts,
        'question_mcqs': question_mcqs,
    })