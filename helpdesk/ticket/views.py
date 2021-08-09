import itertools

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

# Create your views here.
from ticket import models
from ticket.fomrs import CreateQueryForm,EditQueryCategoryForm


class CreateQuery(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
        Create a query ticket
    """
    model = models.Query
    form_class = CreateQueryForm
    template_name = 'ticket/create_ticket.html'
    success_message = "was register successfully"
    success_url = reverse_lazy('dashboard:dashboard')


class EditQueryCategoryView(LoginRequiredMixin,UpdateView):
    """
        Redirect query category by operators
    """
    model = models.Query
    template_name = 'ticket/edit-query.html'
    form_class = EditQueryCategoryForm
    success_url = reverse_lazy('ticket:view-ticket')


class DetailQueryReplay(LoginRequiredMixin, DetailView):
    """
        Show a list of Replays for every single query
    """
    model = models.Query
    template_name = 'ticket/detail-query.html'

    def get_context_data(self, **kwargs):
        context = super(DetailQueryReplay, self).get_context_data()
        context['req'] = self.request
        return context


@login_required
def show_active_query(request):
    """
        Show all query that not resolved
        filter by operators and users
    """

    if request.user.is_authenticated:
        if not request.user.is_superuser:
            try:
                operator_organization = models.Query.objects.filter(operator_info=request.user)
            except:
                return render(request, 'dashboard/dashboard.html')
        else:
            operator_organization = models.Query.objects.all()
        if operator_organization is None:
            return render(request, 'dashboard/dashboard.html')
        other_number = []
        qs = list(itertools.chain(operator_organization, other_number))
        paginated = Paginator(qs, 2)
        paginated_page = paginated.get_page(request.GET.get('page', 1))
        return render(request=request,
                      context={'object_list': paginated_page, },
                      template_name='ticket/list-query.html')
    else:
        return render(request, 'dashboard/dashboard.html')

# class QuoteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     """
#         Create quote with some items
#     """
#     model = models.QuoteItem
#     form_class = QuoteCreateViewForm
#     template_name = 'create-quote.html'
#     success_message = "%(quote)s was register successfully"
#     success_url = reverse_lazy('dashboard:dashboard')
