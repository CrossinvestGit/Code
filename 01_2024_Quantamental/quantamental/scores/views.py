from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

# from . import models
from .forms import UserRegisterForm


# Create your views here.
@login_required
def scores_view(request):
    return render(request, "scores/scores_view.html")


@login_required
def test_view(request):
    return render(request, "scores/test_view.html")


class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


#  def  signup_view(request):
#    return render(request, 'registration/signup.html', {'form': form})
