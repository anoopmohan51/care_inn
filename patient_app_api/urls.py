from django.urls import path
from patient_app_api.views.workorder_settings.workorder_settings import *
from patient_app_api.views.service_view.service_view import *
from patient_app_api.views.informations.informations import *
from patient_app_api.views.requested_items.requested_items import *
from patient_app_api.views.workorder_patient_request.workorder_patient_request import *
from patient_app_api.views.workorder.workorder import *
from patient_app_api.views.folder_details.folder_details import *

urlpatterns = [
    path('workorder-settings/<int:id>',WorkorderSettingsDetailsView.as_view()),
    path('workorder-settings/filter',WorkorderSettingsFilterView.as_view()),
    path('service/<int:pk>',ServiceDetailsView.as_view()),
    path('service/filter',ServiceFilterView.as_view()),
    path('informations/<int:id>',InformationsDetailsView.as_view()),
    path('requested-items/<int:id>',RequestedItemsDetailsView.as_view()),
    path('patient-request/workorder',WorkOrderNursingStationRequestCreateView.as_view()),
    path('nursing-station/approve/workorder',WorkorderNursingStationView.as_view()),
    path('workorder/filter',WorkorderFilterView.as_view()),
    path('workorder/<int:id>',WorkorderDetailsView.as_view()),
    path('folder-details/<int:id>',FolderDetailsView.as_view()),
    

]