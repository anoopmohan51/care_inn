from rest_framework.views import APIView
from workorder_api.models import WorkOrderTimeline
from workorder_api.serializers.workorder_timeline_serializer import WorkOrderTimelineSerializer
from core_api.response_utils.custom_response import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...serializers.workorder_serializer import WorkOrderSerializer
from datetime import datetime
from workorder_api.models import WorkOrder

class WorkOrderTimelineCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            activity = data.get('activity')
            workorder_id = data.get('workorder')
            user_id = request.user.id
            if not activity or not workorder_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Activity and workorder are required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            valid_activities = ['TIMER_START','TIMER_STOP','CLOSED','OPEN']
            if activity not in valid_activities:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Invalid activity"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            
            workorder = WorkOrder.objects.get(id=data.get('workorder'),is_delete=False)
            workorder_data = _prepare_workorder_status_for_activity(self,activity)
            if workorder_data:
                workorder_serializer = WorkOrderSerializer(
                    workorder,
                    data=workorder_data,
                    context={'request': request},
                    partial=True
                )
                if workorder_serializer.is_valid(raise_exception=True):
                    workorder_serializer.save()
                    timeline_data = _perpare_timeline_data(self,data,activity,user_id)
                    timeline_id = data.get("id")
                    if timeline_id:
                        timeline_data['id'] = timeline_id
                        timeline_serializer = WorkOrderTimelineSerializer(
                            data=timeline_data,
                            context={'request': request},
                            partial=True
                        )
                    else:
                        if  activity in ['TIMER_START','TIMER_STOP']:
                            timeline_serializer = WorkOrderTimelineSerializer(
                                data=timeline_data,
                                context={'request': request}
                            )
                    timeline_serializer.is_valid(raise_exception=True)
                    timeline_serializer.save()
                    return CustomResponse(
                        data=timeline_serializer.data,
                        status="success",
                        message=["Work order timeline created successfully"],
                        status_code=status.HTTP_201_CREATED,
                        content_type="application/json"
                    )        
        except WorkOrder.DoesNotExist:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Work order not found"],
                status_code=status.HTTP_404_NOT_FOUND,
                content_type="application/json"
            )
        except Exception as e:
            print("error:::::::",e)
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order timeline creation"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderTimelineUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
            workorder_timeline = WorkOrderTimeline.objects.get(id=pk)
            serializer = WorkOrderTimelineSerializer(workorder_timeline)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order timeline fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order timeline fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
    def put(self, request,pk):
        try:
            data = request.data
            workorder_timeline = WorkOrderTimeline.objects.get(id=pk)
            serializer = WorkOrderTimelineSerializer(workorder_timeline, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse(
                    data=serializer.data,
                    status="success",
                    message=["Work order timeline updated successfully"],
                    status_code=status.HTTP_200_OK,
                    content_type="application/json"
                )
        except Exception as e:
            return CustomResponse(
                data=None,  
                status="failed",
                message=["Error in Work order timeline updating"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )   

class WorkOrderTimelineListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,workorder_id):
        try:
            workorder_timeline = WorkOrderTimeline.objects.filter(workorder=workorder_id).order_by('-created_at')
            serializer = WorkOrderTimelineSerializer(workorder_timeline, many=True)
            return CustomResponse(
                data=serializer.data,
                status="success",
                message=["Work order timeline fetched successfully"],
                status_code=status.HTTP_200_OK,
                content_type="application/json"
            )
        except Exception as e:
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in Work order timeline fetching"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

def _perpare_timeline_data(self,data,activity,user_id):
    timeline_data = data.copy()
    timeline_data['initiated_by'] = user_id
    if activity=='TIMER_START':
        timeline_data['from_date'] = datetime.now()
    elif activity=='TIMER_STOP':
        timeline_data['to_date'] = datetime.now()
    return timeline_data

def _prepare_workorder_status_for_activity(self,activity):
    status_maping = {
        "TIMER_START": {"status":WorkOrder.WORKORDER_STATUS_IN_PROGRESS},
        "TIMER_STOP": {"status":WorkOrder.WORKORDER_STATUS_PAUSED},
        "CLOSED": {"status":WorkOrder.WORKORDER_STATUS_CLOSED},
        "OPEN": {"status":WorkOrder.WORKORDER_STATUS_ASSIGNED_NOT_STARTED},
    }
    return status_maping.get(activity,None)
