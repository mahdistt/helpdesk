from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from ticket import models


@login_required
def show_dashboard(request):
    return render(request, template_name='dashboard/dashboard.html')

