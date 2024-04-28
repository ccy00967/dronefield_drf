from django.urls import path
from customer import views

urlpatterns = [
    path(
        "customer-requests/",
        views.CustomerRequestListView.as_view(),
        name=views.CustomerRequestListView.name,
    ),
    path(
        "customer-requests/<pk>/",
        views.CustomerRequestListUpdateDeleteView.as_view(),
        name=views.CustomerRequestListUpdateDeleteView.name,
    ),
]
