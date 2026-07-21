from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import MCQOption, MCQQuestion


def mcq_reset(request):
    request.session.pop("answered_mcqs", None)
    request.session.pop("mcq_results", None)
    return redirect("mcqs:mcq_list")


def mcq_list(request):
    all_questions = MCQQuestion.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by("pub_date")

    if not all_questions.exists():
        return render(request, "mcqs/index.html", {"no_questions": True})

    answered = request.session.get("answered_mcqs", {})
    results = request.session.get("mcq_results", {})

    current_question = None
    last_result = None

    for q in all_questions:
        if str(q.pk) not in answered:
            current_question = q
            break

    if current_question is None:
        return render(request, "mcqs/index.html", {"session_ended": True})

    options = current_question.mcqoption_set.all()

    return render(
        request,
        "mcqs/index.html",
        {
            "question": current_question,
            "options": options,
            "total_questions": all_questions.count(),
            "answered_count": len(answered),
        },
    )


def submit_answer(request, question_id):
    if request.method != "POST":
        return redirect("mcqs:mcq_list")

    question = get_object_or_404(
        MCQQuestion, pk=question_id, pub_date__lte=timezone.now()
    )

    answered = request.session.get("answered_mcqs", {})
    if str(question_id) in answered:
        return redirect("mcqs:mcq_list")

    try:
        selected_option_id = int(request.POST.get("option", 0))
    except (ValueError, TypeError):
        return redirect("mcqs:mcq_list")

    selected_option = get_object_or_404(
        MCQOption, pk=selected_option_id, question=question
    )

    answered[str(question_id)] = selected_option_id
    request.session["answered_mcqs"] = answered

    results = request.session.get("mcq_results", {})
    if selected_option.is_correct:
        results[str(question_id)] = "correct"
    else:
        correct_option = MCQOption.objects.filter(
            question=question, is_correct=True
        ).first()
        results[str(question_id)] = {
            "status": "wrong",
            "correct_option_id": correct_option.pk if correct_option else None,
            "correct_option_text": correct_option.option_text if correct_option else "",
        }
    request.session["mcq_results"] = results

    return redirect("mcqs:mcq_result", question_id=question_id)


def mcq_result(request, question_id):
    question = get_object_or_404(
        MCQQuestion, pk=question_id, pub_date__lte=timezone.now()
    )

    answered = request.session.get("answered_mcqs", {})
    results = request.session.get("mcq_results", {})

    if str(question_id) not in answered:
        return redirect("mcqs:mcq_list")

    result = results.get(str(question_id))
    options = question.mcqoption_set.all()

    all_questions = MCQQuestion.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by("pub_date")

    next_question = None
    for q in all_questions:
        if str(q.pk) not in answered:
            next_question = q
            break

    return render(
        request,
        "mcqs/result.html",
        {
            "question": question,
            "options": options,
            "result": result,
            "next_question": next_question,
            "total_questions": all_questions.count(),
            "answered_count": len(answered),
        },
    )
