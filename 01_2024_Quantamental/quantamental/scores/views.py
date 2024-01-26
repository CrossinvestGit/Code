from django.shortcuts import render

from . import models


# Create your views here.
def scores_view(request):
    return render(request, "scores/scores_view.html")


def test_view(request):
    return render(request, "scores/test_view.html")
