from django.contrib import admin

from .models import Teacher, Quiz, QuestionText, QuestionMCQ
admin.site.register(Teacher)
admin.site.register(Quiz)
admin.site.register(QuestionText)
admin.site.register(QuestionMCQ)