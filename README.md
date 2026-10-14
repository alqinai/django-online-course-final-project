# Django Online Course — Final Assessment Project

Django 5.2 project with course and lesson models, exam questions, choices, learner submissions, auto-scoring, passing results, and Django admin.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py makemigrations onlinecourse
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo
.venv/bin/python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/ and sign in with the **local demo-only** credentials `demo_admin` / `LocalDemoOnly123!`; capture an authentic screenshot showing **Authentication and Authorization** and **OnlineCourse** titled `03-admin-site.png`.

Visit the course URL shown by the `seed_demo` command, select `models.py`, `python manage.py runserver`, and `{% csrf_token %}` for the three demo questions. Submit and capture the actual Congratulations, score, and exam results page as `07-final.png`.

**Do not deploy the sample user password or default development secret key publicly.** Configure secure credentials, DEBUG off, ALLOWED_HOSTS and proper production hosting before production use.

## Coursera rubric

1. [Models](onlinecourse/models.py) — Question, Choice, Submission, and related models.
2. [Admin](onlinecourse/admin.py) — imports seven model classes; QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin.
3. `03-admin-site.png` — locally captured Django admin screenshot.
4. [Bootstrap course details](onlinecourse/templates/onlinecourse/course_details_bootstrap.html) — lessons, questions, choices, styled form.
5. [Views](onlinecourse/views.py) — submit and show_exam_result.
6. [URLs](onlinecourse/urls.py) — routes for submit and show_exam_result.
7. `07-final.png` — locally captured successful mock-exam result.
