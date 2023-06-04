from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import *

# Register your models here.
#admin.site.register(School)
# admin.site.register(CustomUser, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Class)
admin.site.register(ScheduleClass)
admin.site.register(TestTable)