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
from workorder_api.models import WorkOrderActivity

class WorkOrderTimelineCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            activity = data.get('activity')
            workorder_id = data.get('workorder')
            message = data.get('message',None)
            to = data.get('to',None)
            user_id = request.user.id
            if not activity or not workorder_id:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Activity and workorder are required"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            valid_activities = ['TIMER_START','TIMER_END','CLOSE','OPEN','CAPTURE','WAIT','BEGIN','NOTE']
            if activity not in valid_activities:
                return CustomResponse(
                    data=None,
                    status="failed",
                    message=["Invalid activity"],
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content_type="application/json"
                )
            if activity in ['WAIT','BEGIN','NOTE']:
                if activity == 'WAIT':
                    activity_data={
                        'activity':'WAITING',
                        'workorder_id':workorder_id,
                        'initiated_by_id':user_id,
                        'to_value':to,
                        'message':message,
                    }
                elif activity == 'BEGIN':
                    activity_data={
                        'activity':'BEGIN',
                        'workorder_id':workorder_id,
                        'initiated_by_id':user_id,
                    }
                elif activity == 'NOTE':
                    activity_data={
                        'activity':'NOTE',
                        'workorder_id':workorder_id,
                        'initiated_by_id':user_id,
                        'message':message,
                    }
                WorkOrderActivity.objects.create(**activity_data)
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
                    if activity in ['TIMER_START','TIMER_END']:
                        timeline_data = _perpare_timeline_data(self,data,activity,user_id)
                        timeline_id = data.get("id")
                        if timeline_id:
                            timeline = WorkOrderTimeline.objects.get(id=timeline_id)
                            timeline_serializer = WorkOrderTimelineSerializer(
                                timeline,
                                data=timeline_data,
                                context={'request': request},
                                partial=True
                            )
                            timeline_serializer.is_valid(raise_exception=True)
                            timeline_serializer.save()
                        else:
                            if  activity in ['TIMER_START','TIMER_END']:
                                timeline_serializer = WorkOrderTimelineSerializer(
                                    data=timeline_data,
                                    context={'request': request}
                                )
                        timeline_serializer.is_valid(raise_exception=True)
                        timeline_serializer.save()
                        data = timeline_serializer.data
                    else:
                        data = None
            else:
                data=None
            return CustomResponse(
                data=data,
                status="success",
                message=["Workorder updated successfully"],
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
            return CustomResponse(
                data=None,
                status="failed",
                message=["Error in updating workorder"],
                status_code=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class WorkOrderTimelineListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,workorder_id):
        try:
            limit = int(request.query_params.get('limit',10))
            offset = int(request.query_params.get('offset',0))
            workorder_timeline = WorkOrderTimeline.objects.filter(workorder=workorder_id).order_by('-created_at')
            serializer = WorkOrderTimelineSerializer(workorder_timeline[offset:offset+limit], many=True)
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
    elif activity=='TIMER_END':
        timeline_data['to_date'] = datetime.now()
    return timeline_data

def _prepare_workorder_status_for_activity(self,activity):
    status_maping = {
        "TIMER_START": {"status":WorkOrder.WORKORDER_STATUS_IN_PROGRESS},
        "TIMER_END": {"status":WorkOrder.WORKORDER_STATUS_PAUSED},
        "CLOSE": {"status":WorkOrder.WORKORDER_STATUS_CLOSED},
        "OPEN": {"status":WorkOrder.WORKORDER_STATUS_ASSIGNED_NOT_STARTED},
        "CAPTURE": {"assignee_type":"USER","user":self.request.user.id},
        "WAIT": {"status":WorkOrder.WORKORDER_STATUS_PAUSED}
    }
    return status_maping.get(activity,None)
