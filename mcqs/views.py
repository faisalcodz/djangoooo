from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import MCQAnswer, MCQOption, MCQQuestion


def mcq_login(request):
    if request.user.is_authenticated:
        return redirect("mcqs:mcq_list")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("mcqs:mcq_list")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "mcqs/login.html")


def mcq_signup(request):
    if request.user.is_authenticated:
        return redirect("mcqs:mcq_list")
    form_data = {}
    if request.method == "POST":
        form_data = {
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
        }
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        if not all([form_data["username"], form_data["email"], password]):
            messages.error(request, "All fields are required.")
        elif password != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=form_data["username"]).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=form_data["email"]).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(
                username=form_data["username"], email=form_data["email"], password=password
            )
            login(request, user)
            return redirect("mcqs:mcq_list")
    return render(request, "mcqs/signup.html", {"form_data": form_data})


@login_required
def mcq_logout(request):
    logout(request)
    return redirect("mcqs:mcq_login")


@login_required
def mcq_list(request):
    all_questions = MCQQuestion.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by("pub_date")

    if not all_questions.exists():
        return render(request, "mcqs/index.html", {"no_questions": True})

    answered_ids = set(
        MCQAnswer.objects.filter(user=request.user).values_list("question_id", flat=True)
    )

    current_question = None
    for q in all_questions:
        if q.pk not in answered_ids:
            current_question = q
            break

    if current_question is None:
        return redirect("mcqs:mcq_summary")

    options = current_question.mcqoption_set.all()

    correct_count = MCQAnswer.objects.filter(
        user=request.user, is_correct=True
    ).count()

    return render(
        request,
        "mcqs/index.html",
        {
            "question": current_question,
            "options": options,
            "total_questions": all_questions.count(),
            "answered_count": len(answered_ids),
            "correct_count": correct_count,
        },
    )


@login_required
def submit_answer(request, question_id):
    if request.method != "POST":
        return redirect("mcqs:mcq_list")

    question = get_object_or_404(
        MCQQuestion, pk=question_id, pub_date__lte=timezone.now()
    )

    if MCQAnswer.objects.filter(user=request.user, question=question).exists():
        return redirect("mcqs:mcq_list")

    try:
        selected_option_id = int(request.POST.get("option", 0))
    except (ValueError, TypeError):
        return redirect("mcqs:mcq_list")

    selected_option = get_object_or_404(
        MCQOption, pk=selected_option_id, question=question
    )

    MCQAnswer.objects.create(
        user=request.user,
        question=question,
        selected_option=selected_option,
        is_correct=selected_option.is_correct,
    )

    return redirect("mcqs:mcq_result", question_id=question_id)


@login_required
def mcq_result(request, question_id):
    question = get_object_or_404(
        MCQQuestion, pk=question_id, pub_date__lte=timezone.now()
    )

    answer = MCQAnswer.objects.filter(user=request.user, question=question).first()
    if not answer:
        return redirect("mcqs:mcq_list")

    options = question.mcqoption_set.all()

    all_questions = MCQQuestion.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by("pub_date")

    answered_ids = set(
        MCQAnswer.objects.filter(user=request.user).values_list("question_id", flat=True)
    )

    next_question = None
    for q in all_questions:
        if q.pk not in answered_ids:
            next_question = q
            break

    return render(
        request,
        "mcqs/result.html",
        {
            "question": question,
            "options": options,
            "answer": answer,
            "next_question": next_question,
            "total_questions": all_questions.count(),
            "answered_count": len(answered_ids),
        },
    )


@login_required
def mcq_summary(request):
    user_answers = MCQAnswer.objects.filter(user=request.user)
    correct_count = user_answers.filter(is_correct=True).count()
    total = user_answers.count()

    return render(
        request,
        "mcqs/summary.html",
        {
            "correct_count": correct_count,
            "total": total,
        },
    )
