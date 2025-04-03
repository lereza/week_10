from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_colleges(8)
        self.create_programs(10)
        self.create_organizations(2)  # Changed the method name to plural
        self.create_students(50)
        self.create_membership(10)

    def create_colleges(self, count):
        fake = Faker()
        for _ in range(count):
            College.objects.create(
                college_name=fake.company()
            )
        self.stdout.write(self.style.SUCCESS('Initial data for colleges created successfully.'))

    def create_programs(self, count):
        fake = Faker()
        for _ in range(count):
            Program.objects.create(
                prog_name=fake.word().title(),
                college=College.objects.order_by('?').first()  # Random college
            )
        self.stdout.write(self.style.SUCCESS('Initial data for programs created successfully.'))

    def create_organizations(self, count):  # Plural name to match other methods
        fake = Faker()
        for _ in range(count):
            words = [fake.word() for _ in range(2)]  # Two words for the organization name
            organization_name = ' '.join(words)
            Organization.objects.create(
                name=organization_name.title(),
                college=College.objects.order_by('?').first(),
                description=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS('Initial data for organizations created successfully.'))

    def create_students(self, count):
        fake = Faker('en_PH')
        for _ in range(count):
            program = Program.objects.order_by('?').first()  # Ensure this returns a valid Program
            if program is None:
                self.stdout.write(self.style.ERROR('No program available for student.'))
                continue

            Student.objects.create(
                student_id=f"{fake.random_int(2020, 2024)}-{fake.random_int(1, 8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=program
            )
        self.stdout.write(self.style.SUCCESS('Initial data for students created successfully.'))

    def create_membership(self, count):
        fake = Faker()
        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by('?').first(),
                organization=Organization.objects.order_by('?').first(),
                date_joined=fake.date_between(start_date="-2y", end_date="today")
            )
        self.stdout.write(self.style.SUCCESS('Initial data for student organizations created successfully.'))
