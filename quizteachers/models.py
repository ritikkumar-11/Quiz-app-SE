from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return f"Quiz for {self.year} Year by {self.teacher.name}"


class Question(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('TEXT', 'Text Question'),
        ('MCQ', 'Multiple Choice Question'),
    ]
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=4, choices=QUIZ_TYPE_CHOICES)
    question_text = models.TextField(default='Question')

    def __str__(self):
        return self.question_text


class QuestionText(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_text_ref')
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question.question_text


class QuestionMCQ(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_mcq_ref')
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)

    class CorrectOption(models.TextChoices):
        OPTION_1 = '1', 'Option 1'
        OPTION_2 = '2', 'Option 2'
        OPTION_3 = '3', 'Option 3'
        OPTION_4 = '4', 'Option 4'

    correct_option = models.CharField(
        max_length=1,
        choices=CorrectOption.choices,
    )

    def __str__(self):
        return f"{self.question.question_text} - Correct Option: {self.get_correct_option_display()}"
