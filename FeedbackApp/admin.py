from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Feedback)
admin.site.register(Feedback_data)


from import_export import resources
from .models import QuestionMaster

class QuestionMasterResource(resources.ModelResource):
    class Meta:
        model = QuestionMaster

from import_export.admin import ImportExportModelAdmin
@admin.register(QuestionMaster)
class QuestionMasterAdmin(ImportExportModelAdmin):
    pass

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile

from import_export.admin import ImportExportModelAdmin
@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    pass

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

from import_export.admin import ImportExportModelAdmin
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    pass

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department

from import_export.admin import ImportExportModelAdmin
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    pass

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject

from import_export.admin import ImportExportModelAdmin
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    pass

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

from import_export.admin import ImportExportModelAdmin
@admin.register(Course)
class DepartmentAdmin(ImportExportModelAdmin):
    pass


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Department

from import_export.admin import ImportExportModelAdmin
@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    pass

class TICResource(resources.ModelResource):
    class Meta:
        model = TIC

from import_export.admin import ImportExportModelAdmin
@admin.register(TIC)
class QuestionMasterAdmin(ImportExportModelAdmin):
    pass
