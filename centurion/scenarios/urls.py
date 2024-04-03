from django.urls import path
from .views import ScenarioListView, ScenarioDetailView, ScenarioCreateView, ScenarioUpdateView, ScenarioDeleteView
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView
from .views import PickupCreateView, PickupDeleteView, PickupDetailView, PickupListView, PickupUpdateView
from .views import navbar_scenario_list, scenario_dashboard, order_dashboard

# Scenarios
urlpatterns = [
    path('scenario/', ScenarioListView.as_view(), name='scenario_list'),
    path('scenario/<int:pk>/', ScenarioDetailView.as_view(), name='scenario_detail'),
    path('scenario/add/', ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenario/<int:pk>/edit/', ScenarioUpdateView.as_view(), name='scenario_update'),
    path('scenario/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario_delete'),
    path('scenario/partial/navbar-scenario-list/', navbar_scenario_list, name='navbar_scenario_list'),
    path('scenario/<int:pk>/dashboard/', scenario_dashboard, name='scenario_dashboard'),
]


# Orders
urlpatterns += [
    path('order/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/add/', OrderCreateView.as_view(), name='order_create'),
    path('order/add/pickup/<int:scenario_id>/', OrderCreateView.as_view(), name='order_create_with_scenario_id'),
    path('order/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/dashboard/', order_dashboard, name='order_dashboard'),
]

# Pickups
urlpatterns += [
    path('pickup/', PickupListView.as_view(), name='pickup_list'),
    path('pickup/<int:pk>/', PickupDetailView.as_view(), name='pickup_detail'),
    path('pickup/add/', PickupCreateView.as_view(), name='pickup_create'),
    path('pickup/add/scenario/<int:order_id>/', PickupCreateView.as_view(), name='pickup_create_with_order_id'),
    path('pickup/<int:pk>/edit/', PickupUpdateView.as_view(), name='pickup_update'),
    path('pickup/<int:pk>/delete/', PickupDeleteView.as_view(), name='pickup_delete'),
]