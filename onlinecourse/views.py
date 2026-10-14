"""Django views for course pages, exam submission, and result evaluation."""
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from .models import Choice, Course, Learner, Submission


def course_list(request):
    courses = Course.objects.all().order_by('name')
    return render(request, 'onlinecourse/course_list.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.prefetch_related('questions__choices').all()
    return render(request, 'onlinecourse/course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons,
    })


@login_required
def submit(request, course_id):
    """Persist selected exam choices for the signed-in learner."""
    if request.method != 'POST':
        return HttpResponseBadRequest('Exam submissions must use POST.')
    course = get_object_or_404(Course, pk=course_id)
    learner, _ = Learner.objects.get_or_create(user=request.user)
    questions = list(course_question_set(course))
    if not questions:
        return HttpResponseBadRequest('This course has no exam questions.')

    selected_ids = []
    for question in questions:
        answer_id = request.POST.get(f'question_{question.pk}')
        if not answer_id:
            return HttpResponseBadRequest('Please answer every question.')
        choice = Choice.objects.filter(pk=answer_id, question=question).first()
        if choice is None:
            return HttpResponseBadRequest('Invalid answer submitted.')
        selected_ids.append(choice.pk)

    with transaction.atomic():
        submission = Submission.objects.create(learner=learner, course=course)
        submission.choices.set(selected_ids)
    return redirect('onlinecourse:show_exam_result', course_id=course.pk,
                    submission_id=submission.pk)


def course_question_set(course):
    """Use a consistent order for all of the course's exam questions."""
    from .models import Question
    return Question.objects.filter(lesson__course=course).order_by('lesson__order', 'id')


@login_required
def show_exam_result(request, course_id, submission_id):
    """Grade the learner's saved answers and display question-level results."""
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission.objects.prefetch_related('choices'),
        pk=submission_id, course=course, learner__user=request.user,
    )
    answers = {choice.question_id: choice for choice in submission.choices.all()}
    questions = course_question_set(course).prefetch_related('choices')
    earned = 0
    total = 0
    exam_results = []
    for question in questions:
        selected = answers.get(question.pk)
        correct_choices = [choice for choice in question.choices.all() if choice.is_correct]
        correct = bool(selected and selected.is_correct)
        total += question.grade
        if correct:
            earned += question.grade
        exam_results.append({
            'question': question,
            'selected': selected,
            'correct': correct,
            'correct_choices': correct_choices,
        })
    score = round(100 * earned / total) if total else 0
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submission': submission,
        'score': score,
        'earned': earned,
        'total': total,
        'passed': total > 0 and score >= 70,
        'exam_results': exam_results,
    })
