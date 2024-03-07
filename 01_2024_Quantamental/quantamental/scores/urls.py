from django.urls import path

from . import views

app_name = "scores"

urlpatterns = [
    path(route="signup/", view=views.SignUpView.as_view(), name="signup_view"),
    path(route="scores/", view=views.scores_view, name="scores_view"),
    path(route="singleStock/", view=views.singleStock_view, name="singleStock_view"),
    path(route="table/", view=views.table_view, name="table_view"),
    path(route="data/", view=views.table_view_data, name="table_data"),
    path(route="data2/", view=views.table_view_data_2, name="table_data2"),
    path(route="pf/", view=views.pf_view, name="pf_view"),
]
