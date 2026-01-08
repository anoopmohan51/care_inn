from django.urls import path
from workorder_api.views.service_view.service_view import *
from workorder_api.views.room_views.room_views import *
from workorder_api.views.workorder_temp.workorder_temp import *
from workorder_api.views.workorder.workorder import *
from workorder_api.views.workorder_comments.workorder_comments import *
from workorder_api.views.workorder_timeline.workorder_timeline import *
from workorder_api.views.workorder_activity.workorder_activity import *
from workorder_api.views.workorder_follower.workorder_follower import *
from workorder_api.views.workorder_settings.workorder_settings import *
from workorder_api.views.informations.informations import *
from workorder_api.views.requested_items.requested_items import *
from workorder_api.views.workorder_dashboard.workorder_dashboard import *
from workorder_api.views.workorder_dashboard.workorder_status_dashboard import *
from workorder_api.views.workorder_dashboard.workorder_per_day import *
from workorder_api.views.workorder_dashboard.workorder_type_graph import *
from workorder_api.views.workorder_dashboard.workorder_time import *

urlpatterns = [
    path('service',ServiceCreateView.as_view()),
    path('service/<int:pk>',ServiceUpdateView.as_view()),
    path('service/filter',ServiceFilterView.as_view()),
    path('room',RoomCreateView.as_view()),
    path('room/<int:pk>',RoomUpdateView.as_view()),
    path('room/filter',RoomFilterView.as_view()),
    path('nursing-station/workorder',WorkOrderTempCreateView.as_view()),
    path('workorder',WorkOrderCreateView.as_view()),
    path('workorder/<int:pk>',WorkorderDeleteView.as_view()),
    path('workorder/filter',WorkorderFilterView.as_view()),
    path('workorder-comments',WorkOrderCommentsCreateView.as_view()),
    path('workorder-comments/<int:workorder_id>',WorkOrderCommentsListView.as_view()),
    path('workorder-timeline',WorkOrderTimelineCreateView.as_view()),
    path('workorder-timeline/<int:workorder_id>',WorkOrderTimelineListView.as_view()),
    path('workorder-activity/<int:workorder_id>',WorkOrderActivityListView.as_view()),
    path('nursing-station/approve/workorder',WorkorderStatusCreateView.as_view()),
    path('workorder-followers',WorkOrderFollowerCreateView.as_view()),
    path('workorder-followers/<int:id>',WorkOrderFollowerDetailView.as_view()),
    path('workorder-followers/<int:workorder_id>',WorkOrderFollowerListView.as_view()),
    path('workorder-settings',WorkOrderSettingsCreateView.as_view()),
    path('workorder-settings/<int:id>',WorkOrderSettingsDetailView.as_view()),
    path('workorder-settings/filter',WorkOrderSettingsFilterView.as_view()),
    path('informations',InformationsCreateView.as_view()),
    path('informations/<int:id>',InformationsDetailView.as_view()),
    path('request-items',RequestedItemsCreateView.as_view()),
    path('request-items/<int:id>',RequestedItemsDetailView.as_view()),
    path('workorder-type-count',WorkOrderTypeDashboardCountView.as_view()),
    path('workorder-status-count',WorkOrderStatusDashboardCountView.as_view()),
    path('workorder-count-per-day',WorkOrderPerDayView.as_view()),
    path('workorder-type-count-weekdays',WorkOrderTypeGraphView.as_view()),
    path('workorder-time/summary',WorkOrderTimeView.as_view()),


]