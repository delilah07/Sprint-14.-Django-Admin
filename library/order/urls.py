from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path(
        'create/<int:book_id>/',
        views.create_order,
        name='create_order',
    ),
    path(
        'return/<int:order_id>/',
        views.return_order,
        name='return_order',
    ),
]
