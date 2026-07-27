from django.urls import path

from . import views

app_name = "mcqs"
urlpatterns = [
    path("", views.mcq_list, name="mcq_list"),
    path("login/", views.mcq_login, name="mcq_login"),
    path("signup/", views.mcq_signup, name="mcq_signup"),
    path("logout/", views.mcq_logout, name="mcq_logout"),
    path("summary/", views.mcq_summary, name="mcq_summary"),
    path("<int:question_id>/submit/", views.submit_answer, name="submit_answer"),
    path("<int:question_id>/result/", views.mcq_result, name="mcq_result"),
]
