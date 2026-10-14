"""Populate a sample course and an admin login for local assessment screenshots."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from onlinecourse.models import Choice, Course, Instructor, Learner, Lesson, Question


class Command(BaseCommand):
    help = 'Create demo admin account and a short sample course exam'

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='demo_admin')
        user.set_password('LocalDemoOnly123!')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        learner, _ = Learner.objects.get_or_create(user=user)
        instructor, _ = Instructor.objects.get_or_create(first_name='Alex', last_name='Morgan')
        course, _ = Course.objects.get_or_create(name='Introduction to Django', defaults={
            'description': 'Learn models, views, templates, and Django assessment workflows.'
        })
        course.instructors.add(instructor)
        course.learners.add(learner)
        lesson, _ = Lesson.objects.get_or_create(course=course, title='Django Fundamentals', defaults={
            'content': 'Explore the MVT architecture and how Django organizes applications.', 'order': 1
        })
        for text, items, correct in [
            ('Which Python file typically defines Django database models?', ['urls.py', 'models.py', 'admin.py'], 1),
            ('Which command starts the Django development server?', ['python manage.py runserver', 'python manage.py migrate', 'python manage.py collectstatic'], 0),
            ('Which tag protects Django POST forms against CSRF?', ['{% static %}', '{% csrf_token %}', '{% url %}'], 1),
        ]:
            question, _ = Question.objects.get_or_create(lesson=lesson, question_text=text, defaults={'grade': 10})
            for index, label in enumerate(items):
                Choice.objects.update_or_create(question=question, choice_text=label, defaults={'is_correct': index == correct})
        self.stdout.write(self.style.SUCCESS('Demo created! User: demo_admin | password: LocalDemoOnly123!'))
        self.stdout.write(f'Course page: http://127.0.0.1:8000/course/{course.pk}/')
