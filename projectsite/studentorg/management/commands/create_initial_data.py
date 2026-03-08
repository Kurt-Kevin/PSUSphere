from django.core.management.base import BaseCommand
from faker import Faker

from studentorg.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = "Create initial data for the application"

    def handle(self, *args, **options):
        self.create_colleges()
        self.create_programs()
        self.create_organization(10)
        self.create_students(50)
        self.create_membership(10)

    def create_colleges(self):
        if not College.objects.exists():
            College.objects.bulk_create([
                College(college_name="College of Arts and Sciences"),
                College(college_name="College of Engineering"),
            ])
            self.stdout.write(self.style.SUCCESS("Created initial colleges."))

    def create_programs(self):
        if not Program.objects.exists():
            colleges = list(College.objects.all())
            if not colleges:
                self.stdout.write(self.style.WARNING("No colleges found; skipping program creation."))
                return

            programs = []
            for college in colleges:
                programs.extend([
                    Program(prog_name=f"Program {i} ({college.college_name})", college=college)
                    for i in range(1, 4)
                ])
            Program.objects.bulk_create(programs)
            self.stdout.write(self.style.SUCCESS("Created initial programs."))

    def create_organization(self, count):
        fake = Faker()
        if not College.objects.exists():
            self.stdout.write(self.style.WARNING("No colleges found; cannot create organizations."))
            return

        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            Organization.objects.create(
                name=" ".join(words).title(),
                college=College.objects.order_by("?").first(),
                description=fake.sentence(),
            )

        self.stdout.write(self.style.SUCCESS(
            "Initial data for organization created successfully."))

    def create_students(self, count):
        fake = Faker("en_PH")
        if not Program.objects.exists():
            self.stdout.write(self.style.WARNING("No programs found; cannot create students."))
            return

        for _ in range(count):
            Student.objects.create(
                student_id=f"{fake.random_int(2020, 2025)}-{fake.random_int(1, 8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=Program.objects.order_by("?").first(),
            )

        self.stdout.write(self.style.SUCCESS(
            "Initial data for students created successfully."))

    def create_membership(self, count):
        fake = Faker()
        if not Student.objects.exists() or not Organization.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Need students and organizations to create memberships."))
            return

        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by("?").first(),
                organization=Organization.objects.order_by("?").first(),
                date_joined=fake.date_between(start_date="-2y", end_date="today"),
            )

        self.stdout.write(self.style.SUCCESS(
            "Initial data for student organization created successfully."))
