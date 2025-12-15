from django.urls import path
from workorder_api.views.workorder_attributes.workorder_attributes import *
from workorder_api.views.service_view.service_view import *
from workorder_api.views.room_views.room_views import *
from workorder_api.views.workorder_attribute_icon.workorder_attribute_icon import *
from workorder_api.views.workorder_temp.workorder_temp import *
from workorder_api.views.workorder.workorder import *
from workorder_api.views.workorder_comments.workorder_comments import *
from workorder_api.views.workorder_timeline.workorder_timeline import *

urlpatterns = [
    path('service',ServiceCreateView.as_view()),
    path('service/<int:pk>',ServiceUpdateView.as_view()),
    path('service/filter',ServiceFilterView.as_view()),
    path('room',RoomCreateView.as_view()),
    path('room/<int:pk>',RoomUpdateView.as_view()),
    path('room/filter',RoomFilterView.as_view()),
    path('workorder-attributes',WorkOrderAttributesCreateView.as_view()),
    path('workorder-attributes/<int:pk>',WorkOrderAttributesDetailView.as_view()),
    path('workorder-attributes/filter',WorkOrderAttributesFilterView.as_view()),
    path('workorder-attribute-icons',WorkOrderAttributeIconCreateView.as_view()),
    path('workorder-attribute-icons/<uuid:pk>',WorkOrderAttributeIconDetailView.as_view()),
    path('workorder-temp',WorkOrderTempCreateView.as_view()),
    path('workorder',WorkOrderCreateView.as_view()),
    path('workorder/<int:pk>',WorkorderDeleteView.as_view()),
    path('workorder/filter',WorkorderFilterView.as_view()),
    path('workorder-comments',WorkOrderCommentsCreateView.as_view()),
    path('workorder-comments/<int:workorder_id>',WorkOrderCommentsListView.as_view()),
    path('workorder-timeline',WorkOrderTimelineCreateView.as_view()),
    path('workorder-timeline/<int:workorder_id>',WorkOrderTimelineListView.as_view()),



]