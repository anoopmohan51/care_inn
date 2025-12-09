from django.urls import path
from workorder_api.views.workorder_attributes.workorder_attributes import *
from workorder_api.views.service_view.service_view import *
from workorder_api.views.room_views.room_views import *

urlpatterns = [
    path('service',ServiceCreateView.as_view()),
    path('service/<int:pk>',ServiceUpdateView.as_view()),
    path('room',RoomCreateView.as_view()),
    path('room/<int:pk>',RoomUpdateView.as_view()),
    path('workorder-attributes',WorkOrderAttributesCreateView.as_view()),
    path('workorder-attributes/<int:pk>',WorkOrderAttributesDetailView.as_view()),
    path('workorder-attributes/filter',WorkOrderAttributesFilterView.as_view()),
]