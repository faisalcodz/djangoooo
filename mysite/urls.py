from django.contrib import admin
from django.urls import include, path

from polls import views

admin.site.login_url = "/admin/login/"

urlpatterns = [
    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

