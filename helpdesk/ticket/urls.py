from django.urls import path

from . import views

app_name = 'ticket'
urlpatterns = [
    path('create/', views.CreateQuery.as_view(), name='create-ticket'),
    path('view/', views.show_active_query, name='view-ticket'),
    path('detail/<str:pk>', views.DetailQueryReplay.as_view(), name='detail-query'),
    path('edit/<str:pk>', views.EditQueryCategoryView.as_view(), name='edit-query'),
    path('history/replay', views.HistoryListViewReplay.as_view(), name='list-history-replay'),
    path('history/operator', views.HistoryListViewOperator.as_view(), name='list-history-operator'),
    path('history/query', views.HistoryListViewQuery.as_view(), name='list-history-query'),
]
