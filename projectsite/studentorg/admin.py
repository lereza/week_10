from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember

# Register the models
admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)

# StudentAdmin customization using decorator
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program")
    search_fields = ("lastname", "firstname")

# OrgMemberAdmin customization using decorator
@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "organization", "date_joined")
    search_fields = ("student__lastname", "student__firstname")

    # Custom method to get the program for the student
    def get_member_program(self, obj):
        try:
            member = Student.objects.get(id=obj.student_id)
            return member.program
        except Student.DoesNotExist:
            return None
