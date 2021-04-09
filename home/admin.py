from django.contrib import admin
from .models import Profile, Subject, Sub_Subject, Book, Question


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ("book_name", "related_subject")


class SubSubjectAdmin(admin.ModelAdmin):
    model = Sub_Subject
    list_display = ("sub_subject_name", "related_subject")


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("title", "subject", "profile", "publish_date")


admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Sub_Subject, SubSubjectAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Question, QuestionAdmin)
