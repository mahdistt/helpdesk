import itertools

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormMixin
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import ListAPIView

from ticket import models, serializers
from ticket.forms import CreateQueryForm, EditQueryCategoryForm, CreateReplayForm


class CreateQuery(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
        Create a query ticket
    """
    model = models.Query
    form_class = CreateQueryForm
    template_name = 'ticket/create_ticket.html'
    success_message = "Your message has been successfully registered"
    success_url = reverse_lazy('ticket:view-ticket')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.operator_related = self.request.user
        obj.save()
        return super(CreateQuery, self).form_valid(form)


class EditQueryCategoryView(LoginRequiredMixin, UpdateView):
    """
        Redirect query category by operators
    """
    model = models.Query
    template_name = 'ticket/edit-query.html'
    form_class = EditQueryCategoryForm
    success_message = "Reference has been successfully"
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
        models.Query.objects.filter(pk=self.kwargs.get('pk')).update(operator_related=self.request.user.pk)
        models.Query.objects.filter(pk=self.kwargs.get('pk')).update(status='RESOLVED')
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
    success_message = "%(operator_related)s Your Query create successfully"
    success_url = reverse_lazy('dashboard:dashboard')


@login_required
def show_active_query(request):
    """
        Show all query that resolved or not
        filter by operators and users
    """
    qs_list1, qs_list2 = 0, 0

    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                # list1: query is resolve (up)
                qs_list1 = models.Query.objects.filter(~Q(operator_related__exact='0'))
                # list2: query not resolved (down)
                qs_list2 = models.Query.objects.filter(operator_related__exact='0')
            except:
                return render(request, 'dashboard/dashboard.html')
        elif request.user.is_staff:
            try:
                qs_list1 = models.Query.objects.filter(operator_related=request.user.pk)
                qs_list2 = models.Query.objects.filter(
                    Q(operator_related__exact='0') & Q(category_related=request.user.category)
                )
            except:
                return render(request, 'dashboard/dashboard.html')
        else:
            try:
                qs_list1 = models.Query.objects.filter(user_related=request.user)
            except:
                return render(request, 'dashboard/dashboard.html')
    else:
        return render(request, 'dashboard/dashboard.html')
    # --------------------paginator--------------------
    other_number = []
    qs = list(itertools.chain(qs_list1, other_number))
    paginated = Paginator(qs, 4)
    paginated_page = paginated.get_page(request.GET.get('page', 1))
    return render(request=request,
                  context={'object_list': paginated_page,
                           'qs_list2': qs_list2
                           },
                  template_name='ticket/list-query.html')


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


# --------------------------------------------REST-API-----------------------------------------------------

class QueryInfoAPI(ListAPIView):
    """
    API  all Query related with operator
    """

    serializer_class = serializers.QuerySerializer
    queryset = models.Query.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return qs.filter(user_related=self.request.user)


class ReplayInfoAPI(ListAPIView):
    """
    API  all Replay related with operator
    """
    serializer_class = serializers.ReplaySerializer
    queryset = models.Replay.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return qs.filter(operator_related=self.request.user)
