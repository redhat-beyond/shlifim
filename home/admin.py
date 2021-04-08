from django.contrib import admin
from .models import Profile, Subject, Sub_Subject, Book
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class SubSubjectAdmin(admin.ModelAdmin):
    model = Sub_Subject
    list_display = ("sub_subject_name", "related_subject")


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ("book_name", "related_subject")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Sub_Subject, SubSubjectAdmin)
admin.site.register(Book, BookAdmin)
