"""Course, assessment, and submission data models."""
from django.conf import settings
from django.db import models


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, related_name='courses', blank=True)
    learners = models.ManyToManyField(Learner, related_name='courses', blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='submissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.learner} - {self.course} - {self.created_at:%Y-%m-%d}'
