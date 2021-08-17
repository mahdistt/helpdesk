import itertools

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormMixin

from ticket import models
from ticket.fomrs import CreateQueryForm, EditQueryCategoryForm, CreateReplayForm


class CreateQuery(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
        Create a query ticket
    """
    model = models.Query
    form_class = CreateQueryForm
    template_name = 'ticket/create_ticket.html'
    success_message = "was register successfully"
    success_url = reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.operator_related = self.request.user
        obj.save()
        super(CreateQuery, self)
        return JsonResponse({'massages': 'Created successfully.'}, status=201)


class EditQueryCategoryView(LoginRequiredMixin, UpdateView):
    """
        Redirect query category by operators
    """
    model = models.Query
    template_name = 'ticket/edit-query.html'
    form_class = EditQueryCategoryForm
    success_url = reverse_lazy('ticket:view-ticket')


class DetailQueryReplay(LoginRequiredMixin, FormMixin, DetailView):
    """
         Show a list of Replays for every single query
     """
    model = models.Query
    template_name = 'ticket/detail-query.html'
    form_class = CreateReplayForm
    success_message = "done successfully"
    success_url = reverse_lazy('ticket:view-ticket')

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     s = User.objects.get()
    #     try:
    #         return qs.filter(user_related=self.request.user)
    #     except:
    #         return qs.filter(user_related=self.request.user)

    # def get_success_url(self):
    #     return redirect('ticket:detail-quote', pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(DetailQueryReplay, self).get_context_data(**kwargs)
        context['form'] = CreateReplayForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.operator_related = self.request.user
        obj.query_related = self.object
        obj.save()
        return super(DetailQueryReplay, self).form_valid(obj)

    def form_invalid(self, form):
        JsonResponse({'message': 'form is not valid '})


class CreateReplay(LoginRequiredMixin, CreateView):
    """
    AJAX: Create Replay to one Query
    """
    template_name = 'ticket/detail-query.html'
    form_class = CreateReplayForm
    success_url = reverse_lazy('dashboard:dashboard')
    success_message = "%(operator_related)s Your Query create succcessfully"


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


class HistoryListViewReplay(LoginRequiredMixin, ListView):
    """
    show a list of replay histories and references (for admin)
    """
    model = models.Replay
    template_name = 'ticket/list-history-replay.html'
    extra_context = {'ReplayHistories': models.Replay.history,
                     }
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().order_by('id')
        if self.request.user.is_authenticated:
            try:
                if self.request.user.is_superuser:
                    return qs
            # return qs.filter(user_related=self.request.user)
            except:
                return qs.EmptyQuerySet


class HistoryListViewQuery(LoginRequiredMixin, ListView):
    """
    show a list of query histories (for admin)
    """
    model = models.Query
    template_name = 'ticket/list-history-query.html'
    extra_context = {'ReplayHistories': models.Query.history,
                     }
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().order_by('id')
        if self.request.user.is_authenticated:
            try:
                if self.request.user.is_superuser:
                    return qs
            # return qs.filter(user_related=self.request.user)
            except:
                return qs.EmptyQuerySet


class HistoryListViewOperator(LoginRequiredMixin, ListView):
    """
    show a list of replay history that filter by operator (for operator)
    """
    model = models.Replay
    template_name = 'ticket/list-history-operator.html'
    extra_context = {'ReplayHistories': models.Replay.history,
                     }
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().order_by('id')
        if self.request.user.is_authenticated:
            try:
                if self.request.user.is_staff:
                    qs = models.Replay.objects.filter(operator_related=self.request.user)
                    return qs
                    # return qs.filter(user_related=self.request.user)
            except:
                return qs.EmptyQuerySet
