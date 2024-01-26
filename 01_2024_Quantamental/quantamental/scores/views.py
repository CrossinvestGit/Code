from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import models


# Create your views here.
@login_required
def scores_view(request):
    return render(request, "scores/scores_view.html")


@login_required
def test_view(request):
    return render(request, "scores/test_view.html")
