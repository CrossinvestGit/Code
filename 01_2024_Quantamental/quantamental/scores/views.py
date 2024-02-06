from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import models
from .forms import UserRegisterForm


# VIEWS:
@login_required
def scores_view(request):
    return render(request=request, template_name="scores/scores_view.html")


@login_required
def test_view(request):
    context = {
        "products": models.Product.objects.all(),
        "headers": ["Product", "Category", "Price"],
        "headersl": ["product", "category", "price"],
    }
    return render(
        request=request,
        template_name="scores/test_view.html",
        context=context,
    )

# @login_required
def stock_view(request):
    return render(
        request=request,
        template_name="scores/stock_view.html"
    )

def stock_view_data(request):
    data = list(models.Product.objects.values())  # Retrieve data from your model
    return JsonResponse(data, safe=False)  # Return JSON response

    
# FORMS:
class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
