from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def show_dashboard(request):
    return render(request, template_name='dashboard/dashboard.html')
