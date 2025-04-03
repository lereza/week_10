from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember

# Registering models directly
admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)

# Improved StudentAdmin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program")
    search_fields = ("lastname", "firstname", "middlename", "program__name")  # Added program name for search

# Registering OrgMember with customization
@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "organization", "date_joined")
    search_fields = ("student__lastname", "student__firstname")  # Search by student name

    def get_member_program(self, obj):
        try:
            member = Student.objects.get(id=obj.student_id)
            return member.program
        except Student.DoesNotExist:
            return None
    get_member_program.admin_order_field = 'student__program'  # Makes it sortable in admin
    get_member_program.short_description = 'Program'  # Custom column title
    