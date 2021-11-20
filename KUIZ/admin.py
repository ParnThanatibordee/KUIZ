from django.contrib import admin

from .models import Quiz, Question, Choice, Type, ClassroomUser

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Type)
admin.site.register(ClassroomUser)
