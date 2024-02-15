from django.urls import path

from . import views

app_name = "scores"

urlpatterns = [
    path(route="signup/", view=views.SignUpView.as_view(), name="signup_view"),
    path(route="scores/", view=views.scores_view, name="scores_view"),
    path(route="test/", view=views.test_view, name="test_view"),
    path(route="stock/", view=views.stock_view, name="stock_view"),
    path(route="data/", view=views.stock_view_data, name="data"),
    path(route="data2/", view=views.stock_view_data_2, name="data2"),
]
