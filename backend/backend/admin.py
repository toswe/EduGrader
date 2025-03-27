from django.contrib import admin

from backend.models import Question, Course, Test


admin.site.register(Question)
admin.site.register(Course)
admin.site.register(Test)
