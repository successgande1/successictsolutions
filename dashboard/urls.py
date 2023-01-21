from django.urls import path

from . import views
from user import views as user_view
# from stockmgt import views as stock_view

urlpatterns = [
    path('dashboard/', views.index, name = 'dashboard-index'),
    # path('add_item/', stock_view.add_item, name = 'add-item'),
    # path('add_order/<int:pk>/', stock_view.AddOrder, name = 'add-order'),
    # path('order_pay/<int:pk>/', stock_view.OrderPay, name = 'pay-order'),
    # path('delete/<int:pk>/', stock_view.DeleteItem, name = 'delete-item'),
    # path('delete/added_order/<int:pk>/', stock_view.DeleteAddedOrder, name = 'delete-order'),
    # path('update_stock/<int:pk>/', stock_view.AddStock, name = 'add-stock'),
    # path('update_item/<int:pk>/', stock_view.UpdateItem, name = 'update-item'),
    # path('stock/',  stock_view.list_items, name = 'list-items'),
    # path('register/', user_view.register, name = 'user-register'),
    # path('staff/detail/<int:pk>/', views.staff_detail, name = 'dashboard-staff-detail'),
    # path('profile/', views.profile, name = 'dashboard-profile'),
]