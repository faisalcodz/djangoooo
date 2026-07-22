from django.urls import path

from . import views

app_name = "mcqs"
urlpatterns = [
    path("", views.mcq_list, name="mcq_list"),
    path("reset/", views.mcq_reset, name="mcq_reset"),
    path("<int:question_id>/submit/", views.submit_answer, name="submit_answer"),
    path("<int:question_id>/result/", views.mcq_result, name="mcq_result"),
]
