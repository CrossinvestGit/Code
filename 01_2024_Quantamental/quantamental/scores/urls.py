from django.urls import path

from . import views

app_name = "scores"

urlpatterns = [
    path(route="signup/", view=views.SignUpView.as_view(), name="signup_view"),
    path(route="scores/", view=views.scores_view, name="scores_view"),
    path(route="test/", view=views.test_view, name="test_view"),
]
